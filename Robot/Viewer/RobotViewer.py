from time import sleep

import tkinter as tk
import customtkinter as ctk

from RoboView.Robot.Connection.Serial.SerialConnectionView import SerialConnectionView
from RoboView.Robot.Viewer.RobotSettings import RobotSettings
from RoboView.Robot.Viewer.WindowBar import WindowBar
from RoboView.Gui.InternalWindow.WindowState import State


class RobotViewer:

	def __init__(self, robot):
		self._frame = ctk.CTk()
		self._frame.title("Spiderbot")

		RobotSettings.set_file_name(robot.get_name() + ".pkl")
		self._settings_key = self.__class__.__name__

		self._x_pos = 10
		self._y_pos = 10
		self._width = 1424
		self._height = 776

		self._frame.geometry("{}x{}+{}+{}".format(self._width, self._height, self._x_pos, self._y_pos))
		RobotSettings.load_settings()
		RobotSettings.set_key(self._settings_key + ".x_pos", self._x_pos)
		RobotSettings.set_key(self._settings_key + ".y_pos", self._y_pos)
		RobotSettings.set_key(self._settings_key + ".x_size", self._width)
		RobotSettings.set_key(self._settings_key + ".y_size", self._height)

		ctk.set_appearance_mode("light")
		self._robot = robot
		self._window_bar = WindowBar(self._frame)

		self.build_window()

	def build_window(self):

		menu_bar = tk.Menu(self._frame)

		# connection_menue and settings_menue are implemented in this class, others in subclass
		self.make_connection_menue(menu_bar)
		self.make_data_menu(menu_bar)
		self.make_control_menu(menu_bar)
		self.make_setup_menu(menu_bar)
		self.make_settings_menue(menu_bar)

		self._frame.config(menu=menu_bar)
		self.check_open_views()
		self._frame.mainloop()

		"""		
		while(True):
			self._frame.update_idletasks()
			self._frame.update()
			sleep(1)
		"""

		self.load_config()
		pass

	def load_config(self):
		RobotSettings.load_settings()

	def save_config(self):
		RobotSettings.save_settings()

	# TODO camelcase method
	def onOpenConectionWindow(self) -> None:
		self._connectionWindow = SerialConnectionView(self._frame, self._window_bar)
		self._connectionWindow.draw()

	def make_connection_menue(self, menue_bar):
		menue = tk.Menu(menue_bar)
		menue.add_command(label="Serial", command=self.onOpenConectionWindow)
		menue_bar.add_cascade(label="Connection", menu=menue)

	def make_settings_menue(self, menue_bar):
		menue = tk.Menu(menue_bar)
		menue.add_command(label="Load desktop", command=self.load_config)
		menue.add_command(label="Save desktop", command=self.save_config)
		menue_bar.add_cascade(label="Settings", menu=menue)

	def check_open_views(self):
		if self.is_open_view("SerialConnectionView"):
			self.onOpenConectionWindow()
		if self.is_open_view("DataHubDataView"):
			self.show_data_hub_data()
		if self.is_open_view("HeadSensorsDataView"):
			self.show_head_sensors_data()
		if self.is_open_view("LegSensorsDataView"):
			self.show_leg_sensors_data()
		if self.is_open_view("LegControllersDataView"):
			self.show_leg_controller_data()
		if self.is_open_view("LegSensorsControlView"):
			self.show_leg_sensors_control()
		if self.is_open_view("LegControllersControlView"):
			self.show_leg_controller_control()
		if self.is_open_view("LegControllerSetupView"):
			self.show_leg_controller_setup()

	def is_open_view(self, view_name):
		state_value = RobotSettings.get_int("{}.state".format(view_name))
		if state_value == State.INTERNAL.value:
			RobotSettings.set_key("{}.state".format(view_name), State.INIT_INTERNAL.value)
		elif state_value == State.MINIMIZED.value:
			RobotSettings.set_key("{}.state".format(view_name), State.INIT_MINIMIZED.value)
		elif state_value == State.EXTERNAL.value:
			RobotSettings.set_key("{}.state".format(view_name), State.CLOSED.value)
		return state_value == State.INTERNAL.value or state_value == State.MINIMIZED.value


