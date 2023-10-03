from tkinter import LEFT, RIGHT, TOP, Menu, StringVar
import customtkinter as ctk

from RoboControl.Robot.AbstractRobot.AbstractListener import CpuStatusListener
from RoboControl.Robot.Component.statistic.CpuStatus import CpuStatus


class CpuStatisticsView(CpuStatusListener):
    _context_menu: Menu

    def __init__(self, root, device):
        self._frame = ctk.CTkFrame(
            master=root, fg_color='white', height=50, corner_radius=3)
        self._root = root
        self._device = device

        self._last_load = StringVar()
        self._min_load = StringVar()
        self._max_load = StringVar()

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
        self._last_load_label = ctk.CTkLabel(
            self._frame, textvariable=self._last_load, text=" - ", font=label_font, text_color='black')
        self._last_load_label.pack(side=LEFT,  padx=(0, 10))

        label = ctk.CTkLabel(self._frame, text="min :",
                             font=label_font, text_color='black')
        label.pack(side=LEFT, padx=2)
        self._min_load_label = ctk.CTkLabel(
            self._frame, textvariable=self._min_load, text=" - ", font=label_font, text_color='black')
        self._min_load_label.pack(side=LEFT,  padx=(0, 10))

        label = ctk.CTkLabel(self._frame, text="max :",
                             font=label_font, text_color='black')
        label.pack(side=LEFT, padx=2)
        self._max_load_label = ctk.CTkLabel(
            self._frame, textvariable=self._max_load, text=" - ", font=label_font, text_color='black')
        self._max_load_label.pack(side=LEFT, padx=(0, 10))

        self._frame.bind("<ButtonRelease-3>", self.mouse_released)

        self._context_menu = Menu(self._frame, tearoff=0)
        self._context_menu.add_command(
            label="Clear cpu Statistic", command=self.on_clear_statistic)

        label = ctk.CTkButton(self._frame, text="clear", width=30,
                              fg_color='lightgrey', text_color='black', hover_color='grey')
        label.pack(side=RIGHT, padx=2)

    def mouse_released(self, event):

        try:
            self._context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self._context_menu.grab_release()

    def on_clear_statistic(self):
        self._device.remote_clear_cpu_statistics()
        pass

    def cpu_status_changed(self, statistic: CpuStatus):
        self._min_load.set(str(statistic.get_min_load()))
        self._max_load.set(str(statistic.get_max_load()))
        self._last_load.set(str(statistic.get_last_load()))

    def get_frame(self) -> ctk.CTkFrame:
        return self._frame
