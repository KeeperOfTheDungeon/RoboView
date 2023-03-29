
from tkinter import Frame
import customtkinter as ctk
from RoboView.Gui.InternalWindow.InternalWindow import InternalWindow
from RoboView.Robot.Device.Viewer.StatusBar import StatusBar
from RoboView.Robot.Device.Viewer.ToolBar import ToolBar


class DeviceView(InternalWindow):
    def __init__(self, name, device, window_bar):

        self._tool_bar = None
        self._display = None
        self._status_bar = None
        self._device = device
        self._frame = None

        InternalWindow.__init__(self, name, window_bar)

        self._tool_bar = ToolBar(self._frame, device)
        self._display = Frame(self._frame, bg="gray", borderwidth=1)
        self._status_bar = StatusBar(self._frame, device)
        

    def resize_window(self):
        InternalWindow.resize_window(self)
        self._frame.update()
        x_size = self._frame.winfo_width()
        y_size = self._frame.winfo_height()

        if self._status_bar is not None:
            self._status_bar._frame.place(
                height=50, width=x_size - 24, x=0, y=y_size - 50)

        if self._tool_bar is not None:
            self._tool_bar._frame.place(height=37, width=x_size, x=0, y=24)

        if self._display is not None:
            self._display.place(height=y_size - 90,
                                width=x_size - 3, x=1, y=65)
        
            

    def set_robot(self, robot):
        pass




