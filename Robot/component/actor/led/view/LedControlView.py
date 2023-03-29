

from tkinter import HORIZONTAL, Scale
from RoboControl.Robot.Component.Actor.Led.Led import Led
from RoboView.Robot.component.view.AktorControlView import ActorControlView
from RoboView.Robot.component.view.MissingComponentView import MissingComponentView


class LedControlView(ActorControlView):

    def __init__(self, root, led, settings_key):
        super().__init__(root, led, settings_key, 110, 50)

        self._position_slider = Scale(
            self._data_frame, from_=0, to=100, orient=HORIZONTAL, command=self.change_brightness)
        self._position_slider.place(x=5, y=5,  width=100, height=40)
        self._position_slider.bind("<Button-1>", self.mouse_pressed_sensor)
        self._position_slider.bind("<ButtonRelease-1>", self.mouse_released_value_label)
        self._position_slider.bind("<Leave>", self.mouse_released_value_label)

    # self._state = BooleanVar()
    # self._on_button = Checkbutton(self._data_frame, text="on", variable=self._state, command=self.changeStatus)
    # self._on_button.place(x = 5, y = 20,  width=40, height=20)

    def create_view(root, led, settings_key):

        if led is not None:
            view = LedControlView(root, led, settings_key)
        else:
            view = MissingComponentView(Led.__name__)

        return view

    def change_brightness(self, brightness):
        value = float(brightness)/100
        self._actor.remote_set_brightness(value)

    def mouse_pressed_sensor(self, event):
        self.mouse_pressed(event)
        self._position_slider.bind("<Motion>", self.mouse_motion)

    def mouse_released_value_label(self, event):
        self._position_slider.unbind("<Motion>")


"""package de.hska.lat.robot.component.actor.led.view;

import java.awt.Insets;

import javax.swing.JSlider;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;


import de.hska.lat.robot.component.actor.led.Led;
import de.hska.lat.robot.component.view.ComponentView;
import de.hska.lat.robot.component.view.MissingComponentView;


/**
 * ComponentView child, that implements a Slider changing a Led's brightness.
 * @author mo
 *
 */
public class LedControlView extends ComponentView implements ChangeListener
{

	/**
	 * 
	 */
	private static final long serialVersionUID = -4238144556537574802L;

	
	protected static final int width = 160;
	protected static final int height = 70;
	
	
	protected Led led;
	
	
	protected JSlider brightness;
	
public LedControlView(Led led)
{
	super(led.getComponentName(), false);


	this.led = led;
	buildView();

}


@Override
protected void buildView()
{
	
	
	super.buildView();

	
	Insets insets = this.getBorder().getBorderInsets(this);
	
	
	this.brightness = new JSlider(0,255);
	this.brightness.setBounds(insets.left+5, insets.top+5, 100, 20);
	this.brightness.addChangeListener(this);
	this.add(this.brightness);
	
}



@Override
protected int getViewWidth()
{
	return(LedControlView.width);
}

@Override
protected int getViewHeight()
{
	return(LedControlView.height);
}


@Override
public void stateChanged(ChangeEvent changeEvent)
{
	Object source;
	
	source = changeEvent.getSource();
	
	if (source == this.brightness)
	{
		this.led.remote_setBrightness(((float)this.brightness.getValue())/255);
	}
	// TODO Auto-generated method stub
	
}


public static  ComponentView createView(Led led)
{
	if (led!=null)
	{
		return(new LedControlView(led));
	}
	else
	{
		return(new MissingComponentView(Led.class.getName()));
	}
}




}
"""
