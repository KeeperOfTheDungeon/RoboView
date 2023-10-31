from tkinter import messagebox

import customtkinter as ctk

from Devices.AntDeviceConfig import AntDeviceConfig
from RoboControl.Robot.AbstractRobot.AbstractRobot import AbstractRobot
from RoboControl.Robot.Device.Generic.DataHub.DataHub import DataHub
from RoboView.Robot.Viewer.WindowBar import WindowBar
from RoboView.Robot.Device.Viewer.DeviceView import DeviceView


class DataHubDataView(DeviceView):
    FRAME_NAME: str = "Main Data Hub"

    def __init__(self, root: ctk.CTkFrame, device: DataHub, window_bar: WindowBar):
        super().__init__(root, device, window_bar)

    def set_robot(self, robot: AbstractRobot) -> bool:
        sensors: DataHub = robot.get_device_on_name(AntDeviceConfig.MAIN_DATA_HUB["DeviceName"])
        if sensors is None:
            messagebox.showerror("Error", "No leg controllers available!")
            return False
        self.make_display(robot.get_name(), sensors)
        return True

    def make_display(self, robot_name: str, data_hub: DataHub) -> None:
        self.set_device(robot_name, data_hub)
        # for text in data_hub.get_texts():
        #     self.add_component(TextDataView.create_view(text))
