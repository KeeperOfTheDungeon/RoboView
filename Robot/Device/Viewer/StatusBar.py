import customtkinter as ctk
from tkinter import LEFT, RIGHT, Frame

from RoboControl.Robot.Device.RobotDevice import RobotDevice
from RoboView.Robot.Device.Viewer.ComStatisticsView import ComStatisticsView
from RoboView.Robot.Device.Viewer.CpuStatisticsView import CpuStatisticsView


class StatusBar:
    _com_statistic_view: ComStatisticsView
    _cpu_statistic_view: CpuStatisticsView
    _device: RobotDevice

    def __init__(self, root, device):
        self._frame = Frame(master=root, bg='grey18', borderwidth=1)
        self._root = root
        self.set_device(device)

    def get_frame(self) -> ctk.CTkFrame:
        return self._frame

    def set_device(self, device: RobotDevice) -> None:
        self._device = device
        if hasattr(self, "_cpu_statistic_view"):
            self._cpu_statistic_view.get_frame().pack_forget()
        self._cpu_statistic_view = CpuStatisticsView(self._frame, device)
        self._cpu_statistic_view.get_frame().pack(side=LEFT, padx=5, pady=5, ipadx=5, ipady=5)
        if hasattr(self, "_com_statistic_view"):
            self._com_statistic_view.get_frame().pack_forget()
        self._com_statistic_view = ComStatisticsView(self._frame, device)
        self._com_statistic_view.get_frame().pack(side=RIGHT, padx=5, pady=5, ipadx=5, ipady=5)


"""package de.hska.lat.robot.device.viewer;

import java.awt.Color;

import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;


import javax.swing.JMenuItem;
import javax.swing.JPopupMenu;
import javax.swing.JToolBar;
import javax.swing.border.LineBorder;



import de.hska.lat.robot.device.RobotDevice;



import de.hska.lat.robot.device.viewer.control.comStatistics.ComStatisticsView;
import de.hska.lat.robot.device.viewer.control.comStatistics.CpuStatisticsView;

public class StatusBar extends JToolBar implements ActionListener {

    
    /**
     * 
     */
    private static final long serialVersionUID = 1L;

    protected static String STATUS_TEXT = " status :";
    
    ComStatisticsView comStatisticView;
    CpuStatisticsView cpuStatisticView;
    RobotDevice<?,?> device;
    
    
    protected JPopupMenu contextMenue;
    
    
    protected JMenuItem clearCpuStatisticMenueItem;
    protected JMenuItem clearComStatisticMenueItem;
    
    
    protected static final String CLEAR_CPU_STATISTICS_TEXT = "clear cpu statistics";
    protected static final String CLEAR_COM_STATISTICS_TEXT = "clear com statistics";
    
    protected static final String cmdClearCpuStats = "cmdClearCpuStats";
    protected static final String cmdClearComStats = "cmdClearComStats";
    
public StatusBar(RobotDevice<?,?> device)
{
    this.device = device;
    this.setName(device.getName()+STATUS_TEXT);
    this.setBorder(new LineBorder(Color.black));
    buildStatusBar(device);
    setLayout(new FlowLayout());
}



private void buildStatusBar(RobotDevice<?,?> device)
{


    
    
    this.comStatisticView = new ComStatisticsView();
    this.cpuStatisticView = new CpuStatisticsView();
    
    device.addComStatusListener(this.comStatisticView);
    device.addCpuStatusListener(this.cpuStatisticView);
    
    this.add(this.cpuStatisticView);
    this.addSeparator();
    this.add(this.comStatisticView);

    
    this.makePopupMenu();
        
}




protected JMenuItem addMenuItem(JPopupMenu popupMenu, String text, String command)
{
    
      JMenuItem  menuItem = new JMenuItem(text);
       menuItem.addActionListener(this);
       menuItem.setActionCommand(command);
       popupMenu.add(menuItem);

    
       return(menuItem); 
}

protected void makePopupMenu()
{
    this.contextMenue = new JPopupMenu();
    
      MouseListener popupListener = new PopupListener();
      
      this.clearCpuStatisticMenueItem = this.addMenuItem(this.contextMenue , StatusBar.CLEAR_CPU_STATISTICS_TEXT, StatusBar.cmdClearCpuStats);
      this.clearComStatisticMenueItem = this.addMenuItem(this.contextMenue , StatusBar.CLEAR_COM_STATISTICS_TEXT, StatusBar.cmdClearComStats);
      
      
    

    this.addMouseListener(popupListener);
}



class PopupListener extends MouseAdapter 
{
    public void mousePressed(MouseEvent e) 
    {
        maybeShowPopup(e);
    }

    public void mouseReleased(MouseEvent e) 
    {
        maybeShowPopup(e);
    }

    private void maybeShowPopup(MouseEvent e)
    {
        if (e.isPopupTrigger()) 
        {
            contextMenue.show(e.getComponent(),
                       e.getX(), e.getY());

        }
    }
}



@Override
public void actionPerformed(ActionEvent actionEvent)
{

    String cmd;
    
    cmd = actionEvent.getActionCommand();
    
    if (cmd.equals(cmdClearCpuStats))
    {
        device.remote_clearCpuStatistics();
    }
    else if (cmd.equals(cmdClearComStats))
    {
        device.remote_clearComStatistics();		
    }
    
}



}


"""
