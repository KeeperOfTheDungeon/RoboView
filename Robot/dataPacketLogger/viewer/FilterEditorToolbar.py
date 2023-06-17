import customtkinter as ctk

from RoboControl.Com.PacketLogger.filter.DataPacketFilter import DataPacketFilter
from RoboControl.Com.PacketLogger.filter.DataPacketFilterList import DataPacketFilterList
from RoboView.Robot.dataPacketLogger.viewer.DataPacketFilterSelector import DataPacketFilterSelector
from RoboView.Robot.dataPacketLogger.viewer.FilterSelectorNotifier import FilterSelectorNotifier


class FilterEditorToolbar(ctk.CTkOptionMenu):
    _filter_selector: DataPacketFilterSelector

    LOAD_TEXT = "load"
    SAVE_TEXT = "save"
    NEW_TEXT = "new"

    def __init__(self):
        raise ValueError("WIP FilterEditorToolbar is not yet implemented")
        self.rename("Toolbar")
        self.resize(400, 40)  # setPreferredSize
        self.build_toolbar()

        _load_button: ctk.CTkButton = None
        _save_button: ctk.CTkButton = None
        _new_button: ctk.CTkButton = None

    def build_toolbar(self) -> None:
        self._new_button = ctk.CTkButton(self, text=FilterEditorToolbar.NEW_TEXT)

        def on_action_performed(*_args):
            # PacketLoggerToolBar.this.getDesktopPane().add(new DataPacketFilterBlockConfigViewer());
            # PacketLoggerToolBar.this.getParent().add(new DataPacketFilterBlockConfigViewer());
            pass

        # self._new_button.add_action_listener(on_action_performed)

        self._load_button = ctk.CTkButton(self, text=FilterEditorToolbar.LOAD_TEXT)
        # TODO on_action_performed ?
        # self._load_button.add_action_listener(on_action_performed)

        self._save_button = ctk.CTkButton(self, text=FilterEditorToolbar.SAVE_TEXT)
        # TODO on_action_performed ?
        # self._save_button.add_action_listener(on_action_performed)

        filters = DataPacketFilterList()
        f1 = DataPacketFilter()
        f1.set_name("f1")
        filters.add(f1)

        f2 = DataPacketFilter()
        f2.set_name("f1")
        filters.add(f2)

        self._filter_selector = DataPacketFilterSelector(self, filters)
        self._filter_selector.resize(200, 30)  # setPreferredSize

    def set_selector_listener(self, listener: FilterSelectorNotifier) -> None:
        self._filter_selector.add_selector_listener(listener)
