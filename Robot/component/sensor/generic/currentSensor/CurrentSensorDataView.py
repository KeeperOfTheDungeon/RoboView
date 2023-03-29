
from tkinter import Label
from RoboControl.Robot.Component.generic.distance.DistanceSensor import DistanceSensor
from RoboView.Robot.component.view.MissingComponentView import MissingComponentView
from RoboView.Robot.component.view.SensorDataView import SensorDataView


class CurrentSensorDataView(SensorDataView):

	def __init__(self, root, sensor, settings_key):
		super().__init__(root, sensor, settings_key, 100, 150)

		label = Label(self._data_frame, text="actual")
		label.place(x = 10, y = 5,  width=80, height=15)

		self._actual_label = Label(self._data_frame, text="")
		self._actual_label.place(x = 50, y = 5,  width=80, height=15)


		label = Label(self._data_frame, text="max")
		label.place(x = 10, y = 35,  width=80, height=15)

		self._max_label = Label(self._data_frame, text="")
		self._max_label.place(x = 50, y = 35,  width=80, height=15)


		label = Label(self._data_frame, text="total")
		label.place(x = 10, y = 65,  width=80, height=15)

		self._total_label = Label(self._data_frame, text="")
		self._total_label.place(x = 50, y = 65,  width=80, height=15)
		


		
		self._actual_value = self._sensor.get_actual_value()
		self._max_value = self._sensor.get_max_value()
		self._total_value = self._sensor.get_total_value()
		
		self._actual_value.add_listener(self.update_actual)
		self._max_value.add_listener(self.update_max)
		self._total_value.add_listener(self.update_total)
		
		self.update()



	def build_context_menue(self):
		super().build_context_menue()
		self._context_menue.add_command(label="refresh actual", command=self.on_refresh) 
		self._context_menue.add_command(label="refresh max", command=self.on_refresh_max) 
		self._context_menue.add_command(label="refresh total", command=self.on_refresh_total) 
		self._context_menue.add_separator()
		self._context_menue.add_command(label="reset max", command=self.on_reset_max) 
		self._context_menue.add_command(label="reset total", command=self.on_reset_total) 		
		self._context_menue.add_separator()


	def create_view(root, distance_sensor, settings_key):

		if distance_sensor is not None:
			view = CurrentSensorDataView(root, distance_sensor, settings_key)
		else: 
			view = MissingComponentView(DistanceSensor.__name__)

		return view

	def on_refresh(self):
		self._sensor.remote_get_current()


	def on_refresh_max(self):
		self._sensor.remote_get_max_current()

	def on_reset_max(self):
		self._sensor.remote_reset_max_current()

	def on_refresh_total(self):
		self._sensor.remote_get_total_current()

	def on_reset_total(self):
		self._sensor.remote_reset_total_current()



	def update(self):
		self.update_actual()
		self.update_max()
		self.update_total()



	def update_actual(self):
	
		if self._actual_value.is_valid():
			string = str(self._actual_value.get_value())
			string += " c"
		else:
			string = "-  c"

		self._actual_label['text'] = string
		

	def update_max(self):
	
		if self._max_value.is_valid():
			string = str(self._max_value.get_value())
			string += " c"
		else:
			string = "-  c"

		self._max_label['text'] = string
		

	def update_total(self):
	
		if self._total_value.is_valid():
			string = str(self._total_value.get_value())
			string += " c"
		else:
			string = "-  c"

		self._total_label['text'] = string
