from tkinter import IntVar

import customtkinter as ctk

from RoboControl.Robot.Component.Actor.Led import Led
from RoboView.Robot.component.view.ActorControlView import ActorControlView
from RoboView.Robot.component.view.MissingComponentView import MissingComponentView


class LedControlView(ActorControlView):
    """ "ComponentView child, that implements a Slider changing a Led's brightness." """
    _actor: Led

    def __init__(self, root, led, settings_key):
        super().__init__(root, led, settings_key, 150, 70)

        self._brightness = IntVar()
        self._brightness_slider = ctk.CTkSlider(
            self._data_frame, from_=0, to=255, width=120, height=20, number_of_steps=255, variable=self._brightness
        )
        ctk.CTkLabel(
            master=self._data_frame, textvariable=self._brightness, text="?", width=40, height=20
        ).place(x=60, y=40)
        self._brightness_slider.configure(command=self.change_brightness)
        self._brightness_slider.place(x=20, y=20)
        self._brightness_slider.bind("<Button-1>", self.mouse_pressed_sensor)
        self._brightness_slider.bind("<ButtonRelease-1>", self.mouse_released_value_label)
        self._brightness_slider.bind("<Leave>", self.mouse_released_value_label)

    # self._state = BooleanVar()
    # self._on_button = Checkbutton(self._data_frame, text="on", variable=self._state, command=self.changeStatus)
    # self._on_button.place(x = 5, y = 20,  width=40, height=20)

    @staticmethod
    def create_view(root, led, settings_key):
        if led is None:
            return MissingComponentView(Led.__name__)
        return LedControlView(root, led, settings_key)

    def change_brightness(self, brightness):
        value = float(brightness) / 255
        self._actor.remote_set_brightness(value)

    def mouse_pressed_sensor(self, event):
        self.mouse_pressed(event)
        # self._brightness_slider.bind("<Motion>", self.mouse_motion)

    def mouse_released_value_label(self, event):
        # self._brightness_slider.unbind("<Motion>")
        pass
