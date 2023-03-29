
from tkinter import Label
from RoboControl.Robot.Component.generic.distance.DistanceSensor import DistanceSensor
from RoboView.Robot.component.view.MissingComponentView import MissingComponentView
from RoboView.Robot.component.view.SensorDataView import SensorDataView
from RoboView.Robot.Viewer.RobotSettings import RobotSettings


class DistanceSensorDataView(SensorDataView):

    def __init__(self, root, sensor, settings_key):
        super().__init__(root, sensor, settings_key, 100, 30)
        self._value_label = Label(self._data_frame, text="")
        
        self._value_label.place(x=10, y=5,  width=80, height=15)
        self._value = self._sensor.get_distance_value()
        self._value.add_listener(self.update)
        self.update()

    def build_context_menue(self):
        super().build_context_menue()
        self._context_menue.add_command(
            label="refresh distance", command=self.on_refresh)

    def create_view(root, distance_sensor, settings_key):

        if distance_sensor is not None:
            view = DistanceSensorDataView(root, distance_sensor, settings_key)
        else:
            view = MissingComponentView(DistanceSensor.__name__)

        return view

    def update(self):

        if self._value.is_valid():
            string = str(self._value.get_value())
            string += " mm"
        else:
            string = "- mm"

        self._value_label['text'] = string
        self._value_label.bind("<Button-1>", self.mouse_pressed_sensor)
        self._value_label.bind("<ButtonRelease-1>", self.mouse_released_value_label)
        self._value_label.bind("<Leave>", self.mouse_released_value_label)
        

    def on_refresh(self):
        self._sensor.remote_get_distance()
        
    def mouse_pressed_sensor(self, event):
        self.mouse_pressed(event)
        self._value_label.bind("<Motion>", self.mouse_motion)

    def mouse_released_value_label(self, event):
        self._value_label.unbind("<Motion>")


"""
package de.hska.lat.robot.component.generic.distance.view;

import java.awt.Insets;


import de.hska.lat.robot.component.ComponentChangeNotifier;
import de.hska.lat.robot.component.generic.distance.DistanceSensor;

import de.hska.lat.robot.component.view.ComponentView;
import de.hska.lat.robot.component.view.MissingComponentView;
import de.hska.lat.robot.component.view.SensorDataView;
import de.hska.lat.robot.value.view.ValueView;


public class DistanceSensorDataView  extends SensorDataView<DistanceSensor<?,?>> implements ComponentChangeNotifier
{

	
	protected static final int width = 95;
	protected static final int height = 35;
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 6397689382576347950L;

	
	
	
	
public DistanceSensorDataView(DistanceSensor<?,?> sensor)
{
	super(sensor);
	

	this.buildView();
}

@Override
protected int getViewWidth()
{
	return(DistanceSensorDataView.width);
}

@Override
protected int getViewHeight()
{
	return(DistanceSensorDataView.height);
}




	
public void buildView()
{
	super.buildView();
	ValueView<?> view;
	
	
	Insets insets = this.getBorder().getBorderInsets(this);
	
	
	
	view= DistanceValueView.createView(this.sensor.getDistanceValue(),true );
	view.setLocation(insets.left, insets.top);
	this.add(view);

}
	
	



public static ComponentView createView(DistanceSensor<?,?> sensor)
{

	if (sensor!=null)
	{
		return(new DistanceSensorDataView(sensor));
	}
	else
	{
		return(new MissingComponentView(DistanceSensor.class.getName()));
	}
}


}
"""
