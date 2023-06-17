import tkinter as tk
from tkinter import ttk
from typing import Optional

import customtkinter as ctk

from RoboControl.Com.PacketLogger.DataPacketLogger import DataPacketLoggerEvent, DataPacketLogger
from RoboControl.Robot.AbstractRobot.AbstractRobot import AbstractRobot
from RoboView.Gui.InternalWindow.InternalWindow import InternalWindow
from RoboView.Robot.Viewer.RobotSettings import RobotSettings
from RoboView.Robot.Viewer.WindowBar import WindowBar
from RoboView.Robot.dataPacketLogger.viewer.DataPacketTableModel import DataPacketTableModel
from RoboView.Robot.dataPacketLogger.viewer.FilterDataPanel import FilterDataPanel
from RoboView.Robot.dataPacketLogger.viewer.FilterEditorPanel import FilterEditorPanel
from RoboView.Robot.dataPacketLogger.viewer.FilterEditorToolbar import FilterEditorToolbar


class DataPacketFilterEditor(InternalWindow):
    FRAME_NAME: str = "Data packet filter editor"

    def __init__(self, root: ctk.CTkFrame, window_bar: WindowBar):
        raise ValueError("WIP DataPacketFilterEditor is not yet implemented")
        super().__init__(root, self.FRAME_NAME, window_bar)
        self.root = root

        self._robot: Optional[AbstractRobot] = None
        self.build_view()

    def build_view(self) -> None:
        self.move(-10, -10)
        self.set_min_dimension(950, 200)

        form = ctk.CTkFrame(fg_color="transparent", master=self._frame)
        form.pack(fill="both", expand=True,
                  padx=(10, 20), pady=(30, 20),
                  ipadx=5, ipady=5)

        # this.setLayout(new  BorderLayout());
        self._toolbar = FilterEditorToolbar()
        # this.add(toolBar,BorderLayout.PAGE_START);

        self._filter_data = FilterDataPanel()
        # this.add(this.filterData,BorderLayout.CENTER);

        self._filter_editor = FilterEditorPanel()
        # this.add(this.filterEditor,BorderLayout.PAGE_END);

        self._toolbar.set_selector_listener(self._filter_data)

    def set_robot(self, robot: AbstractRobot) -> bool:
        self.rename(robot.get_name() + " " + self.FRAME_NAME)
        return True