"""
protected JMenu makeConnectionMenu()
{
	JMenu	tmpMenu;
	
	tmpMenu = new JMenu(RobotViewer.MENUE_NAME_CONNECTION);

	
	tmpMenu.add(makeMenuItem(
		RobotViewer.LAN_CONNECTION_TEXT,
		RobotViewer.CMD_SHOW_FRAME+this.addDisplay(LanMasterConnectionView.class.getName())));
	tmpMenu.add(makeMenuItem(
		RobotViewer.CONNECTION_TEXT,
		RobotViewer.CMD_SHOW_FRAME+this.addDisplay(ConnectionView.class.getName())));
	tmpMenu.add(makeMenuItem(
		RobotViewer.BLUETOOTH_CONNECTION_TEXT,
		RobotViewer.CMD_SHOW_FRAME+this.addDisplay(BluetoothConnectionView.class.getName())));	
	tmpMenu.add(makeMenuItem(
		RobotViewer.SERIAL_CONNECTION_TEXT,
		RobotViewer.CMD_SHOW_FRAME+this.addDisplay(SerialConnectionView.class.getName())));	
	tmpMenu.add(makeMenuItem(
		RobotViewer.MENUE_VIEW_PACKET_LOG,
		RobotViewer.CMD_SHOW_FRAME+this.addDisplay(DataPacketLogViewer.class.getName())));
	
	tmpMenu.add(this.makeDataPacketFilterMenu());
	

	
	return(tmpMenu);
}
"""

"""
filemenu = tk.Menu(menubar)
filemenu.add_command(label="Open")
filemenu.add_command(label="Save")
filemenu.add_command(label="Exit")"""
"""
	super(robotName);
	this.settingsKey=this.getClass().getName();

	this.loadConfig();

	this.setContentPane(new JDesktopPane());
	
	this.addWindowListener(this);
	this.setLayout(null);

	this.setBounds(UiSettings.recoverInt(settingsKey + xPositionKey, 10),
			UiSettings.recoverInt(settingsKey + yPositionKey, 10),
			UiSettings.recoverInt(settingsKey + xSizeKey, 600),
			UiSettings.recoverInt(settingsKey + ySizeKey, 600));



	
	this.sheduler = new Timer();
	this.sheduler.scheduleAtFixedRate(new saveSettingsTask(), 100000, 100000);

	
	InputDeviceDiscoverer.discoverJoysticks();
"""

