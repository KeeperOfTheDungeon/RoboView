from tkinter import StringVar

from RoboControl.Robot.AbstractRobot.AbstractListener import ChangeListener
from RoboControl.Robot.Math.Radiant import Radiant


class StepWidthVar(StringVar):
    def __init__(self):
        super().__init__()
        self._index = 0
        self._change = None
        self._change_listeners: list[ChangeListener] = []

    def has_changed(self) -> bool:
        if self._change:
            self._change = False
            return True
        return False

    def output_text(self) -> str:
        position: float = self._index / 200
        position = Radiant.convert_radiant_to_degree(position)
        return f"{position:.2f}°/sec"

    def get_index(self) -> int:
        return self._index

    def set_index(self, index: int) -> None:
        self._index = index
        self.notify_listeners()

    def get(self) -> str:
        return self.output_text()

    def set(self, value: str) -> None:
        self.notify_listeners()

    def get_next_value(self) -> str:
        if self._index < 180:
            self._index += 1
            self._change = True
        return self.output_text()

    def get_previous_value(self) -> str:
        if self._index > 0:
            self._index -= 1
            self._change = True
        return self.output_text()

    def notify_listeners(self) -> None:
        change_listeners = self.get_change_listeners()
        for index, listener in enumerate(change_listeners):
            change_listeners[index].on_change()

    # ---
    def get_change_listeners(self) -> list[ChangeListener]:
        return self._change_listeners

    def add_change_listener(self, listener: ChangeListener) -> None:
        self._change_listeners.append(listener)
