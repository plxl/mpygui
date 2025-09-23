from CTkListbox import CTkListbox

"""
fixes multiselect to instead require ctrl or shift to be held
in order to select additional items (preferred over click toggle)
"""

class CTkCustomListbox(CTkListbox):
    def insert(self, index, option, update=True, **args):
        """Insert item with modified click behaviour"""
        button = super().insert(index, option, update=update, **args)

        if self.multiple:
            # remove source select method
            button.configure(command=None)

            # get index for this button
            index = None
            for k, v in self.buttons.items():
                if v is button:
                    index = k
                    break

            if index is None:
                return button

            button.bind("<Button-1>", lambda e, num=index: self._single_select(num))
            button.bind("<Control-Button-1>", lambda e, num=index: self._ctrl_toggle(num))
            button.bind("<Shift-Button-1>", lambda e, b=button: self.select_multiple(b))

        return button

    def _single_select(self, index):
        self.deactivate("all")
        self.select(index)

    def _ctrl_toggle(self, index):
        if index in self.curselection():
            self.deselect(index)
        else:
            self.select(index)