'''
package de.hska.lat.robot.viewer;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowEvent;
import java.awt.event.WindowListener;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.InvalidPropertiesFormatException;
import java.util.Properties;
import java.util.Timer;
import java.util.TimerTask;

import javax.swing.JDesktopPane;
import javax.swing.JFrame;
import javax.swing.JInternalFrame;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.UIManager;
import javax.swing.event.MenuEvent;
import javax.swing.event.MenuListener;

import de.hska.lat.behavior.view.BehaviorViewer;
import de.hska.lat.inputDevice.InputDeviceDiscoverer;
import de.hska.lat.inputDevice.sphero.gui.RobotControlView;
import de.hska.lat.robot.Robot;
import de.hska.lat.robot.RobotSettings;
import de.hska.lat.robot.connection.view.ConnectionView;
import de.hska.lat.robot.connection.bluetooth.view.BluetoothConnectionView;
import de.hska.lat.robot.connection.lan.view.LanMasterConnectionView;
import de.hska.lat.robot.connection.serial.view.SerialConnectionView;
import de.hska.lat.robot.control.JoystickTestView;
import de.hska.lat.robot.device.RobotDevice;





import de.hska.lat.robot.dataPacketLogger.filter.viewer.DataPacketFilterEditor;
import de.hska.lat.robot.dataPacketLogger.viewer.DataPacketLogViewer;
import de.hska.lat.robot.dataViewer.recorder.ValueRecorderView;
import de.hska.lat.robot.device.generic.dataHub.view.DataHubDataView;
import de.hska.lat.robot.device.viewer.DeviceView;
import de.hska.lat.robot.displayFrame.DisplayFrame;
import de.hska.lat.robot.editor3d.EditorMainFrame;
import de.hska.lat.robot.morphology.appearance.Editor3D.Editor3DFrame;
import de.hska.lat.robot.morphology.model.viewer.MorphologicModelViewer;
import de.hska.lat.robot.pose.view.PoseDataView;
import de.hska.lat.robot.pose.view.PoseControlView;
import de.hska.lat.robot.tools.sharpIr.SharpIrCalculator;
import de.hska.lat.robot.ui.settings.UiSettings;
import de.hska.lat.robot.valueScope.ValueScopeView;

public abstract class RobotViewer extends JFrame implements ActionListener,
MenuListener, WindowListener {


	/**
	* 
	*/
	private static final long serialVersionUID = -7359600953948628400L;
	
	
	protected Robot robot;
	protected JMenuBar menuBar = new JMenuBar();

	
	protected static final String CMD_NEW_ROBOT = "cmdNewRobot";
	protected static final String CMD_OPEN_ROBOT = "cmdOpenRobot";
	protected static final String CMD_SAVE_ROBOT = "cmdSaveRobot";

	
	protected static final String CMD_SHOW_FRAME = "cmdShowFrame";

	private static final String START_EMULATOR_TEXT = "start emulator";
	private static final String START_INTERNAL_EMULATOR_TEXT = "start internal emulator";

	private static final String CMD_START_EMULATOR = "cmdStartEmulator";
	private static final String CMD_START_INTERNAL_EMULATOR = "cmdStartIntermalEmulator";

	
	private static final String CMD_SAVE_SETTINGS  = "cmdSaveSettings";
	
	protected static final String PARROT_CONNECTION_TEXT		= "parrot";
	protected static final String LAN_CONNECTION_TEXT = "w-lan";
	protected static final String SERIAL_CONNECTION_TEXT = "serial";
	protected static final String CONNECTION_TEXT = "connection";
	protected static final String BLUETOOTH_CONNECTION_TEXT = "bluetooth";

	
	protected static final String FILTER_TEXT = "filter";
	protected static final String EDIT_TEXT = "edit";
	
	
	private static final String POSE_TEXT = "pose";

	protected static final String DATA_HUB_TEXT = "data hub";
	

	
	protected static final String SETTINGS_TEXT = "settings";
	protected static final String SAVE_TEXT = "save";

	protected static final String DATA_TEXT = "data";


	protected static final String xPositionKey = ".xPosition";
	protected static final String yPositionKey = ".yPosition";

	protected static final String xSizeKey = ".xSize";
	protected static final String ySizeKey = ".ySize";

	protected String settingsKey;
	
	
	
	protected static final String MENUE_NAME_ROBOT 		= Robot
	protected static final String MENUE_NAME_NEW 		= new;
	protected static final String MENUE_NAME_OPEN	 	= open";
	protected static final String MENUE_NAME_SAVE	 	= save";
	
	
	protected static final String MENUE_FILTER	 		= filter";
	
	protected static final String MENUE_NAME_BEHAVIOR	= behavior";	
	protected static final String MENUE_NAME_SHOW_BEHAVIOR = "show";
	
	
	protected static final String CMD_SHOW_BEHAVIOR		= "cmdShowBehavior";
	
	/*********** old **************/


	private static final String CMD_VIEW_SHARP_IR_CALCULATOR = "cmdsharpIrCalculator";

	private static final String STRG_MENU_TOOLS = "Tools";
	private static final String CMD_SHOW_WINDOWS = "showWindows";

	private static final String STRG_VIEW_SHARP_IR_CALCULATOR = "sharp Ir Calculator";

	//private static final String STRG_VIEW_FOV = "field of view";

	// private static final String STRG_VIEW_FOV = "field of view";

	DataPacketLogViewer dataPacketlogViewer;
	

	
	
	
	protected static final String MENUE_NAME_CONTROL = "control";
	protected static final String MENUE_NAME_SETUP = "setup";
	protected static final String MENUE_NAME_DATA = "data";
	
	protected static final String MENUE_NAME_VALUE = "value";
	protected static final String MENUE_VALUE_RECORDER = "value recorder";
	protected static final String MENUE_VALUE_GENERATOR = "value generator";
	protected static final String MENUE_VALUE_SCOPE = "value scope";
	
	
	protected static final String MENUE_NAME_PERCEPTION = "perception";
	protected static final String MENUE_NAME_CONNECTION = "connection";
	
	protected static final String STRG_3D_EDITOR_TEXT	= "3D Editor";

	
	protected static final String MENUE_NAME_MORPHOLOGY = "morphology";
	protected static final String MENUE_NAME_MORPHOLOGY_VIEW = "view";
	
	protected static final String JOYSTICK_TEST_TEXT = "Test Joystick";

	protected static final String MENUE_NAME_FIELD_OF_VIEW = "field of view";

	
	protected static final String MENUE_VIEW_PACKET_LOG = "view packet log";
	
	//protected DisplayFrame[] frames;

	protected ArrayList<String> displayClassList = new ArrayList<String>();
	// protected ArrayList<Class<DisplayFrame>> displayList = new
	// ArrayList<Class<DisplayFrame>>();

	protected Properties preferences = new Properties();

	protected static final String configurationPath = "config";
	protected static final String configurationFile = configurationPath
			+ "/ui.cfg";


	static {
		try {
//			 UIManager.setLookAndFeel( UIManager.getSystemLookAndFeelClassName() );
			UIManager.setLookAndFeel("com.sun.java.swing.plaf.nimbus.NimbusLookAndFeel");
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	
	
	private Timer sheduler;
	
public RobotViewer(String robotName)
{

	super(robotName);
	this.settingsKey=this.getClass().getName();

	this.loadConfig();

	this.setContentPane(new JDesktopPane());
	
	this.addWindowListener(this);
	this.setLayout(null);

	this.setBounds(UiSettings.recoverInt(settingsKey + xPositionKey, 10),
			UiSettings.recoverInt(settingsKey + yPositionKey, 10),
			UiSettings.recoverInt(settingsKey + xSizeKey, 600),
			UiSettings.recoverInt(settingsKey + ySizeKey, 600));



	
	this.sheduler = new Timer();
	this.sheduler.scheduleAtFixedRate(new saveSettingsTask(), 100000, 100000);

	
	InputDeviceDiscoverer.discoverJoysticks();
	
	//
}

	protected void loadConfig() {

		FileInputStream fis;
		try {
			File configPath = new File(configurationPath);
			if (!configPath.exists()) {
				configPath.mkdir();
			}

			File f = new File(configurationFile);
			if (!f.exists()) {

				f.createNewFile();
				preferences.storeToXML(new FileOutputStream(configurationFile),
						this.getName() + " configuration");
			}

			fis = new FileInputStream(configurationFile);
			preferences.loadFromXML(fis);
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (InvalidPropertiesFormatException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		UiSettings.setPreferences(preferences);
	}


	
	
public void setRobot(Robot robot)
{
	this.robot=robot;
	this.makeMenuBar();
	
	this.openSavedViews();
	
	this.repaint();
}


public Robot getRobot()
{
	return(this.robot);
}







void makeMenuBar()
{
	
	this.menuBar.add(this.makeRobotMenu());
	this.menuBar.add(this.makeDataMenu());
	this.menuBar.add(this.makeControlMenu());
	this.menuBar.add(this.makeSetupMenu());
	
	this.menuBar.add(this.makeConnectionMenu());
	this.menuBar.add(this.makeValueMenu());
	this.menuBar.add(this.makePerceptionMenu());
	
	this.menuBar.add(this.makeMorphologyMenu());
	
	this.menuBar.add(this.makeToolsMenue());
	this.menuBar.add(this.makeWindowsMenue());
	this.menuBar.add(this.makeBehaviorMenu());
	
	this.menuBar.add(this.makeSettingsMenu());
	
	this.menuBar.add(this.makeRobotControlMenu());
	this.setJMenuBar(this.menuBar);			

		
}

protected JMenu makeRobotControlMenu()
{
	JMenu tmpMenu;
	
	tmpMenu = new JMenu("RobotControl");
	tmpMenu.add(makeMenuItem("Scan Window", RobotViewer.CMD_SHOW_FRAME+this.addDisplay(RobotControlView.class.getName())));
	return (tmpMenu);
}


protected JMenu makeRobotMenu()
{
	JMenu	tmpMenu;
	
	tmpMenu = new JMenu(RobotViewer.MENUE_NAME_ROBOT);
	tmpMenu.add(makeMenuItem(RobotViewer.MENUE_NAME_NEW,RobotViewer.CMD_NEW_ROBOT));
	tmpMenu.add(makeMenuItem(RobotViewer.MENUE_NAME_OPEN,RobotViewer.CMD_OPEN_ROBOT));
	tmpMenu.add(makeMenuItem(RobotViewer.MENUE_NAME_SAVE,RobotViewer.CMD_SAVE_ROBOT));
	
	return(tmpMenu);
}



protected JMenu makeSettingsMenu()
{
	JMenu	tmpMenu;
	
	tmpMenu = new JMenu(RobotViewer.SETTINGS_TEXT);
	tmpMenu.add(makeMenuItem(RobotViewer.SAVE_TEXT,RobotViewer.CMD_SAVE_SETTINGS));
	return(tmpMenu);
}


protected JMenu makeControlMenu()
{
	JMenu	tmpMenu;
	
	tmpMenu = new JMenu(RobotViewer.MENUE_NAME_CONTROL);
	tmpMenu.add(makeMenuItem(RobotViewer.POSE_TEXT,RobotViewer.CMD_SHOW_FRAME+this.addDisplay(PoseControlView.class.getName())));
	return(tmpMenu);
}



protected JMenu makeDataPacketFilterMenu()
{
	
	JMenu	tmpMenu;
	
	tmpMenu = new JMenu(RobotViewer.MENUE_FILTER);
	
	tmpMenu.add(makeMenuItem(RobotViewer.EDIT_TEXT,
				RobotViewer.CMD_SHOW_FRAME+this.addDisplay(DataPacketFilterEditor.class.getName())));

	return(tmpMenu);
}


protected JMenu makeSetupMenu()
{
	JMenu	tmpMenu;
	
	tmpMenu = new JMenu(RobotViewer.MENUE_NAME_SETUP);
	
	
	return(tmpMenu);
}


protected JMenu makePerceptionMenu()
{
	JMenu	tmpMenu;
	
	tmpMenu = new JMenu(RobotViewer.MENUE_NAME_PERCEPTION);

	return(tmpMenu);
}


protected JMenu makeFieldOfViewMenu()
{
	JMenu	tmpMenu;
	
	tmpMenu = new JMenu(RobotViewer.MENUE_NAME_FIELD_OF_VIEW);

	return(tmpMenu);
}


protected JMenu makeAreaViewMenu()
{
	JMenu	tmpMenu;
	
	tmpMenu = new JMenu(RobotViewer.MENUE_NAME_PERCEPTION);

	return(tmpMenu);
}

protected JMenu makeBehaviorMenu()
{
	JMenu	tmpMenu;
	
	tmpMenu = new JMenu(RobotViewer.MENUE_NAME_BEHAVIOR);
	tmpMenu.add(makeMenuItem(RobotViewer.MENUE_NAME_SHOW_BEHAVIOR,RobotViewer.CMD_SHOW_BEHAVIOR));

//BehaviorViewer
	//MENUE_NAME_SHOW_BEHAVIOR
	return(tmpMenu);
}



protected JMenu makeDataMenu()
{
	JMenu	tmpMenu;
	
	tmpMenu = new JMenu(RobotViewer.MENUE_NAME_DATA);
	tmpMenu.add(makeMenuItem(RobotViewer.POSE_TEXT,RobotViewer.CMD_SHOW_FRAME+this.addDisplay(PoseDataView.class.getName())));

	return(tmpMenu);
}



protected JMenu makeMorphologyMenu()
{
	JMenu	tmpMenu;
	
	tmpMenu = new JMenu(RobotViewer.MENUE_NAME_MORPHOLOGY);
	tmpMenu.add(makeMenuItem(RobotViewer.MENUE_NAME_MORPHOLOGY_VIEW,RobotViewer.CMD_SHOW_FRAME+this.addDisplay(MorphologicModelViewer.class.getName())));

	return(tmpMenu);
}


protected JMenu makeValueMenu()
{
	JMenu	tmpMenu;
	
	tmpMenu = new JMenu(RobotViewer.MENUE_NAME_VALUE);
	tmpMenu.add(makeMenuItem(RobotViewer.MENUE_VALUE_RECORDER,RobotViewer.CMD_SHOW_FRAME+this.addDisplay(ValueRecorderView.class.getName())));
	tmpMenu.add(makeMenuItem(RobotViewer.MENUE_VALUE_GENERATOR,RobotViewer.CMD_SHOW_FRAME+this.addDisplay(PoseDataView.class.getName())));
	tmpMenu.add(makeMenuItem(RobotViewer.MENUE_VALUE_SCOPE,RobotViewer.CMD_SHOW_FRAME+this.addDisplay(ValueScopeView.class.getName())));

	return(tmpMenu);
}

/*
* 	protected static final String MENUE_NAME_VALUE = "value";
	protected static final String MENUE_VALUE_RECORDER = "value recorder";
	protected static final String MENUE_VALUE_GENERATOR = "value generator";
	protected static final String MENUE_VALUE_SCOPE = "value scope";
*/



protected JMenu makeViewMenu(String name,String commandPrefix)
{
	int counter;
	JMenu	tmpMenu;
	
	tmpMenu = new JMenu(name);
	
	for (counter=0; counter<robot.getDeviceCount();counter++)
	{
	//	if (robot.getDevice(counter).hasView(type))
		{
//			tmpMenu.add(makeMenuItem(robot.getDevice(counter).getDeviceName(),
						commandPrefix+robot.getDevice(counter).getDeviceName()));			
		}

	}

	return(tmpMenu);
}






JMenu makeToolsMenue()
{

	JMenu	tmpMenu;
	
	tmpMenu = new JMenu(RobotViewer.STRG_MENU_TOOLS);
	
	tmpMenu.add(makeMenuItem(RobotViewer.STRG_VIEW_SHARP_IR_CALCULATOR,RobotViewer.CMD_VIEW_SHARP_IR_CALCULATOR));		

	tmpMenu.add(makeMenuItem(RobotViewer.START_EMULATOR_TEXT,RobotViewer.CMD_START_EMULATOR));
	tmpMenu.add(makeMenuItem(RobotViewer.START_INTERNAL_EMULATOR_TEXT, RobotViewer.CMD_START_INTERNAL_EMULATOR));
	tmpMenu.add(makeMenuItem(RobotViewer.STRG_3D_EDITOR_TEXT,RobotViewer.CMD_SHOW_FRAME+this.addDisplay(EditorMainFrame.class.getName())));
	tmpMenu.add(makeMenuItem(RobotViewer.STRG_3D_EDITOR_TEXT,RobotViewer.CMD_SHOW_FRAME+this.addDisplay(Editor3DFrame.class.getName())));
	
	tmpMenu.add(makeMenuItem(RobotViewer.JOYSTICK_TEST_TEXT,RobotViewer.CMD_SHOW_FRAME+this.addDisplay(JoystickTestView.class.getName())));
	//
	return(tmpMenu);
	
}




JMenu makeWindowsMenue()
{
	JMenu	tmpMenu;
	
	tmpMenu = new JMenu("Windows");
	tmpMenu.setActionCommand(RobotViewer.CMD_SHOW_WINDOWS);
	tmpMenu.addMenuListener(this);
	
	return(tmpMenu);
}



protected JMenuItem makeMenuItem(String MenuItemText,String ActionCommand)
{
	JMenuItem TmpItem;
	
	TmpItem = new JMenuItem(MenuItemText);
	TmpItem.setActionCommand(ActionCommand);
	TmpItem.addActionListener(this);
	return(TmpItem);
}




protected void saveBounds()
{
	UiSettings.saveInt(this.settingsKey+xPositionKey, this.getX());
	UiSettings.saveInt(this.settingsKey+yPositionKey, this.getY());
	UiSettings.saveInt(this.settingsKey+xSizeKey, this.getWidth());
	UiSettings.saveInt(this.settingsKey+ySizeKey, this.getHeight());
}










/************************ standard menues ************************************/

protected JMenuItem addDataHubDataView()
{
	return(makeMenuItem(DATA_HUB_TEXT,CMD_SHOW_FRAME+this.addDisplay(DataHubDataView.class.getName())));
}











public int addDisplay(String className)
{
	this.displayClassList.add(className);
	return(this.displayClassList.indexOf(className));
}




public DeviceView findView(String deviceName) 
{
	RobotDevice<?,?> device;
	
	device=this.robot.getDeviceOnName(deviceName);
	
	if (device!=null)
	{
//		return(device.getViewer(type));			
	}
	
	return(null);
}




public void moveView(String deviceName,int xPos,int yPos) 
{
	DeviceView viewer;
	
	viewer=findView(deviceName);

	if (viewer!=null)
	{
		viewer.setLocation(xPos,yPos);
	}
	
}





public void viewFrame(DisplayFrame viewer) 
{
	
	if (viewer==null)
		return;
	
	this.remove(viewer);
	this.add(viewer);
	
	
	
	if (viewer.isValid())
	{
		viewer.show();
	}
	else
	{
		this.add(viewer);
	}
	viewer.toFront();			
}


/*
private void viewDisplay(int index)
{
	String className;
	
	
	className = this.displayClassList.get(index);
	
	if (className==null)
		return;
	
	try {
		
		DisplayFrame displayView = (DisplayFrame) Class.forName(className).newInstance();
		
		displayView.setRobot(this.robot);
		
		this.add(displayView);
		
		
		
	} catch (ClassNotFoundException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	}
	//displayClass.newInstance();
	catch (InstantiationException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	} catch (IllegalAccessException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	}
	
}


*/

public void viewFrame(String deviceName) 
{
	DeviceView viewer;
	
	viewer=findView(deviceName);
	
	if (viewer!=null)
	{
		if (viewer.isValid())
		{
			viewer.show();
		}
		else
		{
			this.add(viewer);
		}
		viewer.toFront();			
	}

	
}








void showWindow(int index)
{
	
	JInternalFrame[] frames;

	JDesktopPane desktopPane;

	
	
	desktopPane = (JDesktopPane) this.getContentPane();

	frames=desktopPane.getAllFrames();

	frames[index].show();
	frames[index].toFront();
	

}




private void viewFrame(int index)
{
	String className;
	
	
	className = this.displayClassList.get(index);
	
	if (className==null)
		return;
	
	try {
		
		DisplayFrame deviceView = (DisplayFrame) Class.forName(className).newInstance();
		
		deviceView.setRobot(this.robot);
		
		this.add(deviceView);
		deviceView.toFront();
		
		
	} catch (ClassNotFoundException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	}
	//displayClass.newInstance();
	catch (InstantiationException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	} catch (IllegalAccessException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	}
	
}



void showWindowsMenu(JMenu menue)
{
	
	int iCounter;
	String frameName;
	JInternalFrame[] frames;

	JDesktopPane desktopPane;

	menue.removeAll();
	
	desktopPane = (JDesktopPane) this.getContentPane();

	frames=desktopPane.getAllFrames();
	
	
	for (iCounter=0;iCounter<frames.length;iCounter++)
	{
		frameName="Window_"+iCounter;
		
		
		menue.add(makeMenuItem(frames[iCounter].getTitle(),frameName));
		
	}

}

protected static final String openViewKey =".openView";
protected static final String openViewCountKey =".openViewCount";

void openSavedViews()
{
	int openViewsCount;
	int viewCounter;
	String viewClassName;
	
	openViewsCount= UiSettings.recoverInt(this.settingsKey+openViewCountKey, 0);
	
	for (viewCounter = 0; viewCounter< openViewsCount; viewCounter++)
	{
		viewClassName=UiSettings.recoverString(this.settingsKey+openViewKey+"."+viewCounter, "");
		try
		{
		DisplayFrame deviceView;
	
			deviceView = (DisplayFrame) Class.forName(viewClassName).newInstance();

		
		deviceView.setRobot(this.robot);
		
		this.add(deviceView);
		deviceView.toFront();
		
		
		} catch (Exception e)
		{
			// TODO Display error !!!!
			e.printStackTrace();
		} 
		
		
	}
}


/**
* save all open views so they can be reopened on restart
*/

void saveOpenWindows()
{	
	int iCounter;

	JInternalFrame[] frames;

	JDesktopPane desktopPane;

	// remove old keys
	
	
	desktopPane = (JDesktopPane) this.getContentPane();

	frames=desktopPane.getAllFrames();
	
	
	UiSettings.saveInt(this.settingsKey+openViewCountKey, frames.length);
	
	for (iCounter=0;iCounter<frames.length;iCounter++)
	{
		
		UiSettings.saveString(this.settingsKey+openViewKey+"."+iCounter, frames[iCounter].getClass().getName());
		
		//menue.add(makeMenuItem(frames[iCounter].getTitle(),frameName));
		
	}

}



@Override
public void actionPerformed(ActionEvent actionEvent)
{
	String cmd;
	
	cmd=actionEvent.getActionCommand();
	
	
	
if (cmd.startsWith(RobotViewer.CMD_SHOW_FRAME))
	{
		int index;
		
		cmd = cmd.substring(CMD_SHOW_FRAME.length());
		
		index=Integer.parseInt(cmd);
		this.viewFrame(index);
	}
	
	else if (cmd.equals(CMD_SHOW_WINDOWS))
	{

		System.out.println("windows");
	}
	else if (cmd.equals(CMD_START_INTERNAL_EMULATOR))
	{
			this.startEmulator(true);
	}
	else if (cmd.equals(CMD_START_EMULATOR))
	{
		this.startEmulator(false);
	}
	else if (cmd.equals(CMD_SAVE_SETTINGS))
	{
		this.saveSettings();
	}
	
	else if (cmd.equals(CMD_VIEW_SHARP_IR_CALCULATOR))
	{
		this.add(new SharpIrCalculator());
	}
	else if (cmd.equals(CMD_SHOW_BEHAVIOR))
	{
		RobotSettings settings = new RobotSettings();
		settings.setFileName("config/behaviordesktop.cfg");
		settings.loadSettings();
		new BehaviorViewer(this.robot.getBehavior(), settings);
	}
	


	else if (cmd.startsWith("Window_"))
	{
		this.showWindow(Integer.parseInt(cmd.substring(7)));
	}
}



@Override
public void menuCanceled(MenuEvent arg0) {
	// TODO Auto-generated method stub
	
}



@Override
public void menuDeselected(MenuEvent arg0) {
	// TODO Auto-generated method stub
	
}



@Override
public void menuSelected(MenuEvent menueEvent)
{
	showWindowsMenu((JMenu) menueEvent.getSource());
	
}


@Override
public void windowActivated(WindowEvent arg0)
{
	// TODO Auto-generated method stub
	
}


@Override
public void windowClosed(WindowEvent arg0)
{
	// TODO Auto-generated method stub
	
}


@Override
public void windowClosing(WindowEvent arg0)
{
	this.saveBounds();
	
	this.saveOpenWindows();
	
	this.saveSettings();
	
	this.robot = null;
	System.out.println("exiting application");
		System.exit(0);
}


@Override
public void windowDeactivated(WindowEvent arg0)
{
	// TODO Auto-generated method stub
	
}


@Override
public void windowDeiconified(WindowEvent arg0)
{
	// TODO Auto-generated method stub
	
}


@Override
public void windowIconified(WindowEvent arg0)
{
	// TODO Auto-generated method stub
	
}


@Override
public void windowOpened(WindowEvent arg0)
{
	// TODO Auto-generated method stub
	
}

protected void startEmulator(boolean internal) 
{
	
}


public void saveSettings()
{
	try
	{
		this.preferences.storeToXML(new FileOutputStream(configurationFile), RobotViewer.this.getName()+" configuration");
	} catch (IOException e)
	{
		e.printStackTrace();
	}
}




class saveSettingsTask extends TimerTask
{


public void run()
{
	RobotViewer.this.saveSettings();
}	

}


}
'''
