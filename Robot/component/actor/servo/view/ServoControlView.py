from tkinter import HORIZONTAL, W, BooleanVar, Checkbutton, Label, Scale
from RoboControl.Robot.Component.generic.distance.DistanceSensor import DistanceSensor
from RoboControl.Robot.Math.Radiant import Radiant
from RoboView.Robot.component.view.AktorControlView import ActorControlView
from RoboView.Robot.component.view.MissingComponentView import MissingComponentView



class ServoControlView(ActorControlView):

	def __init__(self, root, servo, settings_key):
		super().__init__(root, servo, settings_key, 210, 100)
		#self._value_label = Label(self._data_frame, text="0°", font=("Courier", 12))
		#self._value_label.place(x = 1, y = 2,  width=80, height=15)


		self._position_slider = Scale(self._data_frame, from_=-100, to=100, orient=HORIZONTAL,command=self.changePosition)
		self._position_slider.place(x = 5, y = 50,  width=200, height=40)


		self._state = BooleanVar()
		self._on_button = Checkbutton(self._data_frame, text="on", variable=self._state, command=self.changeStatus)
		self._on_button.place(x = 5, y = 20,  width=40, height=20)
	





	def create_view(root, servo, settings_key):

		if servo is not None:
			view = ServoControlView(root, servo, settings_key)
		else: 
			view = MissingComponentView(DistanceSensor.__name__)

		return view




	def changeStatus(self):

		if self._state.get():
			self._actor.remote_servo_on()
		else:
			self._actor.remote_servo_off()


	def changePosition(self, position):
		position = float(position)
		position = Radiant.convert_degree_to_radiant(position)
		self._actor.remote_move_servo_to(position)



