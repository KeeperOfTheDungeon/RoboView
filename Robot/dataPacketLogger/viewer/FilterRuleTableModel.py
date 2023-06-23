from RoboControl.Com.PacketLogger.DataPacketLogger import DataPacketLogger
from RoboControl.Com.PacketLogger.filter.DataPacketFilter import DataPacketFilter


class FilterRuleTableModel(DataPacketLogger):
    def __init__(self):
        super().__init__()
        self._data_packet_logger = None

    def set_logger(self, data_packet_logger: DataPacketLogger):
        self._data_packet_logger = data_packet_logger

    def load_filter(self, packet_filter: DataPacketFilter):
        if self._data_packet_logger:
            self._data_packet_logger.filter = packet_filter
        self.is_recording = True
        self.clear()
        for rule in packet_filter.get_rules():
            tag = "green" if rule.is_pass else "red"
            values = []
            for column_name in self.column_names:
                values.append(rule.as_dict().get(column_name))
            self.add_row(values, tags=[tag])
