from typing import List

import customtkinter as ctk

from RoboControl.Com.PacketLogger.filter.DataPacketFilter import DataPacketFilter
from RoboControl.Com.PacketLogger.filter.DataPacketFilterList import DataPacketFilterList
from RoboView.Robot.dataPacketLogger.viewer.FilterSelectorNotifier import FilterSelectorNotifier


class DataPacketFilterSelector(ctk.CTkComboBox):  # ItemListener
    def __init__(self, master, filters: DataPacketFilterList):
        raise ValueError("WIP DataPacketFilterSelector is not yet implemented")
        super().__init__(master)
        self._filters: DataPacketFilterList = filters
        self._selector_listeners: List[FilterSelectorNotifier] = []

        self.resize(200, 30)  # setPreferredSize
        self.add_item_listener(self)

    def fire_popup_menu_will_become_visible(self) -> None:
        self.remove_all_items()
        if self._filters is None:
            # self.add_item("-")
            return
        for filter in self._filters:
            self.add_item(filter)

    def add_selector_listener(self, listener: FilterSelectorNotifier) -> None:
        """
        "Add a listener for filter selection. This listener sends a notification when a Filter has been selected  "
        :param listener: "selection listener to be add to the notification list"
        :return:
        """
        self._selector_listeners.append(listener)

    def remove_selector_listener(self, listener: FilterSelectorNotifier) -> None:
        """
        "remove a selection listener"
        :param listener: selection listener to be removed from the notification list
        :return:
        """
        self._selector_listeners.remove(listener)

    def on_item_state_changed(self, event: "ItemEvent") -> None:
        if event.get_state_change() == ItemEvent.SELECTED:
            filter: DataPacketFilter = event.get_item()
            for notifier in self._selector_listeners:
                notifier.filter_selected(filter)
