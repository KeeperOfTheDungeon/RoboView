import customtkinter as ctk
import tkinter as tk

from RoboControl.Robot.AbstractRobot import AbstractDevice
from RoboControl.Robot.AbstractRobot.AbstractRobot import AbstractRobot
from RoboControl.Robot.AbstractRobot.Config.DeviceConfig import DeviceConfig
from RoboControl.Robot.Device.RobotDevice import RobotDevice
from RoboView.Gui.InternalWindow.InternalWindow import InternalWindow
from RoboView.Robot.Device.Viewer.StatusBar import StatusBar
from RoboView.Robot.Device.Viewer.ToolBar import ToolBar
from RoboView.Robot.Ui.utils.colors import Color
from RoboView.Robot.Viewer.WindowBar import WindowBar
from RoboView.Robot.component.view.ComponentView import ComponentView


class DeviceViewSet(list):
    pass


CMD_CLEAR_ALL_STREAMS = "cmdClearAllStreams"
CMD_CONTINUE_ALL_STREAMS = "cmdContinueAllStreams"
CMD_DISPLAY_ALL_NAMES = "cmdDisplayAllNames"
CMD_HIDE_ALL_NAMES = "cmdHideAllNames"
CMD_LOAD_SETTINGS = "cmdGetSetup"
CMD_LOAD_STREAMS = "cmdLoadStreams"
CMD_LOCK_ALL = "cmdLockAll"
CMD_PAUSE_ALL_STREAMS = "cmdPauseAllStreams"
CMD_SAVE_STREAMS = "cmdSaveStreams"
CMD_SEND_PING = "cmdSendPing"
CMD_UNLOCK_ALL = "cmdUnlockAll"


