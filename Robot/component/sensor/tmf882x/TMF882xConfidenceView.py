from tkinter import StringVar

from customtkinter import CTkLabel

from RoboControl.Robot.Component.Sensor.DistanceSensor import DistanceSensor
from RoboControl.Robot.Component.Sensor.TMF882x import TMF882xDistanceSensor
from RoboControl.Robot.Value.ComponentValue import ComponentValue
from RoboView.Robot.component.view.MissingComponentView import MissingComponentView
from RoboView.Robot.component.view.SensorDataView import SensorDataView


class TMF882xConfidenceView(SensorDataView):
    def __init__(self, root, sensor: TMF882xDistanceSensor, settings_key):
        super().__init__(root, sensor, settings_key, 100, 30)

        if isinstance(self._sensor, TMF882xDistanceSensor):
            self._value = self._sensor.get_distance_value()

            self._confidence_label_var = StringVar()
            self._confidence_label = CTkLabel(
                master=self._data_frame, textvariable=self._confidence_label_var, text="confidence", width=80, height=15,
            )
            self._confidence_label.place(x=10, y=5)

            self._confidence_value = self._sensor.get_confidence()
            self._value.add_listener(self)

        self.update()

    def build_context_menu(self):
        super().build_context_menu()
        self._context_menue.add_command(label="refresh confidence", command=self.on_refresh)

    @staticmethod
    def create_view(root, distance_sensor, settings_key):
        if distance_sensor is None:
            return MissingComponentView(DistanceSensor.__name__)
        return TMF882xConfidenceView(root, distance_sensor, settings_key)

    def component_value_changed(self, component_value: ComponentValue) -> None:
        res = str(component_value.get_value()) if component_value.is_valid() else "-"
        self._confidence_label_var.set(f"{res} confidence")
        if self._confidence_label.winfo_exists():
            self._confidence_label.bind("<Button-1>", self.mouse_pressed_sensor)
            self._confidence_label.bind("<ButtonRelease-1>", self.mouse_released_value_label)
            self._confidence_label.bind("<Leave>", self.mouse_released_value_label)

    def update(self):
        self.component_value_changed(self._value)

    def on_refresh(self):
        self._sensor.remote_get_distance()

    def mouse_pressed_sensor(self, event):
        self.mouse_pressed(event)
        self._confidence_label.bind("<Motion>", self.mouse_motion)

    def mouse_released_value_label(self, event):
        self._confidence_label.unbind("<Motion>")

