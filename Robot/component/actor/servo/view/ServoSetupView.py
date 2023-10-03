from email.utils import decode_rfc2231
from tkinter import HORIZONTAL, BooleanVar, Checkbutton, Label, Scale, Spinbox, StringVar
import customtkinter as ctk

from RoboControl.Robot.AbstractRobot.AbstractListener import ServoSetupListener
from RoboControl.Robot.Component.Actor.servo.Servo import Servo
from RoboControl.Robot.Component.RobotComponent import RobotComponent
from RoboControl.Robot.Component.generic.distance.DistanceSensor import DistanceSensor
from RoboControl.Robot.Math.Radiant import Radiant

from RoboView.Robot.component.view.ComponentSetupView import ComponentSetupView
from RoboView.Robot.component.view.MissingComponentView import MissingComponentView


class ServoSetupView(ComponentSetupView, ServoSetupListener):
    CMD_ON	="cmdOn"
    CMD_FORCEFEEDBACK_ON	="cmdForceFeedOn"
    CMD_POSITIONFEEDBACK_ON	="cmdPosFeedOn"

    def __init__(self, root, servo: Servo, settings_key):
        super().__init__(root, servo, settings_key, 250, 120)
        self._actor: Servo = servo

        label_font = ctk.CTkFont(family="Arial", size=10)
        
        self._actual_position = ctk.CTkLabel(master=self._data_frame, text="?")
        self._position_slider = Scale(
            self._data_frame, from_=-100, to=100, orient=HORIZONTAL, command=self.update_position
        )
        self._position_slider.place(x=50, y=10, width=200, height=40)

        self._min_pos_var = StringVar()
        self._min_pos_var.set("0")
        self._min_Pos = Spinbox(
            self._data_frame, from_=-90, to=90, increment=1,
            textvariable=self._min_pos_var, width=10, command=self.update_position
        )
        self._min_Pos.place(x=5, y=30, width=40, height=20)

        self._max_pos_var = StringVar()
        self._max_pos_var.set("0")
        self._max_Pos = Spinbox(
            self._data_frame, from_=-90, to=90, increment=1, textvariable=self._max_pos_var, width=10)
        self._max_Pos.place(x=260, y=30, width=40, height=20)

        self._state = BooleanVar()
        self._on_button = Checkbutton(
            self._data_frame, text="on", variable=self._state, command=self.change_status
        )
        self._on_button.place(x=5, y=70, width=40, height=20)

        self._reverse_state = BooleanVar()
        self._reverse_button = Checkbutton(
            self._data_frame, text="reverse", variable=self._reverse_state, command=self.change_reverse_status
        )
        self._reverse_button.place(x=55, y=70, width=60, height=20)

        self._offset_var = StringVar()
        self._offset_var.set("0")
        label = ctk.CTkLabel(
            self._data_frame, text="offset",
            font=label_font, bg_color="transparent", width=80, height=15,
        )
        label.place(x=130, y=54)
        self._offset = Spinbox(
            self._data_frame, from_=0, to=10000, increment=1, textvariable=self._offset_var, width=10)
        self._offset.place(x=240, y=70, width=60, height=20)

        self._scale_var = StringVar()
        self._scale_var.set("0")
        label = ctk.CTkLabel(
            self._data_frame, text="scale",
            font=label_font, bg_color="transparent", width=80, height=15,
        )
        label.place(x=130, y=72)
        self._scale = Spinbox(self._data_frame, from_=0, to=20000,
                              increment=1, textvariable=self._scale_var, width=10)
        self._scale.place(x=240, y=90, width=60, height=20)

        self._speed_var = StringVar()
        self._speed_var.set("0")
        label = ctk.CTkLabel(
            self._data_frame, text="speed",
            font=label_font, bg_color="transparent", width=80, height=15,
        )
        label.place(x=130, y=90)
        self._speed = Spinbox(self._data_frame, from_=0, to=52,
                              increment=0.28, textvariable=self._speed_var, width=10)
        self._speed.place(x=240, y=110, width=60, height=20)

        # forceFeedbackCheckBox: CTkCheckbox
        # forceFeedbackSpinner: Spinbox
        # forceFeedbackSpinnerModel: SpinnerNumberModel

        # positionFeedbackCheckBox: CTkCheckbox
        # positionFeedbackSpinner: Spinbox
        # positionFeedbackSpinnerModel: SpinnerNumberModel

        # self._calibrate: CTkButton

        # self._actor.remote_start_stream(index, int(int(self._period.get())/10))

        servo.add_sensor_listener(self)
        servo.add_setup_listener(self)

    def build_context_menue(self):
        super().build_context_menue()
        self._context_menue.add_command(label="set settings", command=self.on_set_settings)

    @staticmethod
    def create_view(root, servo: Servo, settings_key):
        """ "creates new servo setup view and link it given servo" """
        if servo is None:
            return MissingComponentView(DistanceSensor.__name__)
        return ServoSetupView(root, servo, settings_key)

    def change_status(self) -> None:
        self._actor.remote_servo_on() if self._state.get() else self._actor.remote_servo_off()

    def change_reverse_status(self) -> None:
        raise ValueError("WIP")

    def update_position(self, position: str) -> None:
        position = float(position)
        position = Radiant.convert_degree_to_radiant(position)
        self._actor.remote_move_servo_to(position)
        self._actual_position.configure(text=f"{position:.2f}°")

    def update_values(self, servo: Servo) -> None:
        minimum = Radiant.convert_radiant_to_degree(servo.get_min_range())
        maximum = Radiant.convert_radiant_to_degree(servo.get_max_range())
        self._min_pos_var.set(str(minimum))
        self._max_pos_var.set(str(maximum))
        self._offset_var.set(str(servo.get_offset()))
        self._scale_var.set(str(servo.get_scale()))
        self._position_slider.configure(from_=minimum, to=maximum)
        self._speed_var.set(str(servo.get_speed()))

    def servo_setup_changed(self, servo: Servo) -> None:
        self.update_values(servo)

    def set_settings(self) -> bool:
        min_range = int(self._min_pos_var.get())
        max_range = int(self._max_pos_var.get())
        offset = int(self._offset_var.get())
        scale = int(self._scale_var.get())
        inverse = bool(self._reverse_state.get())
        return self._actor.remote_set_servo_defaults(
            Radiant.convert_degree_to_radiant(min_range),
            Radiant.convert_degree_to_radiant(max_range),
            offset, scale, inverse
        )

    def servo_position_changed(self, servo: Servo) -> None:
        self._actual_position.configure(text=f"{servo.get_position_as_degree()}°")
        self._position_slider.set(servo.get_position_as_degree())

    def servo_speed_changed(self, global_id: int, speed: int) -> None:
        self._speed_var.set(str(speed))

    def is_on(self, servo: Servo) -> None:
        self._state.set(servo.is_on())

    def force_feedback_on(self, servo: Servo) -> None:
        # this.forceFeedbackCheckBox.setSelected(servo.forceFeedbackisOn());
        raise ValueError("WIP")

    def position_feedback_on(self, servo: Servo) -> None:
        # this.positionFeedbackCheckBox.setSelected(servo.positionFeedbackisOn());
        raise ValueError("WIP")

    def servo_force_threshold_changed(self, global_id: int, threshold: int) -> None:
        # this.forceFeedbackSpinner.setValue(threshold);
        raise ValueError("WIP")

    def is_active(self, servo: Servo) -> None:
        print("'is_active is Not of your concern -> ignore'")

    def is_stalling(self, servo: Servo) -> None:
        print("'is_stalling is Not of your concern -> ignore'")

    def settings_changed(self, component: RobotComponent) -> None:
        pass

    def servo_force_position_changed(self, global_id: int, threshold: int) -> None:
        pass

    def is_at_min(self, servo: Servo) -> None:
        pass

    def is_at_max(self, servo: Servo) -> None:
        pass



"""
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

"""
