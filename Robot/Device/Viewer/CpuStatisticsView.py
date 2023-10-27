from tkinter import LEFT, RIGHT, TOP, Menu, StringVar
import customtkinter as ctk



class CpuStatisticsView():
    _context_menu: Menu

    def __init__(self, root, device):
        self._frame = ctk.CTkFrame(master=root, fg_color='white', corner_radius=3, border_width=1)
        self._root = root
        self._device = device

        self._last_load = StringVar()
        self._min_load = StringVar()
        self._max_load = StringVar()

        self.build_view()

        device.add_cpu_status_listener(self)

    def build_view(self):
        label_font = ctk.CTkFont(family="Arial", size=12)
        text_prop = {
            "text_color": "black",
            "font": label_font,
            "height": 12
        }

        ctk.CTkLabel(self._frame, text="CPU", **text_prop).pack(side=TOP, padx=2, pady=(2, 0))

        ctk.CTkLabel(self._frame, text="last:", **text_prop).pack(side=LEFT, padx=(5, 2))
        ctk.CTkLabel(
            self._frame, textvariable=self._last_load, text=" - ", **text_prop
        ).pack(side=LEFT, padx=(1, 5))

        ctk.CTkLabel(self._frame, text="min:", **text_prop).pack(side=LEFT, padx=(5, 2))
        ctk.CTkLabel(
            self._frame, textvariable=self._min_load, text=" - ", **text_prop
        ).pack(side=LEFT, padx=(1, 5))

        ctk.CTkLabel(self._frame, text="max:", **text_prop).pack(side=LEFT, padx=(5, 2))
        ctk.CTkLabel(
            self._frame, textvariable=self._max_load, text=" - ", **text_prop
        ).pack(side=LEFT, padx=(1, 5))

        self._frame.bind("<ButtonRelease-3>", self.mouse_released)

        self._context_menu = Menu(self._frame, tearoff=0)
        self._context_menu.add_command(label="Clear cpu Statistic", command=self._device.remote_clear_cpu_statistics)

        ctk.CTkButton(
            self._frame, text="clear", width=30,
            fg_color='lightgrey', text_color='black', hover_color='grey',
            command=self._device.remote_clear_cpu_statistics
        ).pack(side=RIGHT, padx=2)

    def mouse_released(self, event):
        try:
            self._context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self._context_menu.grab_release()

    def cpu_status_changed(self, statistic):
        self._min_load.set(str(statistic.get_min_load()))
        self._max_load.set(str(statistic.get_max_load()))
        self._last_load.set(str(statistic.get_last_load()))

    def get_frame(self) -> ctk.CTkFrame:
        return self._frame
