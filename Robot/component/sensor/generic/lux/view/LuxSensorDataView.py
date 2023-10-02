from customtkinter import CTkLabel
from RoboControl.Robot.Component.generic.distance.DistanceSensor import DistanceSensor
from RoboView.Robot.component.view.MissingComponentView import MissingComponentView
from RoboView.Robot.component.view.SensorDataView import SensorDataView


class LuxSensorDataView(SensorDataView):
    def __init__(self, root, sensor, settings_key):
        super().__init__(root, sensor, settings_key, 100, 30)

        self._value_label = CTkLabel(
            master=self._data_frame, text="lux", width=80, height=15,
        )
        self._value_label.place(x=10, y=5)

        self._value = self._sensor.get_lux_value()
        self._value.add_listener(self.update)
        self.update()

    def build_context_menue(self):
        super().build_context_menue()
        self._context_menue.add_command(label="refresh lux", command=self.on_refresh)

    @staticmethod
    def create_view(root, distance_sensor, settings_key):
        if distance_sensor is None:
            return MissingComponentView(DistanceSensor.__name__)
        return LuxSensorDataView(root, distance_sensor, settings_key)

    def on_refresh(self):
        self._sensor.remote_get_value()

    def update(self):
        if not self._value_label.winfo_exists():
            return
        res = str(self._value.get_value()) if self._value.is_valid() else "-"
        self._value_label.configure(text=f"{res} lux")
        self._value_label.bind("<Button-1>", self.mouse_pressed_sensor)
        self._value_label.bind("<ButtonRelease-1>", self.mouse_released_value_label)
        self._value_label.bind("<Leave>", self.mouse_released_value_label)

    def mouse_pressed_sensor(self, event):
        self.mouse_pressed(event)
        self._value_label.bind("<Motion>", self.mouse_motion)

    def mouse_released_value_label(self, event):
        self._value_label.unbind("<Motion>")
