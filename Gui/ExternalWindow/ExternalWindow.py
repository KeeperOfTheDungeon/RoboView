from tkinter import Toplevel, Frame, LEFT, BOTTOM
import customtkinter as ctk
from RoboView.Robot.Viewer.RobotSettings import RobotSettings

from RoboView.Robot.Device.Viewer.StatusBar import StatusBar
from RoboView.Robot.Device.Viewer.ToolBar import ToolBar

class ExternalWindow():
    
    def __init__(self, master, device):
        self._master = master
        
        self._window = Toplevel(bg="grey", borderwidth=1, relief='solid')
        self._window.geometry("{}x{}+{}+{}".format(self._master._width, self._master._height, self._master._x_pos, self._master._y_pos))
        self._window.title(self._master._settings_key)

        
        self._tool_bar = ToolBar(self._window, device)
        self._display = Frame(self._window, bg="grey", borderwidth=1)
        self._status_bar = StatusBar(self._window, device)
        
        self.resize_window()

        self._window.protocol("WM_DELETE_WINDOW", lambda: self.on_close())
        self._window.mainloop()
        
        
    def resize_window(self):
        self._window.update()
        
        x_size = self._master._width
        y_size = self._master._height
        
        self._status_bar._frame.place(
                height=50, width=x_size, x=0, y=y_size - 50)
        self._tool_bar._frame.place(height=37, width=x_size, x=0, y=0)
        self._display.place(height=y_size - 90,
                               width=x_size - 3, x=1, y=65)
        
        
    def on_close(self):
        self._window.destroy()
        self._master.close("event")


        

    
        #self.get_components()
        
    #def get_components(self):
        #print("Settingskey.x_pos:", RobotSettings.get_int(self._internal_window._settings_key+".x_pos"))