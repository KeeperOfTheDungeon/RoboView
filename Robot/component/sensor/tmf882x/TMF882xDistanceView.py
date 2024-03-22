from RoboControl.Robot.Component.Sensor.DistanceSensor import DistanceSensor
from RoboControl.Robot.Component.Sensor.TMF882x import TMF882xDistanceSensor
from RoboView.Robot.component.sensor.generic.distance.view.DistanceSensorDataView import DistanceSensorDataView
from RoboView.Robot.component.view.MissingComponentView import MissingComponentView


class TMF882xDistanceView(DistanceSensorDataView):

    def __init__(self, root, sensor, settings_key):
        super().__init__(root, sensor, settings_key)

    @staticmethod
    def create_view(root, distance_sensor: TMF882xDistanceSensor, settings_key):
        if distance_sensor is None:
            return MissingComponentView(DistanceSensor.__name__)
        return TMF882xDistanceView(root, distance_sensor, settings_key)
