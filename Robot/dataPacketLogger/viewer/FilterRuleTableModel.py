class FilterRuleTableModel:
    COLUMNS_NAME = ["nr", "timestamp", "type", "direction", "destination", "source", "name", "data"]

    def __init__(self):
        raise ValueError("WIP FilterRuleTableModel is not yet implemented")
        self._box: JComboBox[String] = JComboBox()

    def get_column_name(self, column: int) -> str:
        return self.COLUMNS_NAME[column]

    """
    def get_column_class(self, column: int) -> class:
        print("get class")
        return self._box.get_class()
    """

    def is_cell_editable(self, row_index: int, column_index: int) -> bool:
        # TODO ??
        return True

    def get_column_count(self) -> int:
        # FIXME ??
        return 3

    def get_row_count(self) -> int:
        # FIXME ??
        return 3

    def get_value_at(self, arg0: int, arg1: int) -> object:
        # FIXME ??
        raise ValueError("get_value_at for FilterRuleTableModel not yet implemented")
