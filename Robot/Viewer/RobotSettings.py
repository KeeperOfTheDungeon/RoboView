import pickle
from os.path import exists


class RobotSettings:
    _settings = dict()
    _file_name = "settings.plk"

    def __init__(self):
        pass

    def add_setting(key, value):
        RobotSettings._settings[key] = value
        pass

    def get_int(key):
        value = 0
        if key in RobotSettings._settings:
            value = RobotSettings._settings[key]
            if not isinstance(value, int):
                value = 0
        return value

    def get_bool(key):
        value = False
        if key in RobotSettings._settings:
            value = RobotSettings._settings[key]
            if not isinstance(value, bool):
                value = False
        return value

    def set_key(key, value):
        RobotSettings._settings[key] = value

    def set_file_name(file_name):
        RobotSettings._file_name = file_name

    def save_settings():
        print('----------Save Settings------------')
        with open(RobotSettings._file_name, 'wb') as f:
            pickle.dump(RobotSettings._settings, f)
            print(RobotSettings._settings)

    def load_settings():
        print('----------Load Settings------------')
        if exists(RobotSettings._file_name):
            with open(RobotSettings._file_name, 'rb') as f:
                RobotSettings._settings = pickle.load(f)
                print(RobotSettings._settings)
