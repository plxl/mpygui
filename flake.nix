{
  description = "Flake using pyproject.toml metadata for mpygui";

  inputs.pyproject-nix.url = "github:pyproject-nix/pyproject.nix";
  inputs.pyproject-nix.inputs.nixpkgs.follows = "nixpkgs";

  outputs =
    { nixpkgs, pyproject-nix, ... }:
    let
      inherit (nixpkgs) lib;
      forAllSystems = lib.genAttrs lib.systems.flakeExposed;

      project = pyproject-nix.lib.project.loadPyproject { projectRoot = ./.; };

      pythonAttr = "python313";

      mkSystemCfg =
        system:
        let
          appName = "mpygui";
          pkgs = import nixpkgs { inherit system; };
          python = pkgs.${pythonAttr};
          isDarwin = pkgs.stdenv.isDarwin;

          # select correct build dependency for system
          buildTool = if isDarwin then "py2app" else "pyinstaller";
          pythonEnv = python.withPackages (
            ps: (project.renderers.withPackages { inherit python; } ps) ++ [ ps.${buildTool} ]
          );
          basePackage = python.pkgs.buildPythonPackage (
            project.renderers.buildPythonPackage { inherit python; }
          );

          appDrv = pkgs.stdenv.mkDerivation {
            pname = appName;
            version = project.metadata.version or "0.0.0";
            src = ./.;

            buildInputs = [ pythonEnv ];

            # choose the build phase at evaluation time
            buildPhase =
              if isDarwin then
                ''
                  # run py2app from the environment that has py2app + your deps
                  ${pythonEnv.interpreter} setup.py py2app
                ''
              else
                ''
                  # run PyInstaller from the environment that has pyinstaller + your deps
                  ${pythonEnv.interpreter} -m PyInstaller --onefile --windowed -n ${appName} src/mpygui/launch.py
                '';

            installPhase =
              if isDarwin then
                ''
                  mkdir -p $out
                  cp -r dist/*.app $out/
                ''
              else
                ''
                  mkdir -p $out/bin
                  cp dist/${appName} $out/bin/
                '';
          };
        in
        {
          pkgs = pkgs;
          python = python;
          pythonEnv = pythonEnv;
          basePackage = basePackage;
          app = appDrv;
          appName = appName;
        };
    in
    {
      devShells = forAllSystems (
        system:
        let
          cfg = mkSystemCfg system;
        in
        {
          default = cfg.pkgs.mkShell {
            packages = [ cfg.pythonEnv ];
            shellHook = ''
              export PYTHONPATH=$PWD/src:$PYTHONPATH
              echo "run with: \"python -m ${cfg.appName}\""
            '';
          };
        }
      );

      packages = forAllSystems (
        system:
        let
          cfg = mkSystemCfg system;
        in
        {
          default = cfg.app; # platform-appropriate artifact (always named "mPyGUI")
          wheel = cfg.basePackage; # plain installable package
        }
      );
    };
}
