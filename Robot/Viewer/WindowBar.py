
from tkinter import Frame, Canvas, LEFT, BOTTOM
from RoboView.Gui.InternalWindow.WindowCloser import WindowCloser
from RoboView.Robot.Viewer.RobotSettings import RobotSettings


class WindowBar:
    def __init__(self, root):
        self._frame = Frame(
            master=root, background='WHITE')
        self._root = root
        self._internal_windows = []
        self._dict = {}
        self._frame.pack(side=BOTTOM, anchor='w')

    def add_window(self, internal_window):
        self._internal_windows.append(internal_window)
        self.render_windowbar()

    def render_windowbar(self):
        for widget in self._frame.winfo_children():
            widget.destroy()
        self._frame.config(width=1)
        self._dict = {}
        for intwin in self._internal_windows:
            internal_window = Canvas(self._frame)
            canvas = Canvas(internal_window, background='darkblue', height=27)
            text = canvas.create_text(
                10, 15, text=intwin._title._name, fill='WHITE', anchor='w', font=('Helvetica', '15', 'bold'))
            bbox = canvas.bbox(text)
            canvas.config(width=bbox[2] - bbox[0] + 40)
            canvas.bind("<Button-1>", self.open_window)
            canvas.pack(side=LEFT)
            self._dict[canvas] = intwin
            closer = WindowCloser(internal_window, self)
            closer._canvas.pack(side=LEFT)
            self._dict[closer._canvas] = intwin
            internal_window.pack(side=LEFT, padx=(0,4))

    # removes window from windowbar
    def remove_window_by_widget(self, event):
        internal_window = self._dict[event.widget]
        self._internal_windows.remove(internal_window)
        self.render_windowbar()
        return internal_window
    
    def remove_window_by_name(self, window_name):
        for window in self._internal_windows:
            if window._settings_key == window_name:
                print("Minimized Window {} removed".format(window))
                self._internal_windows.remove(window)
                self.render_windowbar()

    def open_window(self, event):
        internal_window = self.remove_window_by_widget(event)
        internal_window.show_window()

    def close(self, event):
        internal_window = self.remove_window_by_widget(event)
        internal_window.close(event)

    