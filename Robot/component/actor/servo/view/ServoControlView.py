from tkinter.font import Font

import customtkinter as ctk
import tkinter as tk

from tkinter import HORIZONTAL, BooleanVar, StringVar

from RoboControl.Robot.Component.Actor.Servo import Servo
from RoboControl.Robot.Component.RobotComponent import RobotComponent
from RoboControl.Robot.Math.Radiant import Radiant
from RoboView.Robot.component.actor.servo.view.StepWidthVar import StepWidthVar
from RoboView.Robot.component.view.ActorControlView import ActorControlView
from RoboView.Robot.component.view.MissingComponentView import MissingComponentView


class ServoControlView(ActorControlView):
    _actor: Servo  # protected Servo servo;

    def __init__(self, root, servo, settings_key):
        super().__init__(root, servo, settings_key, 190, 110)

        self._min_pos = StringVar()  # private JLabel minPos;
        self._actual_pos = StringVar()  # private JLabel actualPosition;
        self._max_pos = StringVar()  # private JLabel maxPos;

        self._is_on = BooleanVar()  # private JCheckBox onCheckBox;
        self._speed = StepWidthVar()  # private StepWidthNumberModel stepWidth;

        self._position = tk.DoubleVar()  # private int position;

        # // protected ServoControlInterface servoListener

        self._position_slider = ctk.CTkSlider(self._data_frame)  # private JSlider slider;
        self._default_button_color = self._position_slider.cget("button_color")
        # private JSpinner stepSize;

        servo.add_setup_listener(self)
        servo.add_sensor_listener(self)

        self.build_view()

        # --------------------------------------------------------------

        self._actor.remote_get_settings()
        self.update_values(servo)

    def build_view(self) -> None:
        super().build_view()

        inset_left, inset_top = 20, 10

        self._position_slider.configure(
            from_=-100, to=100, number_of_steps=25,  # java: 0 -> 0
            width=150, height=20,
            command=self.on_position_slider_changed,  # slider.addChangeListener(this);
        )
        self._position_slider.place(
            x=inset_left, y=inset_top,
        )

        for index, variable in enumerate([self._min_pos, self._actual_pos, self._max_pos]):
            kwargs = {"width": 40, "height": 20}
            x = inset_left + (55 * index)
            y = inset_top + 25
            variable.set("-°")
            ctk.CTkLabel(self._data_frame, textvariable=variable, **kwargs).place(x=x, y=y)

        ctk.CTkCheckBox(
            self._data_frame, text="on", variable=self._is_on,
            checkbox_width=20, checkbox_height=20,
            command=self.on_servo_on_checkbox_action,  # onCheckBox.addActionListener(this);
        ).place(x=inset_left, y=inset_top + 55)
        # onCheckBox.setActionCommand("cmdActive");

        ctk.CTkLabel(
            self._data_frame, text="step",
            height=20
        ).place(x=inset_left + 80, y=inset_top + 55)
        tk.Spinbox(
            self._data_frame, textvariable=self._speed,
            from_=0, to=10, increment=1,
            width=4, font=Font(family="Helvetica", size=10),
            command=self.on_speed_spinner_changed  # stepSize.addChangeListener(this);
        ).place(x=inset_left + 140, y=inset_top + 75)

        self.update_values(self._actor)

    @staticmethod
    def create_view(root, servo, settings_key):
        """ "creates new servo control view and link it given servo" """
        if servo is None:
            return MissingComponentView(Servo.__class__.__name__)
        return ServoControlView(root, servo, settings_key)

    def update_position(self, position: float) -> None:
        self._position.set(position)
        self._actual_pos.set(f"{position:.2f}°")

    def update_values(self, servo: Servo) -> None:
        minimum = int(Radiant.convert_radiant_to_degree(servo.get_min_range()))
        maximum = int(Radiant.convert_radiant_to_degree(servo.get_max_range()))
        self._min_pos.set(f"{minimum:.2f}°")
        self._max_pos.set(f"{maximum:.2f}°")
        self._speed.set_index(servo.get_speed())  # this.speedSpinerModel.setIndex(servo.getSpeed());
        if self._position_slider.winfo_exists():
            self._position_slider.configure(from_=minimum, to=maximum)
            if (maximum - minimum) < 1:
                self._position_slider.configure(state="disabled")
                self._position_slider.configure(button_color="gray")
            else:
                self._position_slider.configure(state="normal")
                self._position_slider.configure(button_color=self._default_button_color)

    def servo_position_changed(self, servo: Servo):
        pass  # also empty in java

    def is_active(self, servo: int) -> None:
        print("'is_active is Not of your concern -> ignore'")

    # noinspection PyMethodMayBeStatic
    def is_stalling(self, _servo: int) -> None:
        print("'is_stalling is Not of your concern -> ignore'")

    # noinspection PyMethodMayBeStatic
    def servo_offset_changed(self, _servo: int, _offset: int) -> None:
        print("'servo_offset_changed is Not of your concern -> ignore'")

    def servo_min_range_changed(self, _servo: int, min_range: float) -> None:
        self._max_pos.set(f"{min_range:.2f}°")
        self._position_slider.configure(from_=min_range)

    def servo_max_range_changed(self, _servo: int, max_range: float) -> None:
        self._max_pos.set(f"{max_range:.2f}°")
        self._position_slider.configure(to=max_range)

    def is_on(self, servo: Servo) -> None:
        self._is_on.set(servo.is_on())

    def inverse(self, global_id: int, status: bool) -> None:
        pass  # also empty in java

    def servo_setup_changed(self, servo: Servo) -> None:
        self.update_values(servo)

    def servo_speed_changed(self, global_id: int, speed: int) -> None:
        self._speed.set_index(speed)

    def settings_changed(self, component: RobotComponent) -> None:
        pass  # also empty in java

    def force_feedback_on(self, servo: Servo) -> None:
        pass  # also empty in java

    def position_feedback_on(self, servo: Servo) -> None:
        pass  # also empty in java

    def servo_force_threshold_changed(self, global_id: int, threshold: int) -> None:
        pass  # also empty in java

    def servo_force_position_changed(self, global_id: int, threshold: int) -> None:
        pass  # also empty in java

    def is_at_min(self, servo: Servo) -> None:
        pass  # also empty in java

    def is_at_max(self, servo: Servo) -> None:
        pass  # also empty in java

    # ------------------------------------- public void stateChanged(ChangeEvent event)

    def on_position_slider_changed(self, position: float) -> None:
        # if self._position == position:
        #     return
        self.update_position(position)
        position = Radiant.convert_degree_to_radiant(position)
        self._actor.remote_move_servo_to(position)

    def on_speed_spinner_changed(self) -> None:
        self._actor.remote_set_servo_speed(self._speed.get_index())

    # ------------------------------------- public void actionPerformed(ActionEvent actionEvent)

    def on_servo_on_checkbox_action(self) -> None:
        if self._is_on.get():
            self._actor.remote_servo_on()
        else:
            self._actor.remote_servo_off()
