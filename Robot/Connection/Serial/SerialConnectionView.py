from tkinter import Label
from tkinter.ttk import Combobox

from RoboControl.Robot.AbstractRobot.AbstractRobot import AbstractRobot
from RoboView.Gui.InternalWindow.InternalWindow import InternalWindow
from RoboView.Robot.Ui.Settings.UiSettings import UiSettings
from RoboView.Robot.Viewer.WindowBar import WindowBar


class SerialConnectionView(InternalWindow):
	def __init__(self, root: str, window_bar: WindowBar):
		# UiSettings.get_int_value("test")
		super().__init__(root, window_bar)
		self.rename("Serial Connection")
		self.buildView()

	# FIXME camelCase
	def buildView(self) -> None:
		w = Label(self._frame, text="port")
		w.place(x=20, y=50, width=60, height=20)
		# w.pack()

		comboExample = Combobox(self._frame,
								values=[
									"January",
									"February",
									"March",
									"April"])

		comboExample.place(x=20, y=70, width=100, height=20)

	def connect(self) -> None:
		pass

	def disconnect(self) -> None:
		pass

	def set_robot(self, robot: AbstractRobot) -> bool:
		pass

	# FIXME this should be renamed to on_* for consistency
	def connected(self) -> None:
		pass

	# FIXME this should be renamed to on_* for consistency
	def disconnected(self) -> None:
		pass


"""
private void buildView()
{

	this.setLayout(null);
	JLabel tmpLabel;
	
	tmpLabel=new JLabel("port");
	tmpLabel.setBounds(10,20,50,20);
	this.add(tmpLabel);


	this.portSelector = new SerialInterfaceSelector();
	this.portSelector.setBounds(50,20,120,20);
	this.portSelector.setActionCommand(SerialConnectionView.CMD_PORT_SELECTED);
	this.portSelector.addActionListener(this);
	this.add(this.portSelector);

	
	
	
	
	
	this.connector= new JButton (SerialConnectionView.CONNECT_TEXT);
	this.connector.setBounds(50,50,100,20);
	this.connector.addActionListener(this);
	this.connector.setActionCommand(SerialConnectionView.CMD_CONNECT);
	this.add(this.connector);

	
	this.autoConnect = new JCheckBox(SerialConnectionView.AUTO_CONNECT_TEXT);
	this.autoConnect.setBounds(50,80,120,20);
	this.autoConnect.addActionListener(this);
	this.autoConnect.setActionCommand(SerialConnectionView.CMD_AUTO_CONNECT);
	this.add(this.autoConnect);
	
}

"""

"""package de.hska.lat.robot.connection.serial.view;



import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JLabel;
import javax.swing.JOptionPane;

import de.hska.lat.robot.abstractRobot.AbstractRobot;
import de.hska.lat.robot.abstractRobot.RobotConnectionListener;
import de.hska.lat.robot.connection.serial.SerialConnection;
import de.hska.lat.robot.displayFrame.DisplayFrame;
import de.hska.lat.robot.ui.settings.UiSettings;


public class SerialConnectionView extends DisplayFrame implements RobotConnectionListener, ActionListener
{
	
	
	
	/**
	* 
	*/
	private static final long serialVersionUID = -7180743603886059090L;


	protected static final String FRAME_NAME	= "serial connection";
	
	
	protected static final String CONNECT_TEXT 		= "connect";
	protected static final String DISCONNECT_TEXT	= "disconnect";
	protected static final String AUTO_CONNECT_TEXT	= "auto connect";

	protected static final String CMD_AUTO_CONNECT		= "cmdAutoConnect";
	protected static final String CMD_PORT_SELECTED 	= "cmdportSelected";
	protected static final String CMD_CONNECT 			= "cmdConnect";
	protected static final String CMD_DISCONNECT		= "cmdDisconnect";
	
	
	protected AbstractRobot<?,?,?> robot;
	

	
	protected SerialInterfaceSelector portSelector;
	protected JButton connector;
	protected JCheckBox autoConnect;
	
	protected static final String portKey =".port";
	protected static final String autoConnectKey =".autoConnect";
	
	protected SerialConnection connection;
	
public SerialConnectionView() 
{
	super(SerialConnectionView.FRAME_NAME, false, true, false, false);
	

	this.setBounds(100,100,190,140);
	

	this.buildView();


	this.show();
	
}




public void loadSettings()
{

	String portName;
	boolean autoConnect;
	
	portName = this.portSelector.getSelectedPortName();
	
	portName=UiSettings.recoverString(this.settingsKey+SerialConnectionView.portKey,portName);
	
	this.portSelector.setSelectedPort(portName);
	
	
	autoConnect = UiSettings.recoverBoolean(this.settingsKey+SerialConnectionView.autoConnectKey, false);
	this.autoConnect.setSelected(autoConnect);
}



public void saveActualPort()
{

	String portName;
	
	portName = this.portSelector.getSelectedPortName();
	
	UiSettings.saveString(this.settingsKey+SerialConnectionView.portKey,portName);
	
}

public void saveAutoConnect()
{
	UiSettings.saveBoolean(this.settingsKey+SerialConnectionView.autoConnectKey,this.autoConnect.isSelected());
}




public void connect()
{
	this.connection = new SerialConnection(portSelector.getSelectedPortName());
	
	this.connection.setDataPacketLogger(this.robot.getDataPacketLogger());
	if (connection.connect(this.robot)==true)
	{
		this.robot.connect(connection);
	}
	else
	{
		JOptionPane.showMessageDialog(null,
				"unable to connect to port "+connection.getPortName(),
				"error",
				JOptionPane.ERROR_MESSAGE);

	}

}



public void disconnect()
{
	this.connection.disconnect();
	robot.disconnect();
}

@Override
public boolean setRobot(AbstractRobot<?,?,?> robot)
{
	this.robot = robot;
	this.robot.addConnectionListener(this);
	this.loadSettings();
	
	if (this.autoConnect.isSelected())
	{
		this.connect();
	}

	return(true);
}




@Override
public void connected(AbstractRobot<?, ?, ?> robot)
{
	this.connector.setText(SerialConnectionView.DISCONNECT_TEXT);
	this.connector.setActionCommand(SerialConnectionView.CMD_DISCONNECT);
}




@Override
public void disconnected(AbstractRobot<?, ?, ?> robot)
{
	this.connector.setText(SerialConnectionView.CONNECT_TEXT);
	this.connector.setActionCommand(SerialConnectionView.CMD_CONNECT);
}





@Override
public void actionPerformed(ActionEvent actionEvent)
{
	String cmd;
	cmd = actionEvent.getActionCommand();
	
	if (cmd.equals(SerialConnectionView.CMD_CONNECT))
	{
		this.connect();
	}
	else if (cmd.equals(SerialConnectionView.CMD_DISCONNECT))
	{
		this.disconnect();
	}
	else if (cmd.equals(SerialConnectionView.CMD_PORT_SELECTED))
	{
		this.saveActualPort();
	}
	else if (cmd.equals(SerialConnectionView.CMD_AUTO_CONNECT))
	{
		this.saveAutoConnect();
	}
	
	
	// TODO Auto-generated method stub
	
}




}
"""
