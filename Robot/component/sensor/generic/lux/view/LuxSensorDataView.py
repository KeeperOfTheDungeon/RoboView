
from tkinter import Label
import customtkinter as ctk
from RoboControl.Robot.Component.generic.distance.DistanceSensor import DistanceSensor
from RoboView.Robot.component.view.MissingComponentView import MissingComponentView
from RoboView.Robot.component.view.SensorDataView import SensorDataView


class LuxSensorDataView(SensorDataView):

    def __init__(self, root, sensor, settings_key):
        super().__init__(root, sensor, settings_key, 100, 30)

        self._value_label = Label(self._data_frame, text="")
        self._value_label.place(x=10, y=5,  width=80, height=15)
        self._value = self._sensor.get_lux_value()
        self._value.add_listener(self.update)
        self.update()

    def build_context_menue(self):
        super().build_context_menue()
        self._context_menue.add_command(
            label="refresh lux", command=self.on_refresh)

    def create_view(root, distance_sensor, settings_key):

        if distance_sensor is not None:
            view = LuxSensorDataView(root, distance_sensor, settings_key)
        else:
            view = MissingComponentView(DistanceSensor.__name__)

        return view

    def on_refresh(self):
        self._sensor.remote_get_value()

    def update(self):

        if self._value.is_valid():
            string = str(self._value.get_value())
            string += " lux"
        else:
            string = "-  lux"

        self._value_label['text'] = string
        self._value_label.bind("<Button-1>", self.mouse_pressed_sensor)
        self._value_label.bind("<ButtonRelease-1>",
                               self.mouse_released_value_label)
        self._value_label.bind("<Leave>", self.mouse_released_value_label)

    def mouse_pressed_sensor(self, event):
        self.mouse_pressed(event)
        self._value_label.bind("<Motion>", self.mouse_motion)

    def mouse_released_value_label(self, event):
        self._value_label.unbind("<Motion>")
