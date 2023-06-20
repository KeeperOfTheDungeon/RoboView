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
from RoboView.Robot.dataPacketLogger.viewer.PacketLoggerToolbar import PacketLoggerToolbar


class DataPacketLogView(InternalWindow, DataPacketLoggerEvent):
    FRAME_NAME: str = "Packet Logger"

    COLUMN_WIDTH_KEY = ".columnWidth"
    STRING_CLEAR = "clear list"
    CMD_CLEAR = STRING_CLEAR

    def __init__(self, root: ctk.CTkFrame, window_bar: WindowBar):
        super().__init__(root, self.FRAME_NAME, window_bar)
        self.root = root

        self._robot: Optional[AbstractRobot] = None
        self._packet_logger: Optional[DataPacketLogger] = None
        self._table_model: Optional[DataPacketTableModel] = None
        self._toolbar: Optional[PacketLoggerToolbar] = None

        # TODO this should either go upstream or be deleted
        self._frame.configure(bg="white")
        self.table = self.build_view()
        self.recover_column_width()
        # this.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        # self.show_window()

    def build_view(self) -> ttk.Treeview:
        self.move(-10, -10)
        self.set_min_dimension(950, 200)

        main = ctk.CTkFrame(fg_color="transparent", master=self._frame)
        main.pack(fill="both", expand=True,
                  padx=(10, 20), pady=(30, 20),
                  ipadx=5, ipady=5)

        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=1)

        self._table_model = DataPacketTableModel()

        self._toolbar = PacketLoggerToolbar(main, on_dump=self._table_model.dump_csv)
        self._toolbar.grid_propagate(False)
        self._toolbar.configure(height=PacketLoggerToolbar.HEIGHT)  # setPreferredSize set_min_dimension
        self._toolbar.grid(row=0, sticky="nwe")

        form = ctk.CTkFrame(fg_color="transparent", master=main)
        form.grid(row=1, sticky="nsew", pady=10)

        table = ttk.Treeview(master=form,
                             columns=self._table_model.COLUMNS,
                             selectmode="extended", show="headings", padding=5)

        for column in self._table_model.COLUMNS:
            table.column(column, anchor="c", minwidth=100, width=100, stretch=False)
            table.heading(column, text=column)

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
        for index, column_name in enumerate(self._table_model.COLUMNS):
            key = self._settings_key + self.COLUMN_WIDTH_KEY + str(index)
            new_width = RobotSettings.get_int(key, 100)
            self.table.column(column_name, width=new_width)

    def save_column_width(self) -> None:
        for index, column_name in enumerate(self._table_model.COLUMNS):
            from rich import print
            print(self.table.column(column_name))
            old_width = self.table.column(column_name)["width"]
            key = self._settings_key + self.COLUMN_WIDTH_KEY + str(index)
            RobotSettings.set_key(key, int(old_width))
            RobotSettings.save_settings()

    def close(self, *args) -> None:
        self.save_column_width()
        # TODO do this better
        self.on_logger_change = lambda *x: x
        super().close(*args)

    def repaint(self) -> None:
        self.table.delete(*self.table.get_children())

        for row_index, _ in enumerate(self._packet_logger):
            row = []
            for column_index in range(0, self._table_model.get_column_count()):
                row.append(self._table_model.get_value_at(row_index, column_index))
            self.table.insert('', tk.END, values=row)

    def on_logger_change(self) -> None:
        self.repaint()  # self.table.revalidate(); self.table.repaint()

    def set_robot(self, robot: AbstractRobot) -> bool:
        self.rename(robot.get_name() + " " + self.FRAME_NAME)
        self._packet_logger = robot.get_data_packet_logger()
        self._table_model.set_packet_logger(self._packet_logger)
        self._table_model.set_device_list(robot.get_device_list())
        self._toolbar.set_listener(self._packet_logger)
        self._packet_logger.add_listener(self)

        self.repaint()
        return True
