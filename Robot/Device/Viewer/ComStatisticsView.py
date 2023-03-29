
from tkinter import TOP, LEFT, Frame, Label, Menu, W
import customtkinter as ctk


class ComStatisticsView:
    def __init__(self, root, device):
        self._frame = ctk.CTkFrame(
            master=root, fg_color='white', height=50, corner_radius=3)
        self._root = root
        self._device = device
        self.build_view()

        device.add_com_status_listener(self)

    def build_view(self):
        label_font = ctk.CTkFont()

        label = ctk.CTkLabel(self._frame, text="COM",
                             height=12, font=("Arial", 12), text_color='black')
        label.pack(side=TOP)

        label = ctk.CTkLabel(self._frame, text="rx :",
                             font=label_font, text_color='black')
        label.pack(side=LEFT, padx=2)
        self._rx_count = ctk.CTkLabel(
            self._frame, text=" - ", font=label_font, text_color='black')
        self._rx_count.pack(side=LEFT, padx=(0, 10))

        label = ctk.CTkLabel(self._frame, text="tx :",
                             font=label_font, text_color='black')
        label.pack(side=LEFT, padx=2)
        self._tx_count = ctk.CTkLabel(
            self._frame, text=" - ", font=label_font, text_color='black')
        self._tx_count.pack(side=LEFT, padx=(0, 10))

        label = ctk.CTkLabel(self._frame, text="lost :",
                             font=label_font, text_color='black')
        label.pack(side=LEFT, padx=2)
        self._lost_count = ctk.CTkLabel(
            self._frame, text=" - ", font=label_font, text_color='black')
        self._lost_count.pack(side=LEFT, padx=(0, 10))

        label = ctk.CTkLabel(self._frame, text="inv :",
                             font=label_font, text_color='black')
        label.pack(side=LEFT, padx=2)
        self._invalid_count = ctk.CTkLabel(
            self._frame, text=" - ", font=label_font, text_color='black')
        self._invalid_count.pack(side=LEFT, padx=(0, 10))

        self._frame.bind("<ButtonRelease-3>", self.mouse_released)

        self._context_menue = Menu(self._frame, tearoff=0)
        self._context_menue.add_command(
            label="Clear com Statistic", command=self.on_clear_statistic)

    def mouse_released(self, event):

        try:
            self._context_menue.tk_popup(event.x_root, event.y_root)
        finally:
            self._context_menue.grab_release()

    def on_clear_statistic(self):
        self._device.remote_clear_com_statistics()
        pass

    def com_status_changed(self, statistic):
        rx_count = statistic.get_recived_messages()
        self._rx_count['text'] = str(rx_count)

        tx_count = statistic.get_transfered_messages()
        self._tx_count['text'] = str(tx_count)

        lost_count = statistic.get_lost_messages()
        self._lost_count['text'] = str(lost_count)

        invalid_count = statistic.get_invalid_messages()
        self._invalid_count['text'] = str(invalid_count)


"""
private void buildView()
{

	JLabel tmpLabel;	
	
	this.setLayout(new FlowLayout());
	
	tmpLabel=new JLabel("TX  :");
//	tmpLabel.setBounds(5, 5, 30, 20);
	this.add(tmpLabel);
	 
	this.txCount=new JLabel("-");
//	this.txCount.setBounds(35, 5, 80, 20);
	this.add(this.txCount);
	 
	 
	tmpLabel=new JLabel("RX  :");
//	tmpLabel.setBounds(125, 5, 40, 20);
	this.add(tmpLabel);

	this.rxCount=new JLabel("-");
//	this.rxCount.setBounds(155, 5, 60, 20);
	this.add(this.rxCount);
	 
 
	tmpLabel=new JLabel("INV :");
//	tmpLabel.setBounds(215, 5, 40, 20);
	this.add(tmpLabel);

	this.invalidCount=new JLabel("-");
//	this.invalidCount.setBounds(245, 5, 60, 20);
	this.add(this.invalidCount);
	 
	 
	tmpLabel=new JLabel("LOST:");
//	tmpLabel.setBounds(305, 5, 40, 20);
	this.add(tmpLabel);

	 
	this.lostCount=new JLabel("-");
//	this.lostCount.setBounds(345, 5, 60, 20);
	this.add(this.lostCount);
}"""


"""package de.hska.lat.robot.device.viewer.control.comStatistics;


import java.awt.FlowLayout;

import javax.swing.JLabel;
import javax.swing.JPanel;

import de.hska.lat.robot.component.statistic.ComStatusListener;

import de.hska.lat.robot.component.statistic.ComStatus;

public class ComStatisticsView extends JPanel implements ComStatusListener{

	
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	
	private JLabel rxCount;	
	private JLabel txCount;
	private JLabel invalidCount;
	private JLabel lostCount;
	
public ComStatisticsView()
{
	buildView();
}
	
	





@Override
public void comStatusChanged(ComStatus comStatus)
{
	
	this.rxCount.setText(String.valueOf(comStatus.getRecivedMessages()));
	this.txCount.setText(String.valueOf(comStatus.getTransferedMessages()));
	this.invalidCount.setText(String.valueOf(comStatus.getInvalidMessages()));
	this.lostCount.setText(String.valueOf(comStatus.getLostMessages()));
}
	
}
"""
