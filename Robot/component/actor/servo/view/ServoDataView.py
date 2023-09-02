from tkinter import Label
from RoboControl.Robot.Component.generic.distance.DistanceSensor import DistanceSensor
from RoboView.Robot.component.view.MissingComponentView import MissingComponentView
from RoboView.Robot.component.view.SensorDataView import SensorDataView


class ServoDataView(SensorDataView):

    def __init__(self, root, servo, settings_key):
        super().__init__(root, servo, settings_key, width=100, height=20)
        self._value_label = Label(self._data_frame, text="", font=("Courier", 12))
        self._value_label.place(x=10, y=2, width=80, height=15)

        self._value = self._sensor.get_position_value()
        self._value.add_listener(self.servo_position_changed)

    @staticmethod
    def create_view(root, servo, settings_key):
        if servo is not None:
            view = ServoDataView(root, servo, settings_key)
        else:
            view = MissingComponentView(DistanceSensor.__name__)
        return view

    def servo_position_changed(self):
        if self._value.is_valid():
            string = "{:.1f}".format(self._value.get_value_as_degree())
            # str()
            string += " °"
        else:
            string = "- °"
        self._value_label['text'] = string


"""
package de.hska.lat.robot.component.servo.view;




import java.awt.Color;
import java.awt.Insets;

import javax.swing.JCheckBox;
import javax.swing.JLabel;
import javax.swing.SwingConstants;
import javax.swing.border.LineBorder;

import de.hska.lat.robot.component.actor.servo.Servo;
import de.hska.lat.robot.component.actor.servo.ServoChangeNotifier;
import de.hska.lat.robot.component.view.ComponentView;
import de.hska.lat.robot.value.view.MissingValueView;




public class ServoDataView extends ComponentView  implements ServoChangeNotifier
{

	
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 5165802217514053434L;
	
	
	private JLabel positionLabel;
	private JCheckBox atMinFlag;
	private JCheckBox atMaxFlag;
	private JCheckBox isOnFlag;
	private JCheckBox activeFlag;
	private JCheckBox inverseFlag;
	private JCheckBox stallFlag;


	protected static final int width = 160;
	protected static final int height = 90;
	
	
public ServoDataView(Servo servo) 
{
	super(servo.getComponentName(), false);
	
	servo.addSensorListener(this);
	buildView();


}




@Override
protected void buildView() 
{
	
	super.buildView();

	
	Insets insets = this.getBorder().getBorderInsets(this);
	
	
	JLabel tmpLabel;
	
	tmpLabel=new JLabel("position");
	tmpLabel.setBounds(insets.left+5,insets.top+5,50,20);
	this.add(tmpLabel);
	
	positionLabel=new JLabel("--");
	positionLabel.setHorizontalAlignment(SwingConstants.CENTER);
	positionLabel.setBorder(new LineBorder(Color.black));
	positionLabel.setBounds(insets.left+60,insets.top+5,40,20);
	this.add(positionLabel);
	
	
	
	this.atMinFlag= new JCheckBox("min");
	this.atMinFlag.setBounds(insets.left+5, insets.top+30,60,20);
	this.atMinFlag.setEnabled(false);
	this.add(this.atMinFlag);
	
	this.atMaxFlag= new JCheckBox("max");
	this.atMaxFlag.setBounds(insets.left+85, insets.top+30,60,20);
	this.atMaxFlag.setEnabled(false);
	this.add(this.atMaxFlag);

	
	this.activeFlag= new JCheckBox("active");
	this.activeFlag.setBounds(insets.left+5, insets.top+50,60,20);
	this.activeFlag.setEnabled(false);
	this.add(activeFlag);
	
	
	this.isOnFlag= new JCheckBox("on");
	this.isOnFlag.setBounds(insets.left+85, insets.top+50,60,20);
	this.isOnFlag.setEnabled(false);
	this.add(isOnFlag);

	
	inverseFlag= new JCheckBox("inverse");
	inverseFlag.setBounds(insets.left+5,  insets.top+70,70,20);
	inverseFlag.setEnabled(false);
	this.add(inverseFlag);
	
	
	this.stallFlag= new JCheckBox("stall");
	this.stallFlag.setBounds(insets.left+85,  insets.top+70,60,20);
	this.stallFlag.setEnabled(false);
	this.add(stallFlag);
	
}




@Override
protected int getViewWidth()
{
	return(ServoDataView.width);
}

@Override
protected int getViewHeight()
{
	return(ServoDataView.height);
}




protected void update(Servo servo)
{
	this.positionLabel.setText(servo.getPositionAsDegree()+"�");
	this.atMaxFlag.setSelected(servo.isAtMin());
	this.atMaxFlag.setSelected(servo.isAtMin());
	this.activeFlag.setSelected(servo.isActive());
	this.stallFlag.setSelected(servo.isStalling());
	this.isOnFlag.setSelected(servo.isOn());
}





@Override
public void servoPositionChanged(Servo servo)
{
	this.update(servo);


}



@Override
public void isActive(Servo servo)
{
	this.update(servo);

}



@Override
public void isAtMin(Servo servo)
{
	this.update(servo);
}




@Override
public void isAtMax(Servo servo)
{
	this.update(servo);
}



@Override
public void isStalling(Servo servo)
{
	this.update(servo);

}



@Override
public void isOn(Servo servo)
{
	this.isOnFlag.setSelected(servo.isOn());
	
}




@Override
public void forceFeedbackOn(Servo servo)
{
	// TODO Auto-generated method stub
	
}




@Override
public void positionFeedbackOn(Servo servo)
{
	// TODO Auto-generated method stub
	
}

/**
 * creates new servo data view and link it given servo 
 * @param servo servo to be connected with created view
 * @return a new servo data view
 */

public static ComponentView createView(Servo servo)
{

	if (servo!=null)
	{
		return(new ServoDataView(servo));
	}
	else
	{
		return(new MissingValueView(Servo.class.getName(), false));
	}
}







}
"""
