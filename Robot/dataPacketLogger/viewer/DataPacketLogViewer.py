from tkinter import ttk
# disabled for micropython  # from typing import Optional

import customtkinter as ctk

from RoboControl.Com.PacketLogger.DataPacketLogger import DataPacketLogger
from RoboControl.Robot.AbstractRobot.AbstractRobot import AbstractRobot
from RoboView.Gui.InternalWindow.InternalWindow import InternalWindow
from RoboView.Robot.Viewer.RobotSettings import RobotSettings
from RoboView.Robot.Viewer.WindowBar import WindowBar
from RoboView.Robot.dataPacketLogger.viewer.PacketLoggerToolbar import PacketLoggerToolbar


class DataPacketLogView(InternalWindow):
    FRAME_NAME: str = "Packet Logger"

    COLUMN_WIDTH_KEY = ".columnWidth"
    STRING_CLEAR = "clear list"
    CMD_CLEAR = STRING_CLEAR

    def __init__(self, root: ctk.CTkFrame, window_bar: WindowBar):
        super().__init__(root, self.FRAME_NAME, window_bar)
        self.root = root

        self._robot: "Optional[AbstractRobot]" = None
        self._packet_logger: "Optional[DataPacketLogger]" = None
        self._toolbar: "Optional[PacketLoggerToolbar]" = None

        # TODO this should either go upstream or be deleted
        self._frame.configure(bg="white")
        self.table = self.build_view()
        self.recover_column_width()
        # this.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        # self.show_window()

    def build_view(self) -> ttk.Treeview:
        self.move(-10, -10)
        self.set_min_dimension(1300, 400)

        main = ctk.CTkFrame(fg_color="transparent", master=self._frame)
        main.pack(fill="both", expand=True,
                  padx=(10, 20), pady=(30, 20),
                  ipadx=5, ipady=5)

        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=1)

        self._packet_logger = DataPacketLogger()  # dummy logger

        self._toolbar = PacketLoggerToolbar(main)
        self._toolbar.grid_propagate(False)
        self._toolbar.configure(height=PacketLoggerToolbar.HEIGHT)
        self._toolbar.grid(row=0, sticky="nwe")

        form = ctk.CTkFrame(fg_color="transparent", master=main)
        form.grid(row=1, sticky="nsew", pady=10)

        table = self._packet_logger.as_treeview(form)

        table.grid(row=0, column=0, sticky="nsew")
        form.grid_rowconfigure(0, weight=1)
        form.grid_columnconfigure(0, weight=1)

        ysb = ctk.CTkScrollbar(master=form, command=table.yview,
                               orientation="vertical", width=15, )
        ysb.grid(row=0, column=1, sticky="nse")
        table.configure(yscrollcommand=ysb.set)

        xsb = ctk.CTkScrollbar(master=form, command=table.xview,
                               orientation="horizontal", height=15, )
        xsb.grid(row=1, column=0, columnspan=2, sticky="sew")
        table.configure(xscrollcommand=xsb.set)
        # table.bind('<Motion>', 'break')

        # self._table_model.fill_with_examples(table)
        return table

    def recover_column_width(self) -> None:
        for index, column_name in enumerate(self._packet_logger.column_names):
            key = self._settings_key + self.COLUMN_WIDTH_KEY + str(index)
            new_width = RobotSettings.get_int(key, 100)
            self.table.column(column_name, width=new_width)

    def save_column_width(self) -> None:
        for index, column_name in enumerate(self._packet_logger.column_names):
            from rich import print
            print(self.table.column(column_name))
            old_width = self.table.column(column_name)["width"]
            key = self._settings_key + self.COLUMN_WIDTH_KEY + str(index)
            RobotSettings.set_key(key, int(old_width))
            RobotSettings.save_settings()

    def close(self, *args) -> None:
        self.save_column_width()
        super().close(*args)

    def on_change(self) -> None:
        if self.table.winfo_exists():
            self._packet_logger.paint_on_table(self.table)

    def set_robot(self, robot: AbstractRobot) -> bool:
        self.rename(robot.get_name() + " " + self.FRAME_NAME)
        self._packet_logger = robot.get_data_packet_logger()
        self._toolbar.set_listener(self._packet_logger)
        self._packet_logger.add_listener(self)
        self.on_change()
        return True
