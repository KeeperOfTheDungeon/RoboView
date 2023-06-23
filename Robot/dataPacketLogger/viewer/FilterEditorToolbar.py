import customtkinter as ctk

from RoboControl.Com.PacketLogger.filter.DataPacketFilter import DataPacketFilter
from RoboView.Robot.Ui.utils.colors import Color
from RoboView.Robot.dataPacketLogger.viewer.FilterRuleTableModel import FilterRuleTableModel


class FilterEditorToolbar(ctk.CTkFrame):
    HEIGHT = 50

    def __init__(self, master, *args, table_model: FilterRuleTableModel = None, **kwargs):
        super().__init__(master, *args, **kwargs)
        # TODO why does this have a title?
        # self.rename("Toolbar")
        self._table_model = table_model

        self._active_filter = ctk.StringVar()
        self._active_filter.set(DataPacketFilter.ALLOW_ALL)

        self.build_toolbar()

    @staticmethod
    def make_panel(panel: ctk.CTkFrame) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(panel, border_color=Color.DARK_GRAY, border_width=1,
                             height=FilterEditorToolbar.HEIGHT - 2)
        frame.grid_configure(padx=(5, 5), pady=(5, 5))
        frame.grid_rowconfigure(0, pad=5)
        frame.grid_columnconfigure(0, pad=5)
        return frame

    @staticmethod
    def make_button(panel: ctk.CTkFrame, text: str) -> ctk.CTkButton:
        button_width = 50
        button_height = 20
        return ctk.CTkButton(panel, text=text, state="normal", width=button_width, height=button_height)

    def add_control_panel(self) -> ctk.CTkFrame:
        control_panel = self.make_panel(self)
        new_button = self.make_button(control_panel, "new")
        new_button.grid(row=0, column=0)
        new_button.configure(state="disabled")
        load_button = self.make_button(control_panel, "load")
        load_button.configure(state="disabled")
        load_button.grid(row=0, column=1)
        save_button = self.make_button(control_panel, "save")
        save_button.configure(state="disabled")
        save_button.grid(row=0, column=2)

        def on_new(*_args):
            pass

        def on_load(*_args):
            pass

        def on_save(*_args):
            pass

        new_button.configure(command=on_new)
        load_button.configure(command=on_load)
        save_button.configure(command=on_save)

        return control_panel

    def build_toolbar(self) -> None:
        self.grid_rowconfigure(0, weight=1)
        values = [f.name for f in self._table_model.all_filters]
        selector = ctk.CTkComboBox(self, values=values, variable=self._active_filter)
        selector.grid(row=0, column=0)
        self.add_control_panel().grid(column=1, row=0)

        def on_selected(*_args):
            self.load_filter()

        selector.configure(command=on_selected)
        selector.grid(row=0, column=4)

    def load_filter(self):
        data_filter = self._table_model.get_filter_by_name(self._active_filter.get())
        self._table_model.load_filter(data_filter)
