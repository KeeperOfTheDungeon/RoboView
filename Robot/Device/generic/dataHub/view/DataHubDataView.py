from RoboView.Robot.Device.Viewer.DeviceView import DeviceView


class DataHubDataView(DeviceView):
    def __init__(self, device, window_bar):
        super().__init__("Main Data Hub", device, window_bar)



"""package de.hska.lat.robot.device.generic.dataHub.view;

import de.hska.lat.robot.abstractRobot.AbstractRobot;
import de.hska.lat.robot.component.text.Text;
import de.hska.lat.robot.component.text.view.TextDataView;
import de.hska.lat.robot.device.generic.dataHub.DataHub;
import de.hska.lat.robot.device.viewer.DeviceView;


public class DataHubDataView extends DeviceView
{




/**
	 * 
	 */
	private static final long serialVersionUID = 4664000212248415096L;


@Override
public boolean setRobot(AbstractRobot<?,?,?> robot)
{
	DataHub dataHub;

	dataHub = (DataHub)robot.getDeviceOnId(DataHub.ID);
			
	if (dataHub!=null)
	{
		makeDisplay(robot.getName(), dataHub);
		return(true);
	}
	else
	{
		makeErrorDisplay(DataHub.class.getName());
		return(false);
	}
	
}



public void makeDisplay(String robotName, DataHub dataHub)
{
	setDevice(robotName, dataHub);
	
	
	for (Text text: dataHub.getTexts())
	{
		this.addComponent(TextDataView.createView(text));	
	}
	
	//TextDataView
	
}	

}
"""
