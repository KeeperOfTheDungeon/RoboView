import pickle
from os.path import exists


class RobotSettings:
    _settings = dict()
    # TODO this is likely a typo as it is usually .pkl for py2 & .pickle or .p for py3
    _file_name = "settings.plk"

    @staticmethod
    def get_int(key, default=0):
        value = RobotSettings._settings.get(key)
        return value if isinstance(value, int) else default

    @staticmethod
    def get_bool(key, default=False):
        value = RobotSettings._settings.get(key)
        return value if isinstance(value, bool) else default

    @staticmethod
    def get_key(key, default=None):
        return RobotSettings._settings.get(key, default)

    @staticmethod
    def set_key(key, value):
        RobotSettings._settings[key] = value

    add_setting = set_key

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
