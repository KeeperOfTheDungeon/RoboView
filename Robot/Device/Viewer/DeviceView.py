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





class DeviceView(InternalWindow):
    FRAME_NAME: str = "generic DeviceView"

    CMD_SEND_PING: str = "cmdSendPing"

    def __init__(self, root: ctk.CTkFrame, device: RobotDevice, window_bar: WindowBar):
        menu_bar: "tk.MenubuttonBar"
        self._toolbar: ToolBar = None
        self._component_panel: tk.TkFrame
        self._display = None
        super().__init__(root, self.FRAME_NAME, window_bar)
        self._display = tk.Frame(self._frame, bg="gray", borderwidth=1)
        self._statusbar: StatusBar = StatusBar(self._frame, device)
        self._device: RobotDevice
        self.set_device("generic", device)


        self._tool_bar_menu: "JCheckBoxMenuItem"
        self._status_bar_menu: "JCheckBoxMenuItem"

        # ----


        self.set_min_dimension(600, 400)

    def set_device(self, robot_name: str, device: RobotDevice) -> None:
        name = f"{device.get_name()}({robot_name})"
        self.rename(name)
        self.display_window(robot_name, device)

    def display_window(self, robot_name: str, device: RobotDevice) -> None:
        self._device = device
        # self.build_main_menu()
        mb = self.make_streams_menu()
        mb.place()

        self._toolbar = ToolBar(self._frame, device)
        # self._toolbar.set_listener(device)
        # add to page start
        # self._toolbar.set_aquisators(device.get_aquisators())

        self._component_panel = tk.Frame(self._frame, bg="yellow", borderwidth=1)
        # add to center with black border

        self.show_window()

    def make_error_display(self, name: str) -> None:
        self.set_title("name - device not found")
        self.set_size(100, 100)
        self.to_front()

    def build_main_menu(self) -> None:
        """ "Adds Downdown Menus" """
        self._menubar.add(self.make_streams_menu())
        self._menubar.add(self.make_device_menu())
        self._menubar.add(self.make_data_menu())
        self._menubar.add(self.make_tools_menu())
        self._menubar.add(self.make_components_menu())
        self.set_menubar(self._menubar)

    def make_streams_menu(self) -> tk.Menu:
        """ "make dropdown menu for the stream functions (clear, pause, continue)" """
        menu_button = tk.Menubutton(self._frame, text="Streams")
        menu = tk.Menu(menu_button, tearoff=False)
        def run_command(command: str) -> None:
            print(command)
        menu.add_command(label="Clear all streams", command=lambda x: run_command("cmdClearAllStreams"))
        menu.add_command(label="Pause all streams", command=lambda x: run_command("cmdPauseAllStreams"))
        menu.add_command(label="Continue all streams", command=lambda x: run_command("cmdContinueAllStreams"))
        menu.add_command(label="Save streams", command=lambda x: run_command("cmdSaveStreams"))
        menu.add_command(label="Load streams", command=lambda x: run_command("cmdLoadStreams"))
        return menu

    def make_device_menu(self) -> tk.Menubutton:
        menu = tk.Menubutton("Device")
        menu.add(self.make_menu_item("Send Ping", self.CMD_SEND_PING))
        self.add_action_listener(self)
        return menu

    def make_data_menu(self) -> tk.Menubutton:
        menu = tk.Menubutton("Data")
        menu.add(self.make_menu_item("Load all settings", "cmdGetSetup"))
        self.add_action_listener(self)
        return menu

    def make_tools_menu(self) -> tk.Menubutton:
        menu = tk.Menubutton("Tools")
        return menu

    def make_components_menu(self) -> tk.Menubutton:
        menu = tk.Menubutton("Components")
        menu.add(self.make_menu_item("unloock all", "cmdUnlockAll"))
        menu.add(self.make_menu_item("loock all", "cmdLockAll"))
        menu.add(self.make_menu_item("display all names", "cmdDisplayAllNames"))
        menu.add(self.make_menu_item("hide all names", "cmdHideAllNames"))
        menu.add(self.make_menu_item("show all", self.CMD_SEND_PING))
        menu.add_seperator()

        for i in range(self._device.get_component_count()):
            component_name = self._device.get_component(index).get_component_name()
            menu.add(self.make_menu_item(component_name, self.CMD_SEND_PING))

        return menu

    def make_menu_item(self, text: str, command: str) -> "tk.MenubuttonItem":
        item = tk.MenubuttonItem(text)
        item.set_action_command(command)
        item.add_action_listener(self)
        return item

    def make_checkbox_menu_item(self, text: str, command: str) -> "JCheckBoxMenuItem":
        item = JCheckBoxMenuItem(text)
        item.set_action_command(command)
        item.add_action_listener(self)
        return item

    def add_value(self, view: "ValueView") -> None:
        self._component_panel.add(view)

    def add_component(self, view: ComponentView, x_pos: int = 0, y_pos: int = 0) -> None:
        # view._frame.configure(width=100, height=100)
        view._frame.place(x=x_pos, y=y_pos)

    def add_component_at_right(self, prev_view: ComponentView, view: ComponentView, x_pos: int, y_pos: int) -> None:
        raise ValueError("WIP")
        """
        if (previousView != null)
        {
            xPos+=previousView.getWidth()+previousView.getX();
            yPos+=previousView.getY();
        }
        componentPanel.add(view);
        view.setLocation(xPos,yPos);
        """

    def add_component_at_bottom(self, prev_view: ComponentView, view: ComponentView, x_pos: int, y_pos: int) -> None:
        raise ValueError("WIP")
        """
        if (previousView != null)
        {
            xPos+=previousView.getX();
            yPos+=previousView.getHeight()+previousView.getY();
        }
        componentPanel.add(view);
        view.setLocation(xPos,yPos);
        """

    def resize_window(self):
        InternalWindow.resize_window(self)
        self._frame.update()
        x_size = self._frame.winfo_width()
        y_size = self._frame.winfo_height()

        if hasattr(self, "_statusbar") and self._statusbar is not None:
            self._statusbar._frame.configure(height=50, width=x_size - 24)
            self._statusbar._frame.place(x=0, y=y_size - 60)

        if hasattr(self, "_toolbar") and self._toolbar is not None:
            self._toolbar._frame.configure(height=37, width=x_size)
            self._toolbar._frame.place(x=0, y=24)

        if hasattr(self, "_display") and self._display is not None:
            self._display.configure(height=y_size - 90, width=x_size - 3)
            self._display.place(x=1, y=65)

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

