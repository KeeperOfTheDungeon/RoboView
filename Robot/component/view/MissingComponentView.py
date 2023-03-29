from RoboView.Robot.component.view.ComponentView import ComponentView


class MissingComponentView(ComponentView):
	def __init__(self, name):
		pass
#ToDo fehlermeldung anzeigen
"""
package de.hska.lat.robot.component.view;










public class MissingComponentView  extends  ComponentView 
{
	




/**
	 * 
	 */
	private static final long serialVersionUID = 1820267339241231444L;

	
	protected static final int width = 300;
	protected static final int height = 10;


	
public MissingComponentView(String type)
{
		super("missing :"+ type, false);

		this.setSize(100, 100);
		
		buildView( );
}

@Override
protected int getViewWidth()
{
	return(MissingComponentView.width);
}

@Override
protected int getViewHeight()
{
	return(MissingComponentView.height);
}


}
"""