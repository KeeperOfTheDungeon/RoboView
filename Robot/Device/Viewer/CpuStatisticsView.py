
from tkinter import LEFT, RIGHT, TOP, Button, Frame, Label, Menu, W, E
import customtkinter as ctk


class CpuStatisticsView:
    def __init__(self, root, device):
        self._frame = ctk.CTkFrame(
            master=root, fg_color='white', height=50, corner_radius=3)
        self._root = root
        self._device = device
        self.build_view()

        device.add_cpu_status_listener(self)

    def build_view(self):
        label_font = ctk.CTkFont()

        label = ctk.CTkLabel(self._frame, text="CPU",
                             height=12, font=("Arial", 12), text_color='black')
        label.pack(side=TOP)

        label = ctk.CTkLabel(self._frame, text="last :",
                             font=label_font, text_color='black')
        label.pack(side=LEFT, padx=2)
        self._last_load = ctk.CTkLabel(
            self._frame, text=" - ", font=label_font, text_color='black')
        self._last_load.pack(side=LEFT,  padx=(0, 10))

        label = ctk.CTkLabel(self._frame, text="min :",
                             font=label_font, text_color='black')
        label.pack(side=LEFT, padx=2)
        self._min_load = ctk.CTkLabel(
            self._frame, text=" - ", font=label_font, text_color='black')
        self._min_load.pack(side=LEFT,  padx=(0, 10))

        label = ctk.CTkLabel(self._frame, text="max :",
                             font=label_font, text_color='black')
        label.pack(side=LEFT, padx=2)
        self._max_load = ctk.CTkLabel(
            self._frame, text=" - ", font=label_font, text_color='black')
        self._max_load.pack(side=LEFT, padx=(0, 10))

        self._frame.bind("<ButtonRelease-3>", self.mouse_released)

        self._context_menue = Menu(self._frame, tearoff=0)
        self._context_menue.add_command(
            label="Clear cpu Statistic", command=self.on_clear_statistic)

        label = ctk.CTkButton(self._frame, text="clear", width=30,
                              fg_color='lightgrey', text_color='black', hover_color='grey')
        label.pack(side=RIGHT, padx=2)

    def mouse_released(self, event):

        try:
            self._context_menue.tk_popup(event.x_root, event.y_root)
        finally:
            self._context_menue.grab_release()

    def on_clear_statistic(self):
        self._device.remote_clear_cpu_statistics()
        pass

    def cpu_status_changed(self, statistic):
        min_load = statistic.get_min_load()
        self._min_load['text'] = str(min_load)

        max_load = statistic.get_max_load()
        self._max_load['text'] = str(max_load)

        last_load = statistic.get_last_load()
        self._last_load['text'] = str(last_load)
