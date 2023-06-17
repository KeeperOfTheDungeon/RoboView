import customtkinter as ctk

from RoboView.Robot.Ui.utils.colors import Color
from RoboView.Robot.dataPacketLogger.viewer.FilterRuleTableModel import FilterRuleTableModel


class FilterEditorPanel(ctk.CTkFrame):
	def __init__(self):
		raise ValueError("WIP FilterEditorPanel is not yet implemented")
		super().__init__(border_color=Color.BLACK)
		self.build_panel()

	def build_panel(self) -> None:
		self.resize(900, 100)  # setPreferredSize
		rules_table = JTable(FilterRuleTableModel())
		self.set_viewport_view(rules_table)

		# FIXME what?
		sport_column = rules_table.get_column_model().get_column(1)
		combobox: JComboBox[String] = JComboBox()

		for example in ["Snowboarding", "Rowing", "Chasing toddlers", "Speed reading", "Teaching high school", "None"]:
			combobox.add_item(example)

		sport_column.set_cell_editor(DefaultCellEditor(comboBox))