"""


import java.awt.Insets;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JCheckBox;
import javax.swing.JLabel;
import javax.swing.JSlider;
import javax.swing.JSpinner;
import javax.swing.SwingConstants;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

import de.hska.lat.math.Radiant;
import de.hska.lat.robot.component.RobotComponent;
import de.hska.lat.robot.component.actor.servo.Servo;
import de.hska.lat.robot.component.actor.servo.ServoChangeNotifier;
import de.hska.lat.robot.component.actor.servo.ServoSetupChangeNotifier;
import de.hska.lat.robot.component.view.ComponentView;
import de.hska.lat.robot.component.view.MissingComponentView;



public class ServoControlView extends ComponentView  implements ServoChangeNotifier, ServoSetupChangeNotifier, ChangeListener, ActionListener
{

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	
	
	private static final String CMD_ACTIVE	="cmdActive";
	
	
	private static final String STEP_STRING = "step width";
	
	private JSlider slider;

	
	private JLabel minPos;
	private JLabel maxPos;
	private JLabel actualPosition;
	private JCheckBox onCheckBox;
	
	private JSpinner stepSize;
	private StepWidthNumberModel stepWidth;
	private int position;
	
//	protected ServoControlInterface servoListener;
	protected Servo servo;
	
	protected static final int width = 280;
	protected static final int height = 80;
	
public ServoControlView(Servo servo) 
{
	super(servo.getComponentName(), false);
	
	this.servo = servo;
	
	servo.addSensorListener(this);
	servo.addSetupListener(this);
	
	buildView();

}


@Override
protected void buildView()
{
	
	
	super.buildView();

	
	Insets insets = this.getBorder().getBorderInsets(this);
	
	
	slider=new JSlider();
	slider = new JSlider(); 
	slider.setBounds(insets.left+55,insets.top+25,182,30);
	slider.setMaximum(0);
	slider.setMinimum(0);
	slider.setValue(0);
	slider.setMajorTickSpacing(30);
	slider.setMinorTickSpacing(10);
	slider.setPaintTicks(true); 
	slider.addChangeListener(this);
	add(slider);

	
	actualPosition=new JLabel("-�");
	actualPosition.setBounds(insets.left+117,insets.top+05,40,20);
	actualPosition.setHorizontalAlignment(SwingConstants.CENTER);
	add(actualPosition);
	
	
	minPos=new JLabel("0�");
	minPos.setBounds(insets.left+5,insets.top+35,40,20);
	minPos.setHorizontalAlignment(SwingConstants.CENTER);
	add(minPos);

	
	maxPos=new JLabel("0�");
	maxPos.setBounds(insets.left+240,insets.top+35,40,20);
	maxPos.setHorizontalAlignment(SwingConstants.CENTER);
	add(maxPos);
	
	
	onCheckBox=new JCheckBox("On");
	onCheckBox.setBounds(insets.left+5, insets.top+55, 80, 20);
	onCheckBox.setSelected(false);
	onCheckBox.setActionCommand(CMD_ACTIVE);
	onCheckBox.addActionListener(this);
	add(onCheckBox);
	
	
	
	
	
	JLabel tmpLabel = new JLabel(STEP_STRING);
	tmpLabel.setBounds(insets.left+100, insets.top+55, 80, 25);
	add(tmpLabel);
	

	stepWidth = new StepWidthNumberModel();
	
	stepSize = new JSpinner(stepWidth);
	stepSize.setBounds(insets.left+160, insets.top+55, 100, 25);
	stepSize.addChangeListener(this);
	add(stepSize);
	
	
	this.updateValues(servo);

}


@Override
protected int getViewWidth()
{
	return(ServoControlView.width);
}

@Override
protected int getViewHeight()
{
	return(ServoControlView.height);
}


private void updatePosition(int position)
{
	this.position=position;
	actualPosition.setText(String.valueOf(position)+"�");
}





protected void updateValues(Servo servo)
{
	int min = (int)Radiant.convertRadiantToDegree(servo.getMinRange());
	int max = (int)Radiant.convertRadiantToDegree(servo.getMaxRange());

	
	this.minPos.setText(min+"�");
	this.slider.setMinimum(min);
	
	this.maxPos.setText(max+"�");
	this.slider.setMaximum(max);
	
	this.stepWidth.setIndex(this.servo.getSpeed());

}

/**
 * creates new servo control view and link it given servo 
 * @param servo servo to be connected with created view
 * @return a new servo control view
 */

public static ComponentView createView(Servo servo)
{
	if (servo!=null)
	{
		return(new ServoControlView(servo));
	}
	else
	{
		return(new MissingComponentView(Servo.class.getName()));
	}
}



@Override
public void actionPerformed(ActionEvent actionEvent) 
{

	String cmd;
	
	cmd=actionEvent.getActionCommand();
	
	 if (cmd.equals(CMD_ACTIVE))
	{
		 if (onCheckBox.isSelected())
		 {
			 this.servo.remote_servoOn();
		 }
		 else
		 {
			 this.servo.remote_servoOff();
		 }
		 
	}
	 else
		{
			super.actionPerformed(actionEvent);
		}
}



@Override
public void stateChanged(ChangeEvent event) 
{
	if (event.getSource()==slider)
	{
		
		if (this.slider.hasFocus()==true) 
		{
			if (this.position!=slider.getValue())
			{
				updatePosition(slider.getValue());
				this.servo.remote_moveTo(Radiant.convertDegreeToRadiant(slider.getValue()));
			}	
		}
	}
	else if (event.getSource()==stepSize)
	{
		if (stepWidth.hasChanged())
		{
			this.servo.remote_setServoSpeed(stepWidth.getIndex());
		}
		
	}
}



@Override
public void servoPositionChanged(Servo servo) 
{
	// TODO Auto-generated method stub
	
}





@Override
public void isActive(Servo servo)
{
	// Not of your concern -> ignore
	
}



@Override
public void isStalling(Servo servo) 
{
	// Not of your concern -> ignore
	
}


/*
@Override
public void servoSpeedChanged(int servo, int speed) 
{
	// TODO Auto-generated method stub
	
}
*/

/*
@Override
public void servoOffsetChanged(int servo, int offset)
{
	// Not of your concern -> ignore
}

*/
/*
@Override
public void servoMaxRangeChanged(int servo, float maxRange) 
{
	maxPos.setText(FloatValue.toFormatedFractionString(maxRange, 2)+"�");
	slider.setMaximum((int)maxRange);
	
}
*/

/*
@Override
public void servoMinRangeChanged(int servo, float minRange) 
{

	minPos.setText(FloatValue.toFormatedFractionString(minRange, 2)+"�");
	slider.setMinimum((int)minRange);

}

*/

@Override
public void isOn(Servo servo) 
{
	onCheckBox.setSelected(servo.isOn());
	
}

/*

@Override
public void inverse(int globalId, boolean status)
{
	// TODO Auto-generated method stub
	
}

*/

@Override
public void servoSetupChanged(Servo servo)
{
	this.updateValues(servo);

	
}

@Override
public void servoSpeedChanged(int globalId, int speed) 
{
	this.stepWidth.setIndex(speed);
}


@Override
public void settingsChanged(RobotComponent<?, ?, ?> component)
{
	// TODO Auto-generated method stub
	
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


@Override
public void servoForceThresholdChanged(int globalId, int threshold)
{
	// TODO Auto-generated method stub
	
}


@Override
public void servoForcePositionChanged(int globalId, int threshold)
{
	// TODO Auto-generated method stub
	
}


@Override
public void isAtMin(Servo servo)
{
	// TODO Auto-generated method stub
	
}


@Override
public void isAtMax(Servo servo)
{
	// TODO Auto-generated method stub
	
}

}
"""