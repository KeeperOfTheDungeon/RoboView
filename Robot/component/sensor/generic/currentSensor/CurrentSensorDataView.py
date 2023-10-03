from customtkinter import CTkLabel
from RoboControl.Robot.Component.generic.distance.DistanceSensor import DistanceSensor
from RoboControl.Robot.Value.ComponentValue import ComponentValue
from RoboView.Robot.component.view.MissingComponentView import MissingComponentView
from RoboView.Robot.component.view.SensorDataView import SensorDataView


class CurrentSensorDataView(SensorDataView):

    def __init__(self, root, sensor, settings_key):
        super().__init__(root, sensor, settings_key, 150, 70)

        offset_x = 5
        offset_y = 5
        distance_x = 60
        distance_y = 20

        label = CTkLabel(master=self._data_frame, text="actual", width=80, height=15)
        label.place(x=offset_x, y=offset_y)

        self._actual_label = CTkLabel(self._data_frame, text="", width=80, height=15)
        self._actual_label.place(x=offset_x + distance_x, y=offset_y)

        label = CTkLabel(self._data_frame, text="max", width=80, height=15)
        label.place(x=offset_x, y=offset_y + distance_y)

        self._max_label = CTkLabel(self._data_frame, text="", width=80, height=15)
        self._max_label.place(x=offset_x + distance_x, y=offset_y + distance_y)

        label = CTkLabel(self._data_frame, text="total", width=80, height=15)
        label.place(x=offset_x, y=offset_y + (distance_y * 2))

        self._total_label = CTkLabel(self._data_frame, text="", width=80, height=15)
        self._total_label.place(x=offset_x + distance_x, y=offset_y + (distance_y * 2))

        self._actual_value = self._sensor.get_actual_value()
        self._max_value = self._sensor.get_max_value()
        self._total_value = self._sensor.get_total_value()

        self._actual_value.add_listener(self)
        self._max_value.add_listener(self)
        self._total_value.add_listener(self)

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

    @staticmethod
    def create_view(root, distance_sensor, settings_key):
        if distance_sensor is None:
            return MissingComponentView(DistanceSensor.__name__)
        return CurrentSensorDataView(root, distance_sensor, settings_key)

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

    def component_value_changed(self, component_value: ComponentValue):
        value = str(component_value.get_value()) if component_value.is_valid() else "-"
        if component_value == self._actual_value:
            self._actual_label.configure(text=f"{value}  c")
        elif component_value == self._max_value:
            self._max_label.configure(text=f"{value}  c")
        elif component_value == self._total_value:
            self._total_label.configure(text=f"{value}  c")

    def update(self):
        self.component_value_changed(self._actual_value)
        self.component_value_changed(self._max_value)
        self.component_value_changed(self._total_value)
