from tkinter import LEFT, RIGHT, Menu, Spinbox
from typing import List

import customtkinter as ctk

from RoboControl.Robot.Device.RobotDevice import RobotDevice
from RoboControl.Robot.Device.control.DataAquisator import DataAquisator
from RoboView.Robot.Device.Viewer.Spinbox import Spinbox


class ToolBar:
    def __init__(self, root, device):
        self._frame = ctk.CTkFrame(master=root, corner_radius=0, fg_color='grey15', border_width=1)
        self._root = root

        self._device = device
        aquisators: List[DataAquisator] = self._device.get_data_aquisators() if self._device else []
        self._all_aquisators: List[str] = [a.get_name() for a in aquisators]

        btn_ping = ctk.CTkButton(
            self._frame, text="ping", command=self.send_ping, width=30, height=25, corner_radius=5)
        btn_ping.pack(side=RIGHT)

        self.build_view()

    def send_ping(self):
        self._device.remote_ping_device()

    def build_view(self):
        self._period = Spinbox(self._frame, step_size=10, height=20, corner_radius=5, fg_color='#565b5e')
        self._period.set(1000)
        self._period.pack(side=LEFT)

        self._aquisators = ctk.CTkComboBox(self._frame, values=self._all_aquisators, height=25)
        self._aquisators.pack(side=LEFT)

        button = ctk.CTkButton(self._frame, text="On", width=30, height=25, corner_radius=5)
        button.configure(command=self.start_stream)
        button.pack(side=LEFT)

        button = ctk.CTkButton(self._frame, text="Off", width=30, height=25, corner_radius=5)
        button.configure(command=self.stop_stream)
        button.pack(side=LEFT)

        self._frame.bind("<ButtonRelease-3>", self.mouse_released)

        self._context_menue = Menu(self._frame, tearoff=0)
        self._context_menue.add_command(
            label="Clear all streams", command=self.on_clear)
        self._context_menue.add_command(
            label="Pause all streams", command=self.on_pause)
        self._context_menue.add_command(
            label="Continue all streams", command=self.on_continue)
        self._context_menue.add_separator()
        self._context_menue.add_command(
            label="Save all streams", command=self.on_save)
        self._context_menue.add_command(
            label="Load all streams", command=self.on_load)

    def mouse_released(self, event):

        try:
            self._context_menue.tk_popup(event.x_root, event.y_root)
        finally:
            self._context_menue.grab_release()

    def on_clear(self):
        self._device.remote_clear_streams()

    def on_pause(self):
        self._device.remote_pause_streams()
        pass

    def on_continue(self):
        self._device.remote_continue_streams()
        pass

    def on_save(self):
        self._device.remote_save_streams()
        pass

    def on_load(self):
        self._device.remote_load_streams()
        pass

    def _get_selection_index(self) -> int:
        selection = self._aquisators.get()
        return self._all_aquisators.index(selection)

    def start_stream(self):
        index = self._get_selection_index() + 1
        self._device.remote_start_stream(index, int(int(self._period.get())/10))

    def stop_stream(self):
        index = self._get_selection_index() + 1
        self._device.remote_stop_stream(index)

    def get_frame(self):
        return self._frame

    def set_device(self, device: RobotDevice) -> None:
        self._device = device
