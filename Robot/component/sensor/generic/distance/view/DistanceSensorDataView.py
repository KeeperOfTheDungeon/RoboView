from tkinter import StringVar

from customtkinter import CTkLabel

from RoboControl.Robot.Component.Sensor.DistanceSensor import DistanceSensor
from RoboControl.Robot.Value.ComponentValue import ComponentValue
from RoboView.Robot.component.view.MissingComponentView import MissingComponentView
from RoboView.Robot.component.view.SensorDataView import SensorDataView


class DistanceSensorDataView(SensorDataView):
    def __init__(self, root, sensor, settings_key):
        super().__init__(root, sensor, settings_key, 100, 30)

        self._value_label_var = StringVar()
        self._value_label = CTkLabel(
            master=self._data_frame, textvariable=self._value_label_var, text="mm", width=80, height=15,
        )
        self._value_label.place(x=10, y=5)

        self._value = self._sensor.get_distance_value()
        self._value.add_listener(self)
        self.update()

    def build_context_menue(self):
        super().build_context_menue()
        self._context_menue.add_command(label="refresh distance", command=self.on_refresh)

    @staticmethod
    def create_view(root, distance_sensor, settings_key):
        if distance_sensor is None:
            return MissingComponentView(DistanceSensor.__name__)
        return DistanceSensorDataView(root, distance_sensor, settings_key)

    def component_value_changed(self, component_value: ComponentValue) -> None:
        res = str(component_value.get_value()) if component_value.is_valid() else "-"
        self._value_label_var.set(f"{res} mm")
        if self._value_label.winfo_exists():
            self._value_label.bind("<Button-1>", self.mouse_pressed_sensor)
            self._value_label.bind("<ButtonRelease-1>", self.mouse_released_value_label)
            self._value_label.bind("<Leave>", self.mouse_released_value_label)

    def update(self):
        self.component_value_changed(self._value)

    def on_refresh(self):
        self._sensor.remote_get_distance()

    def mouse_pressed_sensor(self, event):
        self.mouse_pressed(event)
        self._value_label.bind("<Motion>", self.mouse_motion)

    def mouse_released_value_label(self, event):
        self._value_label.unbind("<Motion>")