"""package de.hska.lat.robot.device.viewer;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JCheckBoxMenuItem;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JPanel;
import javax.swing.border.LineBorder;

import de.hska.lat.robot.device.RobotDevice;

import de.hska.lat.robot.component.view.ComponentView;

import de.hska.lat.robot.displayFrame.DisplayFrame;
import de.hska.lat.robot.value.view.ValueView;

public class DeviceView extends DisplayFrame implements ActionListener
{

	private static final long serialVersionUID = -4516474419659312074L;
	private static final String STRING_TOOLS = "Tools";

	

	private static final String STRING_DATA = "Data";
	private static final String STRING_LOAD_ALL_SETTINGS = "Load all settings";
	
	private static final String CMD_LOAD_SETTINGS = "cmdGetSetup";
	

	private static final String DEVICE_STRING = "Device";
	private static final String SEND_PING_TEXT = "Send Ping";
	
	private static final String CMD_SEND_PING = "cmdSendPing";
	private static final String CMD_UNLOCK_ALL = "cmdUnlockAll";
	private static final String CMD_LOCK_ALL = "cmdLockAll";
	private static final String CMD_DISPLAY_ALL_NAMES = "cmdDisplayAllNames";
	private static final String CMD_HIDE_ALL_NAMES = "cmdHideAllNames";

	private static final String COMPONENTS_STRING = "Components";
	private static final String SHOW_ALL = "show all";
	
	protected static final String STREAMS_TEXT = "Streams";
	protected static final String CLEAR_ALL_STREAMS_TEXT = "Clear all streams";
	protected static final String PAUSE_ALL_STREAMS_TEXT = "Pause all streams";
	protected static final String CONTINUE_ALL_STREAMS_TEXT = "Continue all streams";
	protected static final String SAVE_STREAMS_TEXT = "Save streams";
	protected static final String LOAD_STREAMS_TEXT = "Load streams";
	
	
	protected static final String CMD_CLEAR_ALL_STREAMS = "cmdClearAllStreams";
	protected static final String CMD_PAUSE_ALL_STREAMS = "cmdPauseAllStreams";
	protected static final String CMD_CONTINUE_ALL_STREAMS = "cmdContinueAllStreams";
	protected static final String CMD_SAVE_STREAMS = "cmdSaveStreams";
	protected static final String CMD_LOAD_STREAMS = "cmdLoadStreams";
	
	protected static final String UNLOCK_ALL_TEXT = "unloock all";
	protected static final String LOCK_ALL_TEXT = "loock all";
	protected static final String DISPLAY_ALL_NAMES_TEXT = "display all names";
	protected static final String HIDE_ALL_NAMES_TEXT = "hide all names";
	
	protected JMenuBar menuBar = new JMenuBar();
	protected ToolBar toolBar;
	protected StatusBar statusBar;
	protected JPanel componentPanel;
	
	
	
	private JCheckBoxMenuItem toolBarMenue;
	private JCheckBoxMenuItem statusBarMenue;
	
	protected RobotDevice<?,?> device;
	
	
	
public DeviceView()
{
	super("generic",true,true,true,true);

}
	
	
public DeviceView(RobotDevice<?,?> device)
{
		
	super(device.getName(),true,true,true,true);

	
	setDevice("", device);
	
}

protected void setDevice(String robotName, RobotDevice<?,?> device)
{
	this.setName(device.getName()+"("+robotName+")");
	this.setTitle(device.getName()+"("+robotName+")");
	displayWindow(robotName, device);
}


protected void displayWindow(String robotName, RobotDevice<?,?> device)
{
	
	this.device = device;
	buildPanel();
	buildMainMenu();

	toolBar = new ToolBar();
	toolBar.setListener(device);
	this.add(toolBar, BorderLayout.PAGE_START);
	this.toolBar.setAquisators(device.getAquisators());
	
	statusBar= new StatusBar(device);
	this.add(statusBar, BorderLayout.PAGE_END);
		
	this.componentPanel = new JPanel();
	this.componentPanel.setLayout(null);
	this.componentPanel.setBorder(new LineBorder(Color.BLACK));
	this.add(this.componentPanel, BorderLayout.CENTER);
	
	show();
}


private void buildPanel() 
{
}


protected void makeErrorDisplay(String name)
{
	this.setTitle("name - device not found");
	this.setSize(100,100);
	this.toFront();
}


/**
 * Adds Dropdown Menus
 */
protected void buildMainMenu()
{
	this.menuBar.add(this.makeStreamsMenu());
	this.menuBar.add(this.makeDeviceMenu());
	this.menuBar.add(this.makeDataMenu());
	this.menuBar.add(this.makeToolsMenu());
	this.menuBar.add(this.makeComponentsMenu());
	this.setJMenuBar(this.menuBar);	
}


/**
 * make dropdown menu for the stream functions (clear, pause, continue)
 * @return
 */
public JMenu makeStreamsMenu()
{
	JMenu	tmpMenu;
	
	tmpMenu = new JMenu(STREAMS_TEXT);
	tmpMenu.add(makeMenuItem(DeviceView.CLEAR_ALL_STREAMS_TEXT, DeviceView.CMD_CLEAR_ALL_STREAMS));
	tmpMenu.add(makeMenuItem(DeviceView.PAUSE_ALL_STREAMS_TEXT, DeviceView.CMD_PAUSE_ALL_STREAMS));
	tmpMenu.add(makeMenuItem(DeviceView.CONTINUE_ALL_STREAMS_TEXT, DeviceView.CMD_CONTINUE_ALL_STREAMS));
	tmpMenu.add(makeMenuItem(DeviceView.SAVE_STREAMS_TEXT, DeviceView.CMD_SAVE_STREAMS));
	tmpMenu.add(makeMenuItem(DeviceView.LOAD_STREAMS_TEXT, DeviceView.CMD_LOAD_STREAMS));
	tmpMenu.addActionListener(this);
	return(tmpMenu);
}

/**
 * Generate dropdown menu "Device"
 * @return
 */
public JMenu makeDeviceMenu()
{
	JMenu	tmpMenu;
	
	tmpMenu = new JMenu(DEVICE_STRING);
	tmpMenu.add(makeMenuItem(DeviceView.SEND_PING_TEXT, DeviceView.CMD_SEND_PING));
	tmpMenu.addActionListener(this);
	return(tmpMenu);
}

/**
 * Generate dropdown menu "Data"
 * @return
 */
public JMenu makeDataMenu()
{
	JMenu	tmpMenu;
	
	tmpMenu = new JMenu(STRING_DATA);
	tmpMenu.add(makeMenuItem(DeviceView.STRING_LOAD_ALL_SETTINGS, DeviceView.CMD_LOAD_SETTINGS));
	tmpMenu.addActionListener(this);
	return(tmpMenu);
}

/**
 * Generate dropdown menu "Tools"
 * @return
 */
public JMenu makeToolsMenu()
{
	JMenu	tmpMenu;
	tmpMenu = new JMenu(STRING_TOOLS);
	return(tmpMenu);
}

/**
 * Generate dropdown menu "Components"
 * @return
 */
public JMenu makeComponentsMenu()
{
	JMenu	tmpMenu;
	JMenuItem	tmpMenuItem;
	
	tmpMenu = new JMenu(COMPONENTS_STRING);
	int index;
	
	tmpMenu.add(makeMenuItem(DeviceView.UNLOCK_ALL_TEXT, DeviceView.CMD_UNLOCK_ALL));
	tmpMenu.add(makeMenuItem(DeviceView.LOCK_ALL_TEXT, DeviceView.CMD_LOCK_ALL));
	tmpMenu.add(makeMenuItem(DeviceView.DISPLAY_ALL_NAMES_TEXT, DeviceView.CMD_DISPLAY_ALL_NAMES));
	tmpMenu.add(makeMenuItem(DeviceView.HIDE_ALL_NAMES_TEXT, DeviceView.CMD_HIDE_ALL_NAMES));
	
	tmpMenu.add(makeMenuItem(DeviceView.SHOW_ALL, DeviceView.CMD_SEND_PING));
	tmpMenu.addSeparator();
	

	
	
	for (index=0; index<device.getComponentCount(); index++)
	{
		tmpMenuItem = makeMenuItem(device.getCopmonent(index).getComponentName(), DeviceView.CMD_SEND_PING);
		
		tmpMenu.add(tmpMenuItem);
		
	}
	
//	tmpMenu.add(toolBarMenue=makeCheckBoxMenuItem(STRING_TOOLBAR,STRING_TOOLBAR));
//	tmpMenu.add(statusBarMenue=makeCheckBoxMenuItem(STRING_STATUSBAR,STRING_STATUSBAR));
	
	return(tmpMenu);
}


JMenuItem makeMenuItem(String MenuItemText,String ActionCommand)
{
	JMenuItem TmpItem;
	
	TmpItem = new JMenuItem(MenuItemText);
	TmpItem.setActionCommand(ActionCommand);
	TmpItem.addActionListener(this);
	return(TmpItem);
}


JCheckBoxMenuItem makeCheckBoxMenuItem(String MenuItemText,String ActionCommand)
{
	JCheckBoxMenuItem TmpItem;
	
	TmpItem = new JCheckBoxMenuItem(MenuItemText);
	TmpItem.setActionCommand(ActionCommand);
	TmpItem.addActionListener(this);
	return(TmpItem);
	
}


protected void addValue(ValueView<?> view)
{
	
	this.componentPanel.add(view);
	
}


protected void addComponent(ComponentView component)
{
	
	this.componentPanel.add(component);
	
}


protected void addComponent(ComponentView view,int xPos,int yPos)
{
	
	componentPanel.add(view);
	view.setLocation(xPos,yPos);
}


protected void addComponentAtRight(ComponentView previousView ,ComponentView view,int xPos,int yPos)
{
	
	if (previousView != null)
	{
		xPos+=previousView.getWidth()+previousView.getX();
		yPos+=previousView.getY();
	}
	componentPanel.add(view);
	view.setLocation(xPos,yPos);

}


protected void addComponentAtBottom(ComponentView previousView ,ComponentView view,int xPos,int yPos)
{

	if (previousView != null)
	{
		xPos+=previousView.getX();
		yPos+=previousView.getHeight()+previousView.getY();
	}
	
	
	componentPanel.add(view);
	view.setLocation(xPos,yPos);
	
}


public void autoResize()
{
	int index;
	Component[] components;
	int height;
	
//	calculateComponentPanelSize();
	
	height = (int) this.getContentPane().getLocation().getY();
	
	height += 100;
	
	components = this.getContentPane().getComponents();
	for (index = 0; index < components.length; index++)
	{
		if (components[index].isVisible())
			height+=components[index].getHeight();
		
		//System.out.println(components[index].getHeight());
	}
	this.setSize(componentPanel.getWidth()+110,height+60);
}


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
