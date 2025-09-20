import re

def parse_tkdnd_files(data: str):
    # matches {...} or plain paths without spaces
    return re.findall(r'\{([^}]*)\}|(\S+)', data)
