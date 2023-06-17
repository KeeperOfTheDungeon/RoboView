from typing import List, Optional

from tkinter import ttk
import tkinter as tk

from RoboControl.Com.Connection import Connection
from RoboControl.Com.PacketLogger.DataPacketLogger import DataPacketLogger
from RoboControl.Com.PacketLogger.LoggedDataPacket import LoggedDataPacket, DisplayFormat_e
from RoboControl.Robot.AbstractRobot.AbstractRobotDevice import AbstractRobotDevice


class DataPacketTableModel:
    COLUMNS = ["nr", "timestamp", "type", "direction", "destination", "source", "name", "data"]
    _data_packet_logger: DataPacketLogger
    _device_list: List[AbstractRobotDevice]

    def __init__(self):
        # TODO "load data_width" from where?
        pass

    def set_packet_logger(self, packet_logger: DataPacketLogger) -> None:
        self._data_packet_logger = packet_logger

    def set_device_list(self, device_list: List[AbstractRobotDevice]) -> None:
        self._device_list = device_list

    def get_column_name(self, column: int) -> str:
        raise ValueError("WIP")  # return(COLUMNS_NAME [column])

    def get_column_count(self) -> int:
        return len(self.COLUMNS)

    def get_row_count(self) -> int:
        return len(self._data_packet_logger)

    def set_size(self, new_size: int) -> None:
        self._data_packet_logger.set_max_size(new_size)

    def get_value_at(self, row: int, column: int) -> Optional[object]:
        try:
            if self._data_packet_logger is None:
                return "----"
            row: LoggedDataPacket = self._data_packet_logger[row]
            if column == 0:
                return int(row.get_number())
            elif column == 1:
                return row.get_timestamp().isoformat(sep=' ', timespec='milliseconds')
            elif column == 2:
                return row.get_type_name()
            elif column == 3:
                return row.get_direction_as_string()
            elif column == 4:
                device_id = row.get_destination()
                # TODO use actual connection id
                if Connection.REMOTE_CHANEL_ID == device_id:
                    return "Connection"
                else:
                    return self._device_list[device_id].get_name()
            elif column == 5:
                device_id = row.get_source()
                # TODO use actual connection id
                if Connection.REMOTE_CHANEL_ID == device_id:
                    return "Connection"
                else:
                    return self._device_list[device_id].get_name()
            elif column == 6:
                return row.get_command_name() + " (" + str(row.get_command()) + ")"
            elif column == 7:
                data_width = self._data_packet_logger.get_standard_data_width()
                data_format = self._data_packet_logger.get_standard_display_format()
                if data_format == DisplayFormat_e.DECIMAL:
                    return row.get_data_as_string(data_width, False)
                elif data_format == DisplayFormat_e.HEXADECIMAL:
                    return row.get_data_as_string(data_width, True)
                elif data_format == DisplayFormat_e.NATIVE:
                    return row.get_parameters_as_string(False)
                elif data_format == DisplayFormat_e.NATIVE_WITH_DESCRIPTION:
                    return row.get_parameters_as_string(True)
                return row.get_data_as_string(data_width, False)
        except Exception as e:
            raise e
        return None

    def get_as_native(self) -> str:
        raise ValueError("WIP")

    def fill_with_examples(self, table: ttk.Treeview) -> None:
        # generate sample data
        examples = []
        for n in range(1, 100):
            examples.append([f"{n}{i}" for i in range(0, len(self.COLUMNS))])
        for example in examples:
            table.insert('', tk.END, values=example)

    # def get_as_raw(self, row: int):
    #     row: LoggedDataPacket = self._data_packet_logger[row]
    #     return row.get_data_as_string(self.data_width, False)
