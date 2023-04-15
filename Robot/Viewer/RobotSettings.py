import pickle
from os.path import exists


class RobotSettings:
    _settings = dict()
    # TODO this is likely a typo as it is usually .pkl for py2 & .pickle or .p for py3
    _file_name = "settings.plk"

    @staticmethod
    def add_setting(key, value):
        RobotSettings._settings[key] = value
        pass

    @staticmethod
    def get_int(key):
        value = 0
        if key in RobotSettings._settings:
            value = RobotSettings._settings[key]
            if not isinstance(value, int):
                value = 0
        return value

    @staticmethod
    def get_bool(key):
        value = False
        if key in RobotSettings._settings:
            value = RobotSettings._settings[key]
            if not isinstance(value, bool):
                value = False
        return value

    @staticmethod
    def set_key(key, value):
        RobotSettings._settings[key] = value

    @staticmethod
    def set_file_name(file_name):
        RobotSettings._file_name = file_name

    @staticmethod
    def save_settings():
        print('----------Save Settings------------')
        with open(RobotSettings._file_name, 'wb') as f:
            pickle.dump(RobotSettings._settings, f)
            print(RobotSettings._settings)

    @staticmethod
    def load_settings():
        print('----------Load Settings------------')
        if exists(RobotSettings._file_name):
            with open(RobotSettings._file_name, 'rb') as f:
                RobotSettings._settings = pickle.load(f)
                print(RobotSettings._settings)
