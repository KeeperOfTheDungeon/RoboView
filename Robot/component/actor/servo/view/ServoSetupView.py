from email.utils import decode_rfc2231
from tkinter import BooleanVar, Checkbutton, Spinbox, StringVar, IntVar, DoubleVar
import customtkinter as ctk

from RoboControl.Robot.AbstractRobot.AbstractListener import ServoSetupListener, ServoDataListener
from RoboControl.Robot.Component.Actor.servo.Servo import Servo
from RoboControl.Robot.Component.RobotComponent import RobotComponent
from RoboControl.Robot.Math.Radiant import Radiant
from RoboView.Robot.component.actor.servo.view.StepWidthVar import StepWidthVar

from RoboView.Robot.component.view.ComponentSetupView import ComponentSetupView
from RoboView.Robot.component.view.MissingComponentView import MissingComponentView

from logger import getLogger

logger = getLogger(__name__)


class ServoSetupView(
    ComponentSetupView,  # ComponentSettingsView<Servo>
    ServoSetupListener, ServoDataListener,
):
    def __init__(self, root, servo: Servo, settings_key):
        super().__init__(root, servo, settings_key, 250, 120)
        self._actor: Servo = servo

        self._min_pos = IntVar()  # private JSpinner minRange;
        self._min_pos_spinner = Spinbox(self._data_frame)  # protected SpinnerNumberModel minSpinerModel ;

        self._actual_pos = StringVar()  # private JLabel actualPosition;
        self._max_pos = IntVar()  # private JSpinner maxRange;
        self._max_pos_spinner = Spinbox(self._data_frame)  # protected SpinnerNumberModel maxSpinerModel ;

        self._position = DoubleVar()  # private float position;
        self._position_slider = ctk.CTkSlider(self._data_frame)  # private JSlider slider;

        self._is_on = BooleanVar()  # private JCheckBox onCheckBox;
        self._is_reverse = BooleanVar()  # private JCheckBox reverseCheckBox;

        self._scale = IntVar()  # protected SpinnerNumberModel scaleSpinerModel;
        self._speed = StepWidthVar()  # private JSpinner speed; # private StepWidthNumberModel speedSpinerModel;
        self._offset = IntVar()  # // private JSpinner offset; # protected SpinnerNumberModel offsetSpinerModel;

        self._is_force_feedback_on = BooleanVar()  # private JCheckBox forceFeedbackCheckBox;
        self._force_feedback = IntVar()
        self._is_position_feedback_on = BooleanVar()  # private JCheckBox positionFeedbackCheckBox;
        self._position_feedback = IntVar()

        # -------------------

        # self._actor.remote_start_stream(index, int(int(self._period.get())/10))

        self.build_view()

        servo.add_sensor_listener(self)
        servo.add_setup_listener(self)

        # ---------------------------

        self._actor.remote_get_settings()
        self._actor.remote_get_servo_speed()

    def build_view(self) -> None:
        super().build_view()

        label_font = ctk.CTkFont(family="Arial", size=10)

        # JLabel("position").setBounds(insets.left+5,insets.top+12,40,20)
        self._actual_pos.set("0")
        ctk.CTkLabel(
            self._data_frame, textvariable=self._actual_pos, text="?",
            width=40, height=20
        ).place(x=20, y=85)  # this.actualPosition: JLabel

        self._position.set(0)
        self._position_slider.configure(
            self._data_frame, from_=-90, to=90, variable=self._position,  # orient=HORIZONTAL
            width=150, height=20, number_of_steps=45,
            command=self.on_position_slider_change  # this.slider.addChangeListener(this);
        )
        self._position_slider.place(x=50, y=25)

        self._min_pos.set(0)
        self._min_pos_spinner.configure(
            textvariable=self._min_pos,
            from_=-90, to=90, increment=1,
            width=10,
            command=self.on_min_spinner_change,  # this.minRange.addChangeListener(this);
        )
        self._min_pos_spinner.place(x=5, y=30, width=40, height=20)

        self._max_pos.set(0)
        self._min_pos_spinner.configure(
            textvariable=self._max_pos,
            from_=-90, to=90, increment=1,
            width=10,
            command=self.on_max_spinner_change,  # this.maxRange.addChangeListener(this);
        )
        self._min_pos_spinner.place(x=260, y=30, width=40, height=20)

        self._is_on.set(False)
        Checkbutton(
            self._data_frame, text="on", variable=self._is_on,
            command=self.on_servo_on_checkbox_action  # this.onCheckBox.addActionListener(this);
        ).place(x=5, y=70, width=40, height=20)
        # this.onCheckBox.setActionCommand(CMD_ON);

        self._is_reverse.set(False)
        Checkbutton(
            self._data_frame, text="reverse", variable=self._is_reverse,
            command=self.on_servo_reverse_checkbox_action,  # this.reverseCheckBox.addActionListener(this);
        ).place(x=55, y=70, width=60, height=20)
        # //	reverseCheckBox(BCMD_DRAV_DIRECT);

        self._offset.set(750)
        ctk.CTkLabel(
            self._data_frame, text="offset",
            font=label_font, bg_color="transparent",
            width=80, height=15,
        ).place(x=130, y=54)
        Spinbox(
            self._data_frame, textvariable=self._offset,
            from_=300, to=10000, increment=1,
            width=10,
            command=self.on_offset_spinner_action  # tmpSpinner.addChangeListener(this);
        ).place(x=240, y=70, width=60, height=20)

        self._scale.set(15707)
        ctk.CTkLabel(
            self._data_frame, text="scale",
            font=label_font, bg_color="transparent",
            width=80, height=15,
        ).place(x=130, y=72)
        Spinbox(
            self._data_frame, textvariable=self._scale,
            from_=10000, to=20000, increment=1,
            width=10,
            command=self.on_scale_spinner_action,  # tmpSpinner.addChangeListener(this);
        ).place(x=240, y=90, width=60, height=20)

        # self._speed.add_change_listener(self)
        ctk.CTkLabel(
            self._data_frame, text="speed",
            font=label_font, bg_color="transparent",
            width=80, height=15,
        ).place(x=130, y=90)
        Spinbox(
            self._data_frame, textvariable=self._speed,
            from_=0, to=52, increment=0.28,
            width=10,
            command=self.on_speed_spinner_change  # this.speed.addChangeListener(this);
        ).place(x=240, y=110, width=60, height=20)

        # Not yet implemented

        self._is_force_feedback_on.set(False)
        Checkbutton(  # private JCheckBox forceFeedbackCheckBox;
            self._data_frame, text="Force Feedback", variable=self._is_on,
            command=self.on_force_feedback_checkbox_action  # this.forceFeedbackCheckBox.addActionListener(this);
        )  # .place(x=5, y=70, width=40, height=20)
        # this.onCheckBox.setActionCommand(CMD_FORCEFEEDBACK_ON);

        self._is_position_feedback_on.set(False)
        Checkbutton(  # private JCheckBox positionFeedbackCheckBox;
            self._data_frame, text="Position Feedback", variable=self._is_on,
            command=self.on_position_feedback_checkbox_action  # this.positionFeedbackCheckBox.addActionListener(this);
        )  # .place(x=5, y=70, width=40, height=20)
        # this.onCheckBox.setActionCommand(CMD_POSITIONFEEDBACK_ON);

        # private JSpinner forceFeedbackSpinner; # private SpinnerNumberModel forceFeedbackSpinnerModel;
        self._force_feedback.set(30)
        # this.forceFeedbackSpinnerModel = new SpinnerNumberModel();
        # this.forceFeedbackSpinner = new JSpinner(forceFeedbackSpinnerModel);
        # this.forceFeedbackSpinner.setBounds(insets.left+130, insets.top+140, 80, 25);
        # this.forceFeedbackSpinner.addChangeListener(this);
        # add(this.forceFeedbackSpinner);

        # private JSpinner positionFeedbackSpinner; # private SpinnerNumberModel positionFeedbackSpinnerModel;
        self._position_feedback.set(500)
        # this.positionFeedbackSpinnerModel = new SpinnerNumberModel();
        # this.positionFeedbackSpinner = new JSpinner(positionFeedbackSpinnerModel);
        # this.positionFeedbackSpinner.setBounds(insets.left+130, insets.top+190, 80, 25);
        # this.positionFeedbackSpinner.addChangeListener(this);
        # add(this.positionFeedbackSpinner);

        # protected JButton calibrate;
        # this.calibrate = new JButton("calibrate");
        # this.calibrate.setBounds(insets.left+210, insets.top+190, 80, 20);
        # this.calibrate.addActionListener(new ActionListener()
        # {
        #
        #     @Override
        #     public void actionPerformed(ActionEvent arg0)
        #     {
        #         ServoSetupView.this.component.remote_calibrate();
        #     }
        #
        # });
        # this.add(this.calibrate);

        # this.servoPosition = new JProgressBar().setBounds(insets.left+70, insets.top+10, 182, 16)

        # INFO self.build_context_menue() is called implicitly at ComponentView
        #   and does the following from java: addSetButton, addGetButton, addSaveButton, addLoadButton

        self.update_values(self._actor)

    def update_position(self, position: float) -> None:
        self._position.set(position)
        self._actual_pos.set(f"{position:.2f}°")

    def update_values(self, servo: Servo) -> None:
        minimum = int(Radiant.convert_radiant_to_degree(servo.get_min_range()))
        maximum = int(Radiant.convert_radiant_to_degree(servo.get_max_range()))
        self._min_pos.set(minimum)
        self._max_pos.set(maximum)
        self._offset.set(servo.get_offset())
        self._scale.set(servo.get_scale())
        self._speed.set_index(servo.get_speed())  # this.speedSpinerModel.setIndex(servo.getSpeed());
        if self._position_slider.winfo_exists():
            self._position_slider.configure(from_=minimum, to=maximum)

    @staticmethod
    def create_view(root, servo: Servo, settings_key):
        """ "creates new servo setup view and link it given servo" """
        if servo is None:
            return MissingComponentView(Servo.__class__.__name__)
        return ServoSetupView(root, servo, settings_key)

    def set_settings(self) -> bool:
        min_range = int(self._min_pos.get())
        max_range = int(self._max_pos.get())
        offset = int(self._offset.get())
        scale = int(self._scale.get())
        inverse = bool(self._is_reverse.get())
        return self._actor.remote_set_servo_defaults(
            Radiant.convert_degree_to_radiant(min_range),
            Radiant.convert_degree_to_radiant(max_range),
            offset, scale, inverse,
        )

    def servo_position_changed(self, servo: Servo) -> None:
        position = servo.get_position_as_degree()
        self._actual_pos.set(f"{position:.2f}°")
        self._position.set(int(position))

    # noinspection PyMethodMayBeStatic
    def is_active(self, _servo: Servo) -> None:
        print("'is_active is Not of your concern -> ignore'")

    # noinspection PyMethodMayBeStatic
    def is_stalling(self, _servo: Servo) -> None:
        print("'is_stalling is Not of your concern -> ignore'")

    def servo_speed_changed(self, _global_id: int, speed: int) -> None:
        self._speed.set_index(speed)  # this.speedSpinerModel.setIndex(speed);

    def is_on(self, servo: Servo) -> None:
        self._is_on.set(servo.is_on())

    def force_feedback_on(self, servo: Servo) -> None:
        self._is_force_feedback_on.set(servo.is_force_feedback_on())

    def servo_setup_changed(self, servo: Servo) -> None:
        self.update_values(servo)

    def settings_changed(self, _component: RobotComponent) -> None:
        pass  # also empty in java

    def position_feedback_on(self, servo: Servo) -> None:
        self._is_position_feedback_on.set(servo.is_position_feedback_on())

    def servo_force_threshold_changed(self, _global_id: int, threshold: int) -> None:
        self._force_feedback.set(threshold)

    def servo_force_position_changed(self, _global_id: int, threshold: int) -> None:
        # self._position_feedback.set(threshold)
        pass  # also empty in java

    def is_at_min(self, servo: Servo) -> None:
        pass  # also empty in java

    def is_at_max(self, servo: Servo) -> None:
        pass  # also empty in java

    # ------------------------------------- public void stateChanged(ChangeEvent event)

    def on_position_slider_change(self, position: float) -> None:
        # if self._position == position:
        #     return
        self.update_position(position)
        position = Radiant.convert_degree_to_radiant(position)
        self._actor.remote_set_servo_position(position)

    def on_min_spinner_change(self) -> None:
        value = self._min_pos.get()
        self._position_slider.configure(from_=value)
        self._max_pos_spinner.configure(from_=value)

    def on_max_spinner_change(self) -> None:
        value = self._max_pos.get()
        self._position_slider.configure(to=value)
        self._min_pos_spinner.configure(to=value)

    def on_speed_spinner_change(self) -> None:
        self._actor.remote_set_servo_speed(self._speed.get_index())

    def on_force_feedback_spinner_change(self) -> None:
        self._actor.remote_set_servo_force_threshold(self._force_feedback.get())

    def on_position_feedback_spinner_change(self) -> None:
        self._actor.remote_set_servo_force_position(self._position_feedback.get())

    # ------------------------------------- public void actionPerformed(ActionEvent actionEvent)

    def on_servo_on_checkbox_action(self) -> None:
        if self._is_on.get():
            self._actor.remote_servo_on()
        else:
            self._actor.remote_servo_off()

    def on_force_feedback_checkbox_action(self) -> None:
        if self._is_force_feedback_on.get():
            self._actor.remote_force_feedback_is_on()
        else:
            self._actor.remote_force_feedback_is_off()

    def on_position_feedback_checkbox_action(self) -> None:
        if self._is_position_feedback_on.get():
            self._actor.remote_position_feedback_is_on()
        else:
            self._actor.remote_position_feedback_is_off()

    # noinspection PyMethodMayBeStatic
    def on_servo_reverse_checkbox_action(self, *args, **kwargs) -> None:
        logger.warning("Checkbox was ignored: is_reverse")

    # noinspection PyMethodMayBeStatic
    def on_offset_spinner_action(self, *args, **kwargs) -> None:
        logger.warning("Spinner was ignored: offset")

    # noinspection PyMethodMayBeStatic
    def on_scale_spinner_action(self, *args, **kwargs) -> None:
        logger.warning("Spinner was ignored: scale")
