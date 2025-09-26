import customtkinter as ctk
from tkinter import HORIZONTAL, VERTICAL

"""
why? because the tk Paned Window doesn't match with ctk
it would require some icky stuff to look good and IMO would be worse than this
"""

class Splitter(ctk.CTkFrame):
    def __init__(self, master, target_frame, orientation=VERTICAL, minsize=100, minremainder=100, hover_color='gray30', **kwargs):
        """
        orientation: VERTICAL -> left/right resize
                     HORIZONTAL -> top/bottom resize
        """
        if orientation == VERTICAL:
            super().__init__(master, width=4, cursor="sb_h_double_arrow", **kwargs)
        elif orientation == HORIZONTAL:
            super().__init__(master, height=4, cursor="sb_v_double_arrow", **kwargs)
        else:
            raise ValueError("orientation must be 'vertical' or 'horizontal'")
        
        self.master = master
        self.target = target_frame
        self.orientation = orientation
        self.minsize = minsize
        self.minremainder = minremainder
        self.start_pos = 0
        self.start_size = 0

        self.hover_color = hover_color
        self.configure(fg_color="transparent")
        self.resizing = False
        self.mouse_hovered = False

        self.bind("<Enter>", lambda e: self.update_hover_color(True))
        self.bind("<Leave>", lambda e: self.update_hover_color(False))

        self.bind("<ButtonPress-1>", self.start_resize)
        self.bind("<ButtonRelease-1>", self.stop_resize)
        self.bind("<B1-Motion>", self.do_resize)
        self._resize_job = None
        
    def update_hover_color(self, mouse_hovered):
        self.mouse_hovered = mouse_hovered
        if mouse_hovered or self.resizing:
            self.configure(fg_color=self.hover_color)
        else:
            self.configure(fg_color="transparent")
            

    def start_resize(self, event):
        self.resizing = True
        self.configure(fg_color=self.hover_color)

        if self.orientation == "vertical":
            self.start_pos = event.x_root
            self.start_size = self.target.winfo_width()
        else: # horizontal
            self.start_pos = event.y_root
            self.start_size = self.target.winfo_height()

    def do_resize(self, event):
        # throttle updates using after_cancel/after
        if self._resize_job is not None:
            self.after_cancel(self._resize_job)

        self._last_event = event
        self._resize_job = self.after(1, self.apply_resize) # 1ms is enough

    def apply_resize(self):
        event = self._last_event
        if self.orientation == "vertical":
            delta = event.x_root - self.start_pos
            new_size = max(self.minsize, self.start_size + delta)
            new_size = min(self.master.winfo_width() - self.minremainder, new_size)
            self.target.configure(width=new_size)
        else:
            delta = event.y_root - self.start_pos
            new_size = max(self.minsize, self.start_size - delta)
            new_size = min(self.master.winfo_height() - self.minremainder, new_size)
            self.target.configure(height=new_size)
        self._resize_job = None
        
    def stop_resize(self, event):
        self.resizing = False
        if not self.mouse_hovered:
            self.configure(fg_color="transparent")
