import tkinter as tk
from tkinter.font import Font
from typing import Optional

import customtkinter as ctk

from RoboControl.Com.PacketLogger.DataPacketLogger import DataPacketLogger
from RoboControl.Com.PacketLogger.LoggedDataPacket import DisplayDataWidth_e, DisplayFormat_e
from RoboView.Robot.Ui.utils.colors import Color


class PacketLoggerToolbar(ctk.CTkFrame):
    HEIGHT = 80

    def __init__(self, master, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)
        # TODO why does this have a title?
        # self.rename("Toolbar")
        self.listener: Optional[DataPacketLogger] = None

        self._data_width = tk.Variable(master, value=DisplayDataWidth_e.WIDTH_8)
        self._display_format = tk.Variable(master, value=DisplayFormat_e.DECIMAL)

    @staticmethod
    def make_panel(panel: ctk.CTkFrame) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(panel, border_color=Color.DARK_GRAY, border_width=1,
                             height=PacketLoggerToolbar.HEIGHT - 10)
        frame.grid_configure(padx=(5, 5), pady=(5, 5), ipady=5, ipadx=5)
        frame.grid_rowconfigure(0, pad=10)
        frame.grid_columnconfigure(0, pad=10)
        return frame

    @staticmethod
    def make_button(panel: ctk.CTkFrame, text: str) -> ctk.CTkButton:
        button_width = 50
        button_height = 20
        return ctk.CTkButton(panel, text=text, state="normal", width=button_width, height=button_height)

    def add_control_panel(self) -> ctk.CTkFrame:
        control_panel = self.make_panel(self)
        ctk.CTkLabel(control_panel, text="Control: ").grid(column=0, row=0)

        record_button = self.make_button(control_panel, "record")
        record_button.grid(row=1, column=0)

        stop_button = self.make_button(control_panel, "stop")
        stop_button.configure(state="disabled")
        stop_button.grid(row=1, column=1)

        if self.listener and self.listener.is_recording:
            record_button.configure(state="disabled")
            stop_button.configure(state="normal")

        clear_button = self.make_button(control_panel, "clear")
        clear_button.grid(row=1, column=2)

        def on_record(*_args):
            record_button.configure(state="disabled")
            stop_button.configure(state="normal")
            self.listener.is_recording = True

        def on_stop(*_args):
            record_button.configure(state="normal")
            stop_button.configure(state="disabled")
            self.listener.is_recording = False

        def on_clear(*_args):
            if self.listener is None:
                return
            self.listener.clear()

        record_button.configure(command=on_record)
        stop_button.configure(command=on_stop)
        clear_button.configure(command=on_clear)

        return control_panel

    def add_file_panel(self):
        file_panel = self.make_panel(self)
        ctk.CTkLabel(file_panel, text="File: ").grid(column=0, row=0)
        btn = self.make_button(file_panel, "save...")
        btn.grid(column=0, row=1)

        def on_file_select(*_args):
            if not self.listener:
                return
            self.listener.save_as()
        btn.configure(command=on_file_select)
        return file_panel

    def add_filter_panel(self):
        filter_panel = self.make_panel(self)
        ctk.CTkLabel(filter_panel, text="Filter: ").grid(column=0, row=0)
        btn = self.make_button(filter_panel, "edit...")
        # TODO implement
        btn.configure(state="disabled")
        btn.grid(column=0, row=1)

        def on_edit_click(*_args):
            # TODO ?
            # DataPacketFilterBlockConfigViewer(self.master).grid(...)
            raise ValueError("WIP")

        btn.configure(command=on_edit_click)
        return filter_panel

    def set_listener(self, listener: DataPacketLogger) -> None:
        self.listener = listener
        self.build_toolbar()
        self.update_format()

    def add_width_panel(self) -> [ctk.CTkFrame]:
        raw_panel = self.make_panel(self)
        ctk.CTkLabel(raw_panel, text="Width: ").grid(column=0, row=0)
        sizes = {
            "8": DisplayDataWidth_e.WIDTH_8,
            "16": DisplayDataWidth_e.WIDTH_16,
            "24": DisplayDataWidth_e.WIDTH_24,
            "32": DisplayDataWidth_e.WIDTH_32,
        }
        for index, text in enumerate(sizes):
            btn = ctk.CTkRadioButton(raw_panel, text=text, state="normal",
                                     variable=self._data_width, value=sizes[text], width=50)
            btn.grid(column=index, row=1)

            def on_size_selected(*_args):
                self.update_format()

            btn.configure(command=on_size_selected)
        return raw_panel

    def build_toolbar(self) -> None:
        self.grid_rowconfigure(0, weight=1)
        cursor = 0
        for panel in [
            self.add_control_panel(),
            self.add_width_panel(),
            self.add_format_panel(),
            self.add_file_panel(),
            self.add_filter_panel(),
        ]:
            panel.grid(row=0, column=cursor)
            cursor += 1
        self.grid_columnconfigure("all", weight=1)

        log_size = tk.StringVar(self)
        log_size.set(str(DataPacketLogger.DEFAULT_MAX_SIZE))
        log_size_spinner = tk.Spinbox(self, textvariable=log_size,
                                      from_=0, to=1000, increment=1,
                                      width=4, font=Font(family="Helvetica", size=20),
                                      )
        log_size_spinner.grid(row=0, column=cursor, padx=10, pady=10)

        def on_log_size_change(*_args) -> None:
            try:
                new_size = int(log_size.get())
            except ValueError:
                return  # Invalid input
            if self.listener:
                self.listener.max_size = new_size

        # FIXME if this is enabled, writing left to right loses the logs (1->10->100 etc...)
        # log_size.trace("w", callback=on_log_size_change)
        log_size_spinner.configure(command=on_log_size_change)
        log_size_spinner.bind("<Return>", on_log_size_change)

    def update_format(self):
        if self.listener is not None:
            self.listener.set_display_format(self._display_format.get())
            self.listener.set_data_width(self._data_width.get())

    def add_format_panel(self) -> ctk.CTkFrame:
        format_panel = self.make_panel(self)
        ctk.CTkLabel(format_panel, text="Format: ").grid(column=0, row=0)
        formats = {
            "dec": DisplayFormat_e.DECIMAL,
            "hex": DisplayFormat_e.HEXADECIMAL,
            "native": DisplayFormat_e.NATIVE,
            "native+": DisplayFormat_e.NATIVE_WITH_DESCRIPTION,
        }
        for index, text in enumerate(formats):
            btn = ctk.CTkRadioButton(format_panel, text=text, state="normal",
                                     variable=self._display_format, value=formats[text], width=70)
            btn.grid(column=index, row=1)

            def on_format_selected(*_args):
                self.update_format()

            btn.configure(command=on_format_selected)

        return format_panel
