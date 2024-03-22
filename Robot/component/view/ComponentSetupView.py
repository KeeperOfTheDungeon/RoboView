from RoboView.Robot.component.view.ComponentView import ComponentView


class ComponentSetupView(ComponentView):
    def __init__(self, root, component, settings_key, width, height):
        super().__init__(root, component.get_name(), settings_key, width, height)
        self._component = component

    # self._name = component.get_name()

    def build_context_menu(self):
        super().build_context_menu()
        self._context_menue.add_command(label="get settings", command=self.on_get_settings)
        self._context_menue.add_command(label="set settings", command=self.on_set_settings)
        self._context_menue.add_command(label="load defaults", command=self.on_load_defaults)
        self._context_menue.add_command(label="save defaults", command=self.on_save_defaults)
        self._context_menue.add_separator()

    def on_get_settings(self):
        self._component.remote_get_settings()

    def on_set_settings(self):
        self._component.remote_set_settings()

    def on_load_defaults(self):
        self._component.remote_load_defaults()

    def on_save_defaults(self):
        self._component.remote_save_defaults()


"""		package de.hska.lat.robot.component.view;

import java.awt.Color;
import java.awt.event.ActionEvent;

import javax.swing.JButton;
import javax.swing.border.LineBorder;

import de.hska.lat.robot.component.RobotComponent;

public abstract class ComponentSettingsView<C extends RobotComponent<?,?,?>> extends ComponentView  
{

	
	/**
	 * 
	 */
	private static final long serialVersionUID = 6962081753819708662L;
	protected C component;
	
	
	protected static String cmd_set="cmdSet";
	protected static String cmd_get="cmdGet";
	protected static String cmd_save="cmdSave";
	protected static String cmd_load="cmdLoad";
	
	protected static String STRING_GET = "get";
	protected static String STRING_SET = "set";
	protected static String STRING_LOAD = "load";
	protected static String STRING_SAVE = "save";
	
	
public ComponentSettingsView(C component)
{
	super(component.getComponentName(), false);
	
	this.component = component;
	

	// TODO Auto-generated constructor stub
}

protected void addSetButton(int x, int y, int width, int height)
{
	JButton tmpButton;
	
	tmpButton = new JButton(STRING_SET);
	tmpButton.setBounds(x, y, width, height);
	tmpButton.setActionCommand(cmd_set);
	tmpButton.addActionListener(this);
	tmpButton.setBorder(new LineBorder(Color.GRAY));
	this.add(tmpButton);
	
}



protected void addGetButton(int x, int y, int width, int height)
{
	JButton tmpButton;
	
	tmpButton = new JButton(STRING_GET);
	tmpButton.setBounds(x, y, width, height);
	tmpButton.setActionCommand(cmd_get);
	tmpButton.addActionListener(this);
	tmpButton.setBorder(new LineBorder(Color.GRAY));
	this.add(tmpButton);

}



protected void addSaveButton(int x, int y, int width, int height)
{
	JButton tmpButton;
	
	tmpButton = new JButton(STRING_SAVE);
	tmpButton.setBounds(x, y, width, height);
	tmpButton.setActionCommand(cmd_save);
	tmpButton.addActionListener(this);
	tmpButton.setBorder(new LineBorder(Color.GRAY));
	this.add(tmpButton);
}	


protected void addLoadButton(int x, int y, int width, int height)
{
	JButton tmpButton;
	
	tmpButton = new JButton(STRING_LOAD);
	tmpButton.setBounds(x, y, width, height);
	tmpButton.setActionCommand(cmd_load);
	tmpButton.addActionListener(this);
	tmpButton.setBorder(new LineBorder(Color.GRAY));
	this.add(tmpButton);
}


/**
 * load components defaults. Send to remote commands loadDefaults, followed by getSettings.
 *  First command load device defaults from devices non volatile memory.
 *  Second command  
 * @return
 */
protected boolean loadDefaults()
{
	boolean resoult = this.component.remote_loadDefaults() || 
	this.component.remote_getSettings();
	
	return(resoult);
}


/**
 * save actual Defaults in remote device non volatile memory
 * @return true if this command could be send, else if not
 */
protected boolean saveDefaults()
{
	return(this.component.remote_saveDefaults());
}


/**
 * 
 * @return true if this command could be send, else if not
 */

protected boolean getSettings()
{
	return(this.component.remote_getSettings());
}




protected abstract boolean setSettings();




@Override
public void actionPerformed(ActionEvent actionEvent) 
{
	

	String cmd;
	
	cmd=actionEvent.getActionCommand();
	
	if (cmd.equals(ComponentSettingsView.cmd_get))
	{
		this.getSettings();
	}
	else if (cmd.equals(ComponentSettingsView.cmd_save))
	{
		this.saveDefaults();
	}
	else if (cmd.equals(ComponentSettingsView.cmd_load))
	{
		this.loadDefaults();
		this.getSettings();
	}	
	else if (cmd.equals(ComponentSettingsView.cmd_set))
	{
		this.setSettings();
	}	
	else
	{
		super.actionPerformed(actionEvent);
	}
}


/*
 * 	



	

 */

}
"""
