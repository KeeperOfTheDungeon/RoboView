import tkinter
from tkinter import Label
import customtkinter as ctk

from RoboControl.Robot.AbstractRobot.AbstractListener import ServoDataListener
from RoboControl.Robot.Component.Actor.servo.Servo import Servo
from RoboControl.Robot.Component.generic.distance.DistanceSensor import DistanceSensor
from RoboView.Robot.component.view.MissingComponentView import MissingComponentView
from RoboView.Robot.component.view.SensorDataView import SensorDataView


class ServoDataView(SensorDataView, ServoDataListener):
    def __init__(self, root, servo: Servo, settings_key):
        super().__init__(root, servo, settings_key, width=160, height=90)
        self.build_view()

    def build_view(self) -> None:
        # super().build_view()
        self._sensor.add_sensor_listener(self)

        insets_left = 0
        insets_top = 0
        form = ctk.CTkFrame(fg_color="transparent", master=self._data_frame, width=160, height=110)
        form.grid_rowconfigure("all", weight=1)
        form.pack(fill="both", expand=True,
                  ipadx=5, ipady=5)

        position_label = ctk.CTkLabel(master=form, text="position")
        position_label.configure(width=50, height=20)
        position_label.place(x=insets_left + 5, y=insets_top + 5)

        self._position_value = tkinter.StringVar()
        value_label = ctk.CTkLabel(
            master=form, textvariable=self._position_value, text="--", width=40, height=20
        )  # centered # black border
        value_label.place(x=insets_left + 60, y=insets_top + 5)

        self._at_min_flag = ctk.CTkCheckBox(master=form, text="min", command=print)
        self._at_min_flag.configure(width=60, height=20)
        self._at_min_flag.place(x=insets_left + 5, y=insets_top + 35)
        self._at_min_flag.configure(state=tkinter.DISABLED)

        self._at_max_flag = ctk.CTkCheckBox(master=form, text="max", command=print)
        self._at_max_flag.configure(width=60, height=20)
        self._at_max_flag.place(x=insets_left + 85, y=insets_top + 35)
        self._at_max_flag.configure(state=tkinter.DISABLED)

        self._active_flag = ctk.CTkCheckBox(master=form, text="active", command=print)
        self._active_flag.configure(width=60, height=20)
        self._active_flag.place(x=insets_left + 5, y=insets_top + 60)
        self._active_flag.configure(state=tkinter.DISABLED)

        self._inverse_flag = ctk.CTkCheckBox(master=form, text="inverse", command=print)
        self._inverse_flag.configure(width=70, height=20)
        self._inverse_flag.place(x=insets_left + 5, y=insets_top + 85)
        self._inverse_flag.configure(state=tkinter.DISABLED)

        self._stall_flag = ctk.CTkCheckBox(master=form, text="stall", command=print)
        self._stall_flag.configure(width=60, height=20)
        self._stall_flag.place(x=insets_left + 85, y=insets_top + 85)
        self._stall_flag.configure(state=tkinter.DISABLED)

        self._is_on_flag = ctk.CTkCheckBox(master=form, text="on", command=print)
        self._is_on_flag.configure(width=60, height=20)
        self._is_on_flag.place(x=insets_left + 85, y=insets_top + 60)
        self._is_on_flag.configure(state=tkinter.DISABLED)

    @staticmethod
    def create_view(root, servo, settings_key):
        """
        "creates new servo data view and link it given servo"
        :param root:
        :param servo: "servo to be connected with created view"
        :param settings_key:
        :return: "a new servo data view"
        """
        if servo is not None:
            return ServoDataView(root, servo, settings_key)
        # return(new MissingValueView(Servo.class.getName(), false));
        return MissingComponentView(DistanceSensor.__name__)

    def update(self, servo: Servo) -> None:
        degree = servo.get_position_as_degree()
        self._position_value.set(f"{degree:.2f}°")
        self._at_max_flag.select() if servo.is_at_min() else self._at_max_flag.deselect()
        self._active_flag.select() if servo.is_active() else self._active_flag.deselect()
        self._stall_flag.select() if servo.is_stalling() else self._stall_flag.deselect()
        self._is_on_flag.select() if servo.is_on() else self._is_on_flag.deselect()

    def force_feedback_on(self, servo: Servo) -> None:
        raise ValueError("WIP")

    def position_feedback_on(self, servo: Servo) -> None:
        raise ValueError("WIP")

    def is_active(self, servo: Servo) -> None:
        self.update(servo)

    def is_at_min(self, servo: Servo) -> None:
        self.update(servo)

    def is_at_max(self, servo: Servo) -> None:
        self.update(servo)

    def is_stalling(self, servo: Servo) -> None:
        self.update(servo)

    def is_on(self, servo: Servo) -> None:
        self._is_on_flag.select() if servo.is_on() else self._is_on_flag.deselect()

    def component_value_changed(self, servo: Servo) -> None:
        self.update(servo)