"""

@Override
public void actionPerformed(ActionEvent actionEvent)
{
    Object object;
    String cmd;
    
    object = actionEvent.getSource();
    cmd = actionEvent.getActionCommand();
    if (object == toolBarMenue)
    {
        if (toolBarMenue.isSelected())
        {
            this.add(toolBar,BorderLayout.PAGE_START);
        }
        else
        {
            this.remove(toolBar);
        }
        autoResize();
    }
    else if (object == statusBarMenue)
    {
        if (statusBarMenue.isSelected())
        {
            this.add(statusBar,BorderLayout.PAGE_END);
        }
        else
        {
            this.remove(statusBar);
        }
        autoResize();
    }
    else if (cmd.equals(DeviceView.CMD_LOAD_SETTINGS))
    {
        this.device.loadSetup();
    }
    else if (cmd.equals(DeviceView.CMD_CLEAR_ALL_STREAMS))
    {
        this.device.remote_clearAllDataStreams();
    }
    else if (cmd.equals(DeviceView.CMD_PAUSE_ALL_STREAMS))
    {
        this.device.remote_pauseAllDataStreams();
    }
    else if (cmd.equals(DeviceView.CMD_CONTINUE_ALL_STREAMS))
    {
        this.device.remote_continueAllDataStreams();
    }
    else if (cmd.equals(DeviceView.CMD_SAVE_STREAMS))
    {
        this.device.remote_saveStreams();
    }
    else if (cmd.equals(DeviceView.CMD_LOAD_STREAMS))
    {
        this.device.remote_loadStreams();
    }	
    else if (cmd.equals(DeviceView.CMD_SEND_PING))
    {
        this.device.remote_pingDevice();
    }

    else if  (cmd.equals(DeviceView.CMD_LOCK_ALL))
    {
        
        for (Component component : this.componentPanel.getComponents())
        {
            if (component instanceof ComponentView)
            {
                ((ComponentView) component).setMoveable(false);
            }
        }
        
    }

    else if  (cmd.equals(DeviceView.CMD_UNLOCK_ALL))
    {
        
        for (Component component : this.componentPanel.getComponents())
        {
            if (component instanceof ComponentView)
            {
                ((ComponentView) component).setMoveable(true);
            }
        }
        
    }
    else if  (cmd.equals(DeviceView.CMD_DISPLAY_ALL_NAMES))
    {
        for (Component component : this.componentPanel.getComponents())
        {
            if (component instanceof ComponentView)
            {
                ((ComponentView) component).showName(true);
    
            }
        }
    }
        
    else if  (cmd.equals(DeviceView.CMD_HIDE_ALL_NAMES))
    {
        for (Component component : this.componentPanel.getComponents())
        {
            if (component instanceof ComponentView)
            {
                ((ComponentView) component).showName(false);
    
            }
        }
    }
        

    
    
    
}
}
"""
