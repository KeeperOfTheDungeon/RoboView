import customtkinter as ctk

from tkinter import HORIZONTAL, W, BooleanVar, Checkbutton, Label, Scale

from RoboControl.Robot.Component.Actor.servo.Servo import Servo
from RoboControl.Robot.Component.RobotComponent import RobotComponent
from RoboControl.Robot.Component.generic.distance.DistanceSensor import DistanceSensor
from RoboControl.Robot.Math.Radiant import Radiant
from RoboView.Robot.component.view.ActorControlView import ActorControlView
from RoboView.Robot.component.view.MissingComponentView import MissingComponentView


class ServoControlView(ActorControlView):
    CMD_ACTIVE = "cmdActive"
    _actor: Servo

    def __init__(self, root, servo, settings_key):
        super().__init__(root, servo, settings_key, 180, 120)
        # self._value_label = Label(self._data_frame, text="0°", font=("Courier", 12))
        # self._value_label.place(x = 1, y = 2,  width=80, height=15)

        inset_left, inset_top = 0, 0
        self._position_slider = Scale(
            self._data_frame, from_=-100, to=100, orient=HORIZONTAL, command=self.change_position
        )
        self._position_slider.place(x=inset_left + 10, y=inset_top + 10, width=200, height=40)

        self._min_pos = ctk.CTkLabel(
            self._data_frame, text="0°", width=40, height=20, anchor=ctk.W
        )
        self._min_pos.place(x=inset_left + 20, y=inset_top + 55)
        self._max_pos = ctk.CTkLabel(
            self._data_frame, text="0°", width=40, height=20, anchor=ctk.W
        )
        self._max_pos.place(x=inset_left + 120, y=inset_top + 55)
        self._actual_position = ctk.CTkLabel(
            self._data_frame, text="-°", width=40, height=20, anchor=ctk.W
        )
        self._actual_position.place(x=inset_left + 120, y=inset_top + 80)

        self._state = BooleanVar()
        self._on_button = Checkbutton(self._data_frame, text="On", variable=self._state, command=self.change_status)
        self._on_button.place(x=inset_left + 10, y=inset_top + 110, width=80, height=20)

        self._position: int = None
        servo.add_setup_listener(self)
        servo.add_sensor_listener(self)

        step_label = ctk.CTkLabel(
            self._data_frame, text="step width", width=80, height=20
        )
        step_label.place(x=inset_left + 100, y=inset_top + 85)

        # self._step_size: Spinner = None  # stepSize.setBounds(insets.left+160, insets.top+55, 100, 25);
        # self._step_width: StepWidthNumberModel = None

        self.update_values(servo)

    @staticmethod
    def create_view(root, servo, settings_key):
        """ "creates new servo control view and link it given servo" """
        if servo is None:
            return MissingComponentView(DistanceSensor.__name__)
        return ServoControlView(root, servo, settings_key)

    def change_status(self):
        if self._state.get():
            self._actor.remote_servo_on()
        else:
            self._actor.remote_servo_off()

    def change_position(self, position):
        position = float(position)
        position = Radiant.convert_degree_to_radiant(position)
        self._actor.remote_move_servo_to(position)

    def update_position(self, position: int) -> None:
        self._position = position
        self._actual_position.configure(text=f"{position}°")

    def update_values(self, servo: Servo) -> None:
        minimum = Radiant.convert_radiant_to_degree(servo.get_min_range())
        maximum = Radiant.convert_radiant_to_degree(servo.get_max_range())
        self._min_pos.configure(text=f"{minimum:.2f}°")
        self._max_pos.configure(text=f"{maximum:.2f}°")
        if self._position_slider.winfo_exists():
            self._position_slider.configure(from_=minimum)
            self._position_slider.configure(to=maximum)
        # self._step_width.set_index(self._actor.get_speed())

    def state_changed(self, event: "ChangeEvent") -> None:
        if event.get_source() == self._position_slider:
            if self._position_slider.has_focues():
                if self._position != self._position_slider.get():
                    self.update_position(self._position_slider.get())
                    position = Radiant.convert_degree_to_radiant(self._position_slider.get())
                    self._actor.remote_move_servo_to(position)
        elif event.get_source() == self._step_size:
            if self._step_width.has_changed():
                self._actor.remote_set_servo_speed(self._step_width.get_index())

    def servo_position_changed(self, servo: Servo):
        pass

    def servo_speed_changed(self, servo: Servo, speed: int):
        pass

    @staticmethod
    def is_active(self, servo: int) -> None:
        print("'is_active is Not of your concern -> ignore'")

    @staticmethod
    def is_stalling(self, servo: int) -> None:
        print("'is_stalling is Not of your concern -> ignore'")

    @staticmethod
    def servo_offset_changed(self, servo: int, offset: int) -> None:
        print("'servo_offset_changed is Not of your concern -> ignore'")

    def servo_max_range_changed(self, servo: int, max_range: float) -> None:
        self._max_pos.configure(text=f"{max_range:.2f}°")
        self._position_slider.configure(to=max_range)

    def servo_min_range_changed(self, servo: int, min_range: float) -> None:
        self._max_pos.configure(text=f"{min_range:.2f}°")
        self._position_slider.configure(from_=min_range)

    def is_on(self, servo: Servo) -> None:
        self._on_button.select() if servo.is_on() else self._on_button.deselect()

    def inverse(self, global_id: int, status: bool) -> None:
        pass

    def servo_setup_changed(self, servo: Servo) -> None:
        self.update_values(servo)

    def servo_speed_changed(self, global_id: int, speed: int) -> None:
        raise ValueError("WIP: _step_width")
        self._step_width.set_index(speed)

    def settings_changed(self, component: RobotComponent) -> None:
        pass

    def force_feedback_on(self, servo: Servo) -> None:
        pass

    def position_feedback_on(self, servo: Servo) -> None:
        pass

    def servo_force_threshold_changed(self, global_id: int, threshold: int) -> None:
        pass

    def servo_force_position_changed(self, global_id: int, threshold: int) -> None:
        pass

    def is_at_min(self, servo: Servo) -> None:
        pass

    def is_at_max(self, servo: Servo) -> None:
        pass
