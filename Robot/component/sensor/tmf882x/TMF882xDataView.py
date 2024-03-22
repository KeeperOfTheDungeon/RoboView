from RoboControl.Robot.Component.Sensor.TMF882x import TMF882x
from RoboView.Robot.Device.Viewer.DeviceView import DeviceView
from RoboView.Robot.component.sensor.generic.distance.view.DistanceSensorDataView import DistanceSensorDataView
from RoboView.Robot.component.sensor.tmf882x.TMF882xConfidenceView import TMF882xConfidenceView


class TMF882xDataView:

    def __init__(self, head_sensors: list[TMF882x], data_view: DeviceView):
        x_cursor, y_cursor = 20, 20
        row_count = 0
        for (sensor) in head_sensors:
            for s in sensor.get_distance_sensors():
                distance_view = DistanceSensorDataView.create_view(data_view._display, s, data_view._settings_key)
                confidence_view = TMF882xConfidenceView.create_view(data_view._display, s, data_view._settings_key)
                data_view.add_component(distance_view, x_cursor, y_cursor)
                view_width, view_height = distance_view.get_frame().winfo_reqwidth(), distance_view.get_frame().winfo_reqheight()
                data_view.add_component(confidence_view, x_cursor, y_cursor + view_height)
                confidence_view_width, confidence_view_height = confidence_view.get_frame().winfo_reqwidth(), confidence_view.get_frame().winfo_reqheight()
                view_width += confidence_view_width
                view_height += confidence_view_height
                if row_count < 2:
                    x_cursor += view_width + 10
                    row_count += 1
                else:
                    x_cursor = 20
                    y_cursor += view_height + 10
                    row_count = 0