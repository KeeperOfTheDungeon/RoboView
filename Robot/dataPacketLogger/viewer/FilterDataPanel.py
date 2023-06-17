import tkinter as tk
import customtkinter as ctk

from RoboControl.Com.PacketLogger.filter.DataPacketFilter import DataPacketFilter
from RoboView.Robot.dataPacketLogger.viewer.FilterSelectorNotifier import FilterSelectorNotifier


class FilterDataPanel(tk.Frame, FilterSelectorNotifier):
    FILTER_NAME_TEXT = "filter name"

    _filter_name: ctk.CTkTextbox  # JTextField
    _description: ctk.CTkTextbox  # JTextArea
    _filter: DataPacketFilter

    def __init__(self):
        raise ValueError("WIP FilterDataPanel is not yet implemented")
        super().__init__()
        # self.set_border(LineBorder(Color.BLACK))
        self.build_panel()

    def build_panel(self) -> None:
        # self.set_layout(None)
        tmp_label = ctk.CTkLabel(FilterDataPanel.FILTER_NAME_TEXT)
        tmp_label.set_bounds(10, 10, 100, 25)
        self.add(tmp_label)

        self.resize(300, 100)  # setPreferredSize

        self._filter_name = ctk.CTkTextbox(self, )
        self._filter_name.set_bounds(110, 10, 300, 25)

        self._description = ctk.CTkTextbox(self, )
        self._description.set_bounds(110, 40, 300, 60)

        tmp_button = ctk.CTkButton(self, text="new block")

        # tmp_button.set_bounds(10, 40, 100, 40)

        def on_action_performed(*_args):
            if self._filter is not None:
                self._filter.add_filter_block()

    # self.add_action_listener(on_action_performed)

    def edit_filter(self, edited_filter: DataPacketFilter) -> None:
        if self._filter is not None:
            self._filter_name.set_text(edited_filter.get_name())

    def filter_selected(self, selected_filter: DataPacketFilter) -> None:
        self.edit_filter(selected_filter)
