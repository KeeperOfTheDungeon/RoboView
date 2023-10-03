from RoboControl.Robot.AbstractRobot.AbstractListener import ComponentValueChangeListener
from RoboControl.Robot.Value.ComponentValue import ComponentValue
from RoboView.Robot.component.view.ComponentView import ComponentView


class SensorDataView(ComponentView, ComponentValueChangeListener):
    def __init__(self, root, sensor, settings_key, width, height):
        super().__init__(root, sensor.get_name(), settings_key, width, height)
        self._sensor = sensor
        # self._name = sensor.get_name()

    def component_value_changed(self, component_value: ComponentValue):
        raise ValueError("WIP SensorDataView.value_changed")

    # refresh fehlt
"""package de.hska.lat.robot.component.view;

import java.awt.event.ActionEvent;

import javax.swing.JSeparator;

import de.hska.lat.robot.component.sensor.Sensor;


public class SensorDataView<C extends Sensor<?,?,?>> extends ComponentView  
{


/**
	 * 
	 */
	private static final long serialVersionUID = -671723169597138383L;

	private static final String REFRESH_TEXT	= "refresh";
	private static final String CMD_REFRESH		= "cmdRefresh";
	
	protected C sensor;
	
	
public SensorDataView(C sensor)
{
	super(sensor.getComponentName(), false);
	
	this.sensor = sensor;
}



@Override
protected void makePopupMenu()
{
	super.makePopupMenu();

	this.contextMenue.add(new JSeparator());
	this.addMenuItem(this.contextMenue , SensorDataView.REFRESH_TEXT, SensorDataView.CMD_REFRESH);


}


@Override
public void actionPerformed(ActionEvent actionEvent)
{
	String cmd;
	
	cmd = actionEvent.getActionCommand();
	
	if (cmd.equals(SensorDataView.CMD_REFRESH))
	{
		this.sensor.remote_getValue();
	}	
	else
	{
		super.actionPerformed(actionEvent);
	}
	
	

}


}
"""
