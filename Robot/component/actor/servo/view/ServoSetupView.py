from email.utils import decode_rfc2231
from tkinter import HORIZONTAL, BooleanVar, Checkbutton, Label, Scale, Spinbox, StringVar
from RoboControl.Robot.Component.generic.distance.DistanceSensor import DistanceSensor
from RoboControl.Robot.Math.Radiant import Radiant

from RoboView.Robot.component.view.ComponentSetupView import ComponentSetupView
from RoboView.Robot.component.view.MissingComponentView import MissingComponentView


class ServoSetupView(ComponentSetupView):

    def __init__(self, root, servo, settings_key):
        super().__init__(root, servo, settings_key, 310, 200)

        self._position_slider = Scale(
            self._data_frame, from_=-100, to=100, orient=HORIZONTAL, command=self.changePosition)
        self._position_slider.place(x=50, y=10,  width=200, height=40)

        min_pos_var = StringVar()
        min_pos_var.set("0")

        self._min_Pos = Spinbox(self._frame, from_=-90, to=90, increment=1,
                                textvariable=min_pos_var, width=10, command=self.changePosition)
        self._min_Pos.place(x=5, y=30,  width=40, height=20)

        max_pos_var = StringVar()
        max_pos_var.set("0")

        self._max_Pos = Spinbox(
            self._frame, from_=-90, to=90, increment=1, textvariable=max_pos_var, width=10)
        self._max_Pos.place(x=260, y=30,  width=40, height=20)

        self._state = BooleanVar()
        self._on_button = Checkbutton(
            self._data_frame, text="on", variable=self._state, command=self.changeStatus)
        self._on_button.place(x=5, y=70,  width=40, height=20)

        self._state = BooleanVar()
        self._on_button = Checkbutton(
            self._data_frame, text="reverse", variable=self._state, command=self.changeStatus)
        self._on_button.place(x=55, y=70,  width=60, height=20)

        offset_var = StringVar()
        offset_var.set("0")

        label = Label(self._data_frame, text="offset")
        label.place(x=160, y=70,  width=80, height=15)

        self._offset = Spinbox(
            self._frame, from_=0, to=10000, increment=1, textvariable=offset_var, width=10)
        self._offset.place(x=240, y=70,  width=60, height=20)

        offset_var = StringVar()
        offset_var.set("0")

        label = Label(self._data_frame, text="scale")
        label.place(x=160, y=90,  width=80, height=15)

        self._scale = Spinbox(self._frame, from_=0, to=20000,
                              increment=1, textvariable=offset_var, width=10)
        self._scale.place(x=240, y=90,  width=60, height=20)

        offset_var = StringVar()
        offset_var.set("0")

        label = Label(self._data_frame, text="speed")
        label.place(x=160, y=110,  width=80, height=15)

        self._speed = Spinbox(self._frame, from_=0, to=52,
                              increment=0.28, textvariable=offset_var, width=10)
        self._speed.place(x=240, y=110,  width=60, height=20)


# self._device.remote_start_stream(index, int(int(self._period.get())/10))


    def build_context_menue(self):
        super().build_context_menue()
        self._context_menue.add_command(
            label="set settings", command=self.on_set_settings)

    def create_view(root, servo, settings_key):

        if servo is not None:
            view = ServoSetupView(root, servo, settings_key)
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

    def on_set_settings(self):
        pass


