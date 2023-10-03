from tkinter import TOP, LEFT, Menu, StringVar, RIGHT
import customtkinter as ctk
import tkinter as tk

from RoboControl.Robot.AbstractRobot.AbstractListener import ComStatusListener
from RoboControl.Robot.Component.statistic.ComStatus import ComStatus


class ComStatisticsView(ComStatusListener):
    _context_menu: Menu

    def __init__(self, root, device):
        self._frame = ctk.CTkFrame(master=root, fg_color='white', corner_radius=3, border_width=1)
        self._root = root
        self._device = device

        self._rx_count = StringVar()
        self._tx_count = StringVar()
        self._lost_count = StringVar()
        self._invalid_count = StringVar()

        self.build_view()

        device.add_com_status_listener(self)

    def build_view(self):
        label_font = ctk.CTkFont(family="Arial", size=12)
        text_prop = {
            "text_color": "black",
            "font": label_font,
            "height": 12
        }

        ctk.CTkLabel(self._frame, text="COM", **text_prop).pack(side=TOP, padx=2, pady=(2, 0))

        ctk.CTkLabel(self._frame, text="rx:", **text_prop).pack(side=LEFT, padx=(5, 2))
        ctk.CTkLabel(
            self._frame, textvariable=self._rx_count, text=" - ", **text_prop
        ).pack(side=LEFT, padx=(1, 5))

        ctk.CTkLabel(self._frame, text="tx:", **text_prop).pack(side=LEFT, padx=(5, 2))
        ctk.CTkLabel(
            self._frame, textvariable=self._tx_count, text=" - ", **text_prop
        ).pack(side=LEFT, padx=(1, 5))

        ctk.CTkLabel(self._frame, text="lost:", **text_prop).pack(side=LEFT, padx=(5, 2))
        ctk.CTkLabel(
            self._frame, textvariable=self._lost_count, text=" - ", **text_prop
        ).pack(side=LEFT, padx=(1, 5))

        ctk.CTkLabel(self._frame, text="inv:", **text_prop).pack(side=LEFT, padx=(5, 2))
        ctk.CTkLabel(
            self._frame, textvariable=self._invalid_count, text=" - ", **text_prop
        ).pack(side=LEFT, padx=(0, 10))

        self._frame.bind("<ButtonRelease-3>", self.mouse_released)

        self._context_menu = Menu(self._frame, tearoff=0)
        self._context_menu.add_command(label="Clear com Statistic", command=self._device.remote_clear_com_statistics)
        ctk.CTkButton(
            self._frame, text="clear", width=30,
            fg_color='lightgrey', text_color='black', hover_color='grey',
            command=self._device.remote_clear_com_statistics
        ).pack(side=RIGHT, padx=2)

    def mouse_released(self, event):
        try:
            self._context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self._context_menu.grab_release()

    def com_status_changed(self, statistic: ComStatus) -> None:
        self._rx_count.set(str(statistic.get_recived_messages()))
        self._tx_count.set(str(statistic.get_transfered_messages()))
        self._lost_count.set(str(statistic.get_lost_messages()))
        self._invalid_count.set(str(statistic.get_invalid_messages()))

    def get_frame(self) -> ctk.CTkFrame:
        return self._frame
