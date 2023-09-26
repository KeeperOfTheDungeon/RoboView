import traceback
from tkinter import messagebox

import customtkinter as ctk

from RoboControl.Com.Connection.SerialConnection import SerialConnection
from RoboControl.Robot.AbstractRobot.AbstractRobot import AbstractRobot
from RoboView.Gui.InternalWindow.InternalWindow import InternalWindow
from RoboView.Robot.Viewer.RobotSettings import RobotSettings
from RoboView.Robot.Viewer.WindowBar import WindowBar
from ant import Ant


class SerialConnectionView(InternalWindow):  # extends DisplayFrame implements RobotConnectionListener, ActionListener
    FRAME_NAME: str = "Serial Connection"

    CONNECT_TEXT: str = "Connect"
    DISCONNECT_TEXT: str = "Disconnect"
    AUTO_CONNECT_TEXT: str = "auto connect"

    CMD_AUTO_CONNECT: str = "cmdAutoConnect"
    CMD_PORT_SELECTED: str = "cmdportSelected"
    CMD_CONNECT: str = "cmdConnect"
    CMD_DISCONNECT: str = "cmdDisconnect"

    PORT_KEY: str = ".port"
    AUTO_CONNECT_KEY: str = ".autoConnect"

    def __init__(self, root: ctk.CTkFrame, window_bar: WindowBar):
        available_ports = [str(p.name) for p in SerialConnection.get_ports()]
        if not available_ports:
            messagebox.showerror("Error", "No ports available!")
            raise ValueError("No ports available!")
        super().__init__(root, self.FRAME_NAME, window_bar)
        self.root = root

        self._robot = None
        # TODO these aren't really optional
        self.connector: ctk.CTkButton = None
        self.port_selector: ctk.CTkComboBox = None
        self.auto_connect: ctk.CTkCheckBox = None
        self.pinger: ctk.CTkButton = None

        # TODO this should either go upstream or be deleted
        self._frame.configure(bg="white")
        self.buildView()
        # self.show_window()

    # FIXME camelCase
    def buildView(self) -> None:
        self.move(-10, -10)
        self.set_min_dimension(300, 380)

        form = ctk.CTkFrame(fg_color="transparent", master=self._frame)
        form.grid_rowconfigure("all", weight=1)
        form.pack(fill="both", expand=True,
                  padx=(10, 20), pady=(30, 20),
                  ipadx=5, ipady=5)

        port_selection = ctk.CTkFrame(form, bg_color="transparent", fg_color="#ebebeb")
        port_selection.pack(pady=10, padx=10)

        ctk.CTkLabel(port_selection, text="Serial Port:").pack(pady=(10, 0), padx=10)
        available_ports = [str(p.name) for p in SerialConnection.get_ports()]
        self.port_selector = ctk.CTkComboBox(port_selection, values=available_ports, command=self.save_actual_port)
        self.port_selector.pack(pady=10, padx=10)
        # this.portSelector.setActionCommand(SerialConnectionView.CMD_PORT_SELECTED);
        # this.portSelector.addActionListener(this);

        self.auto_connect = ctk.CTkCheckBox(master=form, text=self.AUTO_CONNECT_TEXT, command=self.save_auto_connect)
        self.auto_connect.pack(pady=10, padx=10)
        # this.autoConnect.addActionListener(this);
        # this.autoConnect.setActionCommand(SerialConnectionView.CMD_AUTO_CONNECT);

        self.connector = ctk.CTkButton(master=form, text=self.CONNECT_TEXT, height=30, command=self.connect)
        self.connector.pack(pady=10, padx=10)
        self.pinger = ctk.CTkButton(master=form, text="Ping !", height=30, state="disabled", fg_color="green")
        self.pinger.pack(pady=(0, 10), padx=10)
        # this.connector.addActionListener(this);
        # this.connector.setActionCommand(SerialConnectionView.CMD_CONNECT);

    def load_settings(self) -> None:
        port_key = self._settings_key + SerialConnectionView.PORT_KEY
        port_name = RobotSettings.get_key(port_key, default=self.port_selector.get())
        self.port_selector.set(port_name)
        auto_connect_key = self._settings_key + SerialConnectionView.AUTO_CONNECT_KEY
        auto_connect = RobotSettings.get_bool(auto_connect_key, default=False)
        self.auto_connect.select() if auto_connect else self.auto_connect.deselect()

    def save_actual_port(self) -> None:
        key = self._settings_key + SerialConnectionView.PORT_KEY
        RobotSettings.set_key(key, self.port_selector.get())
        RobotSettings.save_settings()

    def save_auto_connect(self) -> None:
        key = self._settings_key + SerialConnectionView.AUTO_CONNECT_KEY
        RobotSettings.set_key(key, bool(self.auto_connect.get()))
        RobotSettings.save_settings()

    # FIXME why is a parameter required here ? (AbstractRobot.on_connected sends one)
    def connect(self, *_args) -> None:
        selected_port = self.port_selector.get()
        try:
            self._robot._connection.set_port(selected_port)
            self._robot._connection.set_data_packet_logger(self._robot.get_data_packet_logger())
            self._robot.connect(self._robot._connection)
            self.connected(self._robot)
        except Exception as e:
            print(traceback.format_exc())
            messagebox.showerror("Error", f"Unable to connect to port {selected_port}:\n{e}")

    def set_robot(self, robot: AbstractRobot) -> bool:
        self._robot = robot
        # FIXME why double connection ?
        # self._robot.add_connection_listener(self)
        self.load_settings()
        if self.auto_connect.get():
            self.connect()
        return True

    # TODO this should be renamed to on_* for consistency
    def connected(self, robot: Ant) -> None:
        self.connector.configure(text=SerialConnectionView.DISCONNECT_TEXT, command=self.disconnect)
        self.pinger.configure(command=robot.get_data_hub().remote_ping_device, state="normal")

    # TODO why is a parameter required here
    def disconnect(self, *_args) -> None:
        self._robot._connection.disconnect()
        self._robot.disconnect()
        self.disconnected(self._robot)

    # TODO this should be renamed to on_* for consistency
    def disconnected(self, _robot: AbstractRobot) -> None:
        self.connector.configure(text=SerialConnectionView.CONNECT_TEXT, command=self.connect)
        self.pinger.configure(state="disabled")

    # TODO is this relevant?
    def action_performed(self, event) -> None:
        cmd = event.get_action_command()
        if cmd == SerialConnectionView.CMD_CONNECT:
            self.connect()
        elif cmd == SerialConnectionView.CMD_DISCONNECT:
            self.disconnect()
        elif cmd == SerialConnectionView.CMD_PORT_SELECTED:
            self.save_actual_port()
        elif cmd == SerialConnectionView.CMD_AUTO_CONNECT:
            self.save_auto_connect()