class DeviceView(InternalWindow):
    FRAME_NAME: str = "generic DeviceView"

    _menu_bar: tk.Menu  # JMenuBar
    _toolbar: ToolBar
    _statusbar: StatusBar

    _form: ctk.CTkFrame
    _display: tk.Frame  # = component_panel: JPanel
    _toolbar_menu: "JCheckBoxMenuItem"
    _statusbar_menu: "JCheckBoxMenuItem"

    _device: RobotDevice

    _robot_name = "generic"

    def __init__(self, root: ctk.CTkFrame, device: RobotDevice, window_bar: WindowBar):
        super().__init__(root, self.FRAME_NAME, window_bar)
        self.build_panel()
        self.display_window(self._robot_name, device)
        self.set_device(self._robot_name, device)

    def build_panel(self) -> None:
        self.set_min_dimension(600, 400)
        self._form = ctk.CTkFrame(fg_color="transparent", master=self._frame)
        self._form.pack(
            fill="both", expand=True,
            padx=(10, 15), pady=(25, 15),
            ipadx=2, ipady=2
        )
        self._form.grid_columnconfigure(0, weight=10)
        self._form.grid_rowconfigure(1, weight=1)

    def set_device(self, robot_name: str, device: RobotDevice) -> None:
        self._device = device
        self.rename(f"{device.get_name()}({robot_name})")  # setName & setTitle
        self._toolbar.set_device(device)
        self._statusbar.set_device(device)

    def display_window(self, robot_name: str, device: RobotDevice) -> None:
        # self.build_panel()
        self.build_main_menu()

        self._toolbar = ToolBar(self._form, device)
        self._toolbar.get_frame().grid(row=0, sticky="ew", padx=2, pady=2, ipady=5)
        # self._toolbar.set_listener(device)
        # self._toolbar.set_aquisators()

        self._display = ctk.CTkFrame(self._form, border_width=1, fg_color="white")
        self._display.grid(row=1, sticky="ewns")

        self._statusbar = StatusBar(self._form, device)
        self._statusbar.get_frame().grid(row=2, sticky="ew", padx=2, pady=2, ipadx=2, ipady=2)

        # self.show_window()

    def make_error_display(self, name: str) -> None:
        self.rename(f"{name} - device not found")
        self.resize(100, 100)
        self.show_window()  # TODO self.to_front()

    def build_main_menu(self) -> None:
        """ "Adds Downdown Menus" """
        mb = self.make_streams_menu()
        mb.place()
        return
        self._menubar.add(self.make_streams_menu())
        self._menubar.add(self.make_device_menu())
        self._menubar.add(self.make_data_menu())
        self._menubar.add(self.make_tools_menu())
        self._menubar.add(self.make_components_menu())
        self.set_menubar(self._menubar)

    def run_command(self, command: str) -> None:
        """ """
        """
        object: Object = actionEvent.getSource()
        cmd: str = actionEvent.getActionCommand()
        if Object is self._toolbar_menu:
            self.add(self._toolbar, PAGE_START) if self._toolbar_menu.is_selected() else self.remove(self._toolbar)
            self.auto_resize()
        if Object is self._statusbar_menu:
            self.add(self._statusbar, PAGE_END) if self._statusbar_menu.is_selected() else self.remove(self._statusbar)
            self.auto_resize()
        """
        if command == CMD_LOAD_SETTINGS:
            self._device.load_setup()
        elif command == CMD_CLEAR_ALL_STREAMS:
            self._device.remote_clear_streams()
        elif command == CMD_PAUSE_ALL_STREAMS:
            self._device.remote_pause_streams()
        elif command == CMD_CONTINUE_ALL_STREAMS:
            self._device.remote_continue_streams()
        elif command == CMD_SAVE_STREAMS:
            self._device.remote_save_streams()
        elif command == CMD_LOAD_STREAMS:
            self._device.remote_load_streams()
        elif command == CMD_SEND_PING:
            self._device.remote_ping_device()
        elif command == CMD_CLEAR_ALL_STREAMS:
            self._device.remote_clear_streams()
        elif command == CMD_CLEAR_ALL_STREAMS:
            self._device.remote_clear_streams()
        elif command == CMD_LOCK_ALL:
            for component in self._display.get_components():
                if isinstance(component, ComponentView):
                    component.set_moveable(False)
        elif command == CMD_UNLOCK_ALL:
            for component in self._display.get_components():
                if isinstance(component, ComponentView):
                    component.set_moveable(True)
        elif command == CMD_DISPLAY_ALL_NAMES:
            for component in self._display.get_components():
                if isinstance(component, ComponentView):
                    component.show_name(True)
        elif command == CMD_HIDE_ALL_NAMES:
            for component in self._display.get_components():
                if isinstance(component, ComponentView):
                    component.show_name(False)

    def make_streams_menu(self) -> tk.Menu:
        """ "make dropdown menu for the stream functions (clear, pause, continue)" """
        menu_button = tk.Menubutton(self._frame, text="Streams")
        menu = tk.Menu(menu_button, tearoff=False)

        menu.add_command(label="Clear all streams", command=lambda x: self.run_command(CMD_CLEAR_ALL_STREAMS))
        menu.add_command(label="Pause all streams", command=lambda x: self.run_command(CMD_PAUSE_ALL_STREAMS))
        menu.add_command(label="Continue all streams", command=lambda x: self.run_command(CMD_CONTINUE_ALL_STREAMS))
        menu.add_command(label="Save streams", command=lambda x: self.run_command(CMD_SAVE_STREAMS))
        menu.add_command(label="Load streams", command=lambda x: self.run_command(CMD_LOAD_STREAMS))
        return menu

    def make_device_menu(self) -> tk.Menu:
        menu_button = tk.Menubutton(self._frame, text="Device")
        menu = tk.Menu(menu_button, tearoff=False)

        menu.add_command(label="Send Ping", command=lambda x: self.run_command(CMD_SEND_PING))
        return menu

    def make_data_menu(self) -> tk.Menu:
        menu_button = tk.Menubutton(self._frame, text="Data")
        menu = tk.Menu(menu_button, tearoff=False)

        menu.add_command(label="Load all settings", command=lambda x: self.run_command(CMD_LOAD_SETTINGS))
        return menu

    def make_tools_menu(self) -> tk.Menu:
        menu_button = tk.Menubutton(self._frame, text="Tools")
        menu = tk.Menu(menu_button, tearoff=False)
        return menu

    def make_components_menu(self) -> tk.Menu:
        menu_button = tk.Menubutton(self._frame, text="Components")
        menu = tk.Menu(menu_button, tearoff=False)

        menu.add_command(label="Unlock all", command=lambda x: self.run_command(CMD_UNLOCK_ALL))
        menu.add_command(label="Lock all", command=lambda x: self.run_command(CMD_LOCK_ALL))
        menu.add_command(label="Display all names", command=lambda x: self.run_command(CMD_DISPLAY_ALL_NAMES))
        menu.add_command(label="hide all names", command=lambda x: self.run_command(CMD_HIDE_ALL_NAMES))
        menu.add_command(label="Show all", command=lambda x: self.run_command(CMD_SEND_PING))
        menu.add_separator()
        for i in range(self._device.get_component_count()):
            component_name = self._device.get_component(i).get_component_name()
            menu.add_command(label=component_name, command=lambda x: self.run_command(CMD_SEND_PING))
        return menu

    # def make_menu_item(self, text: str, command: str) -> "tk.MenubuttonItem":
    # def make_checkbox_menu_item(self, text: str, command: str) -> "JCheckBoxMenuItem":

    def add_value(self, view: "ValueView") -> None:
        self._display.add(view)

    def add_component(self, view: ComponentView, x_pos: int = 0, y_pos: int = 0) -> None:
        # view._frame.configure(width=100, height=100)
        view._frame.place(x=x_pos, y=y_pos)

    def add_component_at_right(self, prev_view: ComponentView, view: ComponentView, x_pos: int, y_pos: int) -> None:
        if prev_view is not None:
            x_pos += prev_view.get_view_width() + prev_view.get_x()
            y_pos += prev_view.get_y()
        # self._display.add(view)
        view._frame.place(x=x_pos, y=y_pos)

    def add_component_at_bottom(self, prev_view: ComponentView, view: ComponentView, x_pos: int, y_pos: int) -> None:
        if prev_view is not None:
            x_pos += prev_view.get_x()
            y_pos += prev_view.get_view_height() + prev_view.get_y()
        # self._display.add(view)
        view._frame.place(x=x_pos, y=y_pos)

    def get_frame(self):
        return self._form

    def auto_resize(self) -> None:
        raise ValueError("WIP")
        """
        int index;
        Component[] components;
        int height;
        height = (int) this.getContentPane().getLocation().getY();
        height += 100;
        components = this.getContentPane().getComponents();
        for (index = 0; index < components.length; index++)
        {
            if (components[index].isVisible())
                height+=components[index].getHeight();
        }
        this.setSize(componentPanel.getWidth()+110,height+60);
        """
