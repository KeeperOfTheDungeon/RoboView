# disabled for micropython  # from typing import Optional

import customtkinter as ctk
from tkinter import ttk

from RoboControl.Robot.AbstractRobot.AbstractRobot import AbstractRobot
from RoboView.Gui.InternalWindow.InternalWindow import InternalWindow
from RoboView.Robot.Viewer.WindowBar import WindowBar
from RoboView.Robot.dataPacketLogger.viewer.FilterEditorToolbar import FilterEditorToolbar
from RoboView.Robot.dataPacketLogger.viewer.FilterRuleTableModel import FilterRuleTableModel


class DataPacketFilterEditor(InternalWindow):
    FRAME_NAME: str = "Data packet filter editor"

    def __init__(self, root: ctk.CTkFrame, window_bar: WindowBar):
        super().__init__(root, self.FRAME_NAME, window_bar)
        self.root = root

        # TODO this should either go upstream or be deleted
        self._frame.configure(bg="white")

        self._robot: "Optional[AbstractRobot]" = None
        self._table_model: "Optional[FilterRuleTableModel]" = None
        self._toolbar: "Optional[FilterEditorToolbar]" = None

        self.table: ttk.Treeview = self.build_view()
        self._toolbar.load_filter()

    def build_view(self) -> ttk.Treeview:
        self.move(-10, -10)
        self.set_min_dimension(800, 300)

        main = ctk.CTkFrame(fg_color="transparent", master=self._frame)
        main.pack(fill="both", expand=True,
                  padx=(10, 20), pady=(30, 20),
                  ipadx=5, ipady=5)

        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=1)

        self._table_model = FilterRuleTableModel()
        self._table_model.add_listener(self)

        self._toolbar = FilterEditorToolbar(main, table_model=self._table_model)
        self._toolbar.grid_propagate(False)
        self._toolbar.configure(height=FilterEditorToolbar.HEIGHT)
        self._toolbar.grid(column=0, row=0, sticky="nwe")

        form = ctk.CTkFrame(fg_color="transparent", master=main)
        form.grid(column=0, row=1, sticky="nsew", pady=10)

        table = self._table_model.as_treeview(form)

        table.grid(column=0, row=0, sticky="nsew")
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

        return table

    def set_robot(self, robot: AbstractRobot) -> bool:
        self.rename(robot.get_name() + " " + self.FRAME_NAME)
        self._table_model.set_logger(robot.get_data_packet_logger())
        return True

    def on_change(self) -> None:
        self._table_model.paint_on_table(self.table)
