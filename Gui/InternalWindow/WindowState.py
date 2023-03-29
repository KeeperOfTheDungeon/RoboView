from enum import Enum
from RoboView.Robot.Viewer.RobotSettings import RobotSettings


class State(Enum):
    CLOSED = 0
    INIT_INTERNAL = 1
    INIT_MINIMIZED = 2
    INTERNAL = 3
    MINIMIZED = 4
    EXTERNAL = 5


class WindowState:
    def __init__(self, internal_window):
        print("get state: {}".format(internal_window._settings_key))
        self._state = RobotSettings.get_int(internal_window._settings_key+".state")
        if self._state == 0:
            self._state = State.CLOSED
        elif self._state == 1:
            self._state = State.INIT_INTERNAL
        elif self._state == 2:
            self._state = State.INIT_MINIMIZED
        elif self._state == 3:
            self._state = State.INTERNAL
        elif self._state == 4:
            self._state = State.MINIMIZED
        elif self._state == 5:
            self._state = State.EXTERNAL
        self._value = self._state.value
        self._settings_key = internal_window._settings_key


    def state(self, new_state):
        if isinstance(new_state, State):
            if self._state == State.CLOSED and new_state == State.INTERNAL or (
                self._state == State.INIT_INTERNAL and new_state == State.INTERNAL) or (
                self._state == State.INIT_MINIMIZED and new_state == State.MINIMIZED) or (
                self._state == State.MINIMIZED and new_state == State.INIT_MINIMIZED) or (
                self._state == State.INTERNAL and (new_state == State.INIT_INTERNAL or new_state == State.MINIMIZED or new_state == State.EXTERNAL)) or (
                self._state == State.MINIMIZED and (new_state == State.INIT_MINIMIZED or new_state == State.INTERNAL)) or (
                new_state == State.CLOSED or new_state == self._state):
                print("{} State changed from {} to {} ".format(self._settings_key, self._state, new_state))
                self._state = new_state
                RobotSettings.set_key(self._settings_key+".state", new_state.value)
            else:
                print("{} State change from {} to {} not possible".format(self._settings_key, self._state, new_state))
        else:
            raise ValueError("Invalid State")
        
    def isOpen(self):
        if self._state == State.INTERNAL or self._state == State.MINIMIZED:
            return True
        return False
    
    def isState(self, state):
        return self._state.value == state