"""package de.hska.lat.robot.component.servo.view;



import java.awt.Insets;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JLabel;
import javax.swing.JSlider;
import javax.swing.JSpinner;
import javax.swing.SpinnerNumberModel;
import javax.swing.SwingConstants;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

import de.hska.lat.math.Radiant;
import de.hska.lat.robot.component.RobotComponent;
import de.hska.lat.robot.component.actor.servo.Servo;
import de.hska.lat.robot.component.actor.servo.ServoChangeNotifier;
import de.hska.lat.robot.component.actor.servo.ServoSetupChangeNotifier;
import de.hska.lat.robot.component.view.ComponentSettingsView;
import de.hska.lat.robot.component.view.ComponentView;
import de.hska.lat.robot.component.view.MissingComponentView;


import javax.swing.JProgressBar;


public class ServoSetupView extends ComponentSettingsView<Servo>  implements ChangeListener, ActionListener, ServoChangeNotifier, ServoSetupChangeNotifier{


	/**
	 * 
	 */
	private static final long serialVersionUID = 49462972340295156L;
	private JSlider slider;
	private JLabel actualPosition;
	
	private JCheckBox forceFeedbackCheckBox;
	private JSpinner forceFeedbackSpinner;
	private SpinnerNumberModel forceFeedbackSpinnerModel;
	
	private JCheckBox positionFeedbackCheckBox;
	private JSpinner positionFeedbackSpinner;
	private SpinnerNumberModel positionFeedbackSpinnerModel;

	private JSpinner maxRange;
	private JSpinner minRange;
//	private JSpinner offset;
	
	private JCheckBox onCheckBox;
	private JCheckBox reverseCheckBox;
	
	private static final String CMD_ON	="cmdOn";
	private static final String CMD_FORCEFEEDBACK_ON	="cmdForceFeedOn";
	private static final String CMD_POSITIONFEEDBACK_ON	="cmdPosFeedOn";
	
	protected SpinnerNumberModel minSpinerModel ;
	protected SpinnerNumberModel maxSpinerModel ;
	protected SpinnerNumberModel offsetSpinerModel;
	protected SpinnerNumberModel scaleSpinerModel;
	
	
	protected JProgressBar servoPosition;
	
	private JSpinner speed;
	private StepWidthNumberModel speedSpinerModel;
	
	protected JButton calibrate;

	
	private float position;
	
	
	protected static final int width = 340;
	protected static final int height = 220;
	
	
private ServoSetupView(Servo servo) 
{
	super(servo);
	
	
	buildView();
	
	servo.addSensorListener(this);
	servo.addSetupListener(this);
	

	
	

}


@Override
protected void buildView()
{
	
	super.buildView();

	
	Insets insets = this.getBorder().getBorderInsets(this);
	
	JLabel tmpLabel;

	
	tmpLabel=new JLabel("position");
	tmpLabel.setBounds(insets.left+5,insets.top+12,40,20);
	this.add(tmpLabel);
	
	this.actualPosition=new JLabel("0�");
	this.actualPosition.setBounds(insets.left+48,insets.top+10,29,25);
	this.actualPosition.setHorizontalAlignment(SwingConstants.CENTER);
	this.add(this.actualPosition);
	
	this.slider = new JSlider(); 
	this.slider.setBounds(insets.left+70,insets.top+25,182,30);
	this.slider.setMaximum(90);
	this.slider.setMinimum(-90);
	this.slider.setValue(0);
	this.slider.setMajorTickSpacing(30);
	this.slider.setMinorTickSpacing(10);
	this.slider.setPaintTicks(true); 
	this.slider.addChangeListener(this);
	this.add(this.slider);
	
	this.servoPosition = new JProgressBar();
	this.servoPosition.setBounds(insets.left+70, insets.top+10, 182, 16);
	add(this.servoPosition);
	
	
	this.minSpinerModel = new SpinnerNumberModel(0,-90,90,1 );
	this.maxSpinerModel = new SpinnerNumberModel(0, -90,90, 1);
	
	this.minRange= new JSpinner(this.minSpinerModel);
	this.minRange.setBounds(insets.left+5,insets.top+30,60,25);
	this.minRange.addChangeListener(this);
	this.add(this.minRange);
	
	this.maxRange= new JSpinner(this.maxSpinerModel);
	this.maxRange.setBounds(insets.left+260,insets.top+30,60,25);
	this.maxRange.addChangeListener(this);
	this.add(this.maxRange);
	 

	
	this.onCheckBox=new JCheckBox("On");
	this.onCheckBox.setBounds(insets.left+5, insets.top+55, 80, 20);
	this.onCheckBox.setSelected(false);
	this.onCheckBox.setActionCommand(CMD_ON);
	this.onCheckBox.addActionListener(this);
	this.add(this.onCheckBox);
	
	this.reverseCheckBox=new JCheckBox("Reverse");
	this.reverseCheckBox.setBounds(insets.left+85, insets.top+55, 80, 20);
	this.reverseCheckBox.setSelected(false);
//	reverseCheckBox(BCMD_DRAV_DIRECT);
	this.reverseCheckBox.addActionListener(this);
	this.add(this.reverseCheckBox);
	
	
	tmpLabel= new JLabel("offset");
	tmpLabel.setBounds(insets.left+203, insets.top+53, 50, 25);
	this.add(tmpLabel);
	 
	JSpinner tmpSpinner;
	
	this.offsetSpinerModel = new SpinnerNumberModel(750, 300, 10000, 1);

	tmpSpinner= new JSpinner(this.offsetSpinerModel);
	tmpSpinner.setBounds(insets.left+260, insets.top+55, 60, 25);
	tmpSpinner.addChangeListener(this);
	this.add(tmpSpinner);
	
	
	
	tmpLabel= new JLabel("scale");
	tmpLabel.setBounds(insets.left+203, insets.top+80, 40, 25);
	this.add(tmpLabel);
	 
	
	this.scaleSpinerModel = new SpinnerNumberModel(15707, 10000, 20000, 1);

	tmpSpinner= new JSpinner(this.scaleSpinerModel);
	tmpSpinner.setBounds(insets.left+250, insets.top+80, 70, 25);
	tmpSpinner.addChangeListener(this);
	this.add(tmpSpinner);
	
	this.addSetButton(insets.left+5, insets.top+80, 50, 22);
	this.addGetButton(insets.left+5, insets.top+105, 50, 22);
	
	this.addSaveButton(insets.left+58, insets.top+80, 50, 22);
	this.addLoadButton(insets.left+58, insets.top+105, 50, 22);
	

	
	
	tmpLabel= new JLabel("speed");
	tmpLabel.setBounds(insets.left+203, insets.top+105, 40, 25);
	this.add(tmpLabel);
	 
	
	this.speedSpinerModel = new StepWidthNumberModel();
	
	this.speed = new JSpinner(speedSpinerModel);
	this.speed.setBounds(insets.left+240, insets.top+105, 80, 25);
	this.speed.addChangeListener(this);
	add(this.speed);
	
	
	tmpLabel=new JLabel("Force Feedback:");
	tmpLabel.setBounds(insets.left,insets.top+135,110,30);
	this.add(tmpLabel);
	
	this.forceFeedbackCheckBox=new JCheckBox("");
	this.forceFeedbackCheckBox.setBounds(insets.left+110, insets.top+140, 20, 20);
	this.forceFeedbackCheckBox.setSelected(false);
	this.forceFeedbackCheckBox.setActionCommand(CMD_FORCEFEEDBACK_ON);
	this.forceFeedbackCheckBox.addActionListener(this);
	this.add(this.forceFeedbackCheckBox);
	
	/*
	this.forceFeedbackSpinner = new JSlider(JSlider.HORIZONTAL, 0, 100, 0); //public JSlider(int orientation, int min, int max, int value)
	this.forceFeedbackSpinner.setBounds(insets.left+130,insets.top+140,165,40);
	this.forceFeedbackSpinner.setMajorTickSpacing(20);
	this.forceFeedbackSpinner.setMinorTickSpacing(10);
	this.forceFeedbackSpinner.setPaintLabels(true);
	this.forceFeedbackSpinner.setPaintTicks(true); 
	this.forceFeedbackSpinner.addChangeListener(this);
	this.add(this.forceFeedbackSpinner);
	*/
	this.forceFeedbackSpinnerModel = new SpinnerNumberModel();	
	this.forceFeedbackSpinner = new JSpinner(forceFeedbackSpinnerModel);
	this.forceFeedbackSpinner.setBounds(insets.left+130, insets.top+140, 80, 25);
	this.forceFeedbackSpinner.addChangeListener(this);
	add(this.forceFeedbackSpinner);
	this.forceFeedbackSpinner.setValue(30);
	
	tmpLabel=new JLabel("Position Feedback:");
	tmpLabel.setBounds(insets.left,insets.top+190,110,20);
	this.add(tmpLabel);
	
	this.positionFeedbackCheckBox=new JCheckBox("");
	this.positionFeedbackCheckBox.setBounds(insets.left+110, insets.top+190, 20, 20);
	this.positionFeedbackCheckBox.setSelected(false);
	this.positionFeedbackCheckBox.setActionCommand(CMD_POSITIONFEEDBACK_ON);
	this.positionFeedbackCheckBox.addActionListener(this);
	this.add(this.positionFeedbackCheckBox);
	
	this.positionFeedbackSpinnerModel = new SpinnerNumberModel();
	this.positionFeedbackSpinner = new JSpinner(positionFeedbackSpinnerModel);
	this.positionFeedbackSpinner.setBounds(insets.left+130, insets.top+190, 80, 25);
	this.positionFeedbackSpinner.addChangeListener(this);
	add(this.positionFeedbackSpinner);
	this.positionFeedbackSpinner.setValue(500);
	
	
	this.calibrate = new JButton("calibrate");
	this.calibrate.setBounds(insets.left+210, insets.top+190, 80, 20);
	this.calibrate.addActionListener(new ActionListener()
	{

		@Override
		public void actionPerformed(ActionEvent arg0)
		{
			ServoSetupView.this.component.remote_calibrate();
		}
		
	});
	this.add(this.calibrate);

	
	
	
	this.updateValues(this.component);
}



@Override
protected int getViewWidth()
{
	return(ServoSetupView.width);
}

@Override
protected int getViewHeight()
{
	return(ServoSetupView.height);
}


private void updatePosition(float position)
{
	this.position=position;
	this.actualPosition.setText(String.valueOf(position)+"�");
}



protected void updateValues(Servo servo)
{
	int min = (int)Radiant.convertRadiantToDegree(servo.getMinRange());
	int max = (int)Radiant.convertRadiantToDegree(servo.getMaxRange());


	
	this.minSpinerModel.setValue(min);
	this.maxSpinerModel.setValue(max);
	this.offsetSpinerModel.setValue((int)servo.getOffset());
	this.scaleSpinerModel.setValue((int)servo.getScale());
	
	this.servoPosition.setMinimum((int)Radiant.convertRadiantToDegree(min));
	this.servoPosition.setMaximum((int)Radiant.convertRadiantToDegree(max));
	
	this.speedSpinerModel.setIndex(servo.getSpeed());
}


/**
 * creates new servo setup view and link it given servo 
 * @param servo servo to be connected with created view
 * @return a new servo setup view
 */

public static ComponentView createView(Servo servo)
{

	if (servo!=null)
	{
		return(new ServoSetupView(servo));
	}
	else
	{
		return(new MissingComponentView(Servo.class.getName()));
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
				this.updatePosition(slider.getValue());
				this.component.remote_setServoPosition(Radiant.convertDegreeToRadiant(slider.getValue()));
			}	
		}

	}
	
	else if (event.getSource()==minRange)
		{
		this.maxSpinerModel.setMinimum((Comparable<?>) minSpinerModel.getNumber());
		this.slider.setMinimum( (Integer) minSpinerModel.getNumber());
		}
	
	else if (event.getSource()==maxRange)
		{
		this.minSpinerModel.setMaximum((Comparable<?>) maxSpinerModel.getNumber());
		this.slider.setMaximum( (Integer) maxSpinerModel.getNumber());
		}
	else if (event.getSource()==speed)
	{
		if (speedSpinerModel.hasChanged())
		{
			this.component.remote_setServoSpeed(speedSpinerModel.getIndex());
		}
		
	} else if (event.getSource()==forceFeedbackSpinner)
	{
		
			this.component.remote_setServoForceThreshold(forceFeedbackSpinnerModel.getNumber().intValue());
	}else if (event.getSource()==positionFeedbackSpinner)
	{
		
		this.component.remote_setServoForcePosition(positionFeedbackSpinnerModel.getNumber().intValue());
}
}


@Override
protected boolean setSettings()
{
	
	int minRange = this. minSpinerModel.getNumber().intValue();
	int maxRange = this.maxSpinerModel.getNumber().intValue();
	int offset =  this.offsetSpinerModel.getNumber().intValue();
	int scale =  this.scaleSpinerModel.getNumber().intValue();
	boolean inverse = this.reverseCheckBox.isSelected();

	return(this.component.remote_setServoDefaults(Radiant.convertDegreeToRadiant(minRange),
			Radiant.convertDegreeToRadiant(maxRange),
			offset,
			scale,
			inverse));
}



@Override
public void actionPerformed(ActionEvent actionEvent) 
{
	String cmd;
	
	super.actionPerformed(actionEvent);
	
	cmd=actionEvent.getActionCommand();
	
	if (cmd.equals(CMD_ON))
	{
		 if (onCheckBox.isSelected())
		 {
			 this.component.remote_servoOn();
		 }
		 else
		 {
			 this.component.remote_servoOff();
		 }
		 
	}else if (cmd.equals(CMD_FORCEFEEDBACK_ON)){
		 if (forceFeedbackCheckBox.isSelected())
		 {
			 this.component.remote_forceFeedbackOn();
		 }
		 else
		 {
			 this.component.remote_forceFeedbackOff();
		 }
		
	}else if (cmd.equals(CMD_POSITIONFEEDBACK_ON)){
		 if (positionFeedbackCheckBox.isSelected())
		 {
			 this.component.remote_positionFeedbackOn();
		 }
		 else
		 {
			 this.component.remote_positionFeedbackOff();
		 }
	}

}



@Override
public void servoPositionChanged(Servo servo) 
{
	this.actualPosition.setText(String.valueOf(servo.getPositionAsDegree())+"�");
	
	this.servoPosition.setValue((int)servo.getPositionAsDegree());
	
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

@Override
public void servoSpeedChanged(int globalId, int speed)
{
	this.speedSpinerModel.setIndex(speed);
}


@Override
public void isOn(Servo servo) 
{
	this.onCheckBox.setSelected(servo.isOn());
	
}

@Override
public void forceFeedbackOn(Servo servo){
	this.forceFeedbackCheckBox.setSelected(servo.forceFeedbackisOn());
}



@Override
public void servoSetupChanged(Servo servo)
{
	this.updateValues(servo);
}


@Override
public void settingsChanged(RobotComponent<?, ?, ?> component)
{
	// TODO Auto-generated method stub
	
}


@Override
public void positionFeedbackOn(Servo servo)
{
	this.positionFeedbackCheckBox.setSelected(servo.positionFeedbackisOn());
	
}


@Override
public void servoForceThresholdChanged(int globalId, int threshold)
{
	this.forceFeedbackSpinner.setValue(threshold);
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
