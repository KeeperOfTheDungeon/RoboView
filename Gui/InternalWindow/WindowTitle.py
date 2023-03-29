from tkinter import Canvas, Frame, Button, Toplevel
import customtkinter as ctk


class WindowTitle():
    def __init__(self, root, master, name):
        self._canvas = Canvas(root)
        self._root = root
        self._master = master
        self._canvas.config(bg="darkblue")
        self._canvas.bind("<Button-1>", self.mouse_pressed)
        self._canvas.bind("<ButtonRelease-1>", self.mouse_released)
        self._name = name
        self._text = self._canvas.create_text(
            10, 15, text=self._name,  fill='WHITE', anchor='w', font=('Helvetica', '15', 'bold'))
        self._canvas.bind("<Double-Button-1>", self.extract_window)
        self._canvas.bind("<ButtonRelease-3>", self.minimize_window)
        
        

    def rename(self, new_name):
        self._name = new_name
        self._canvas.itemconfig(self._text, text=self._name)

    def mouse_pressed(self, event):
        self._root.lift()
        self._origin_x = event.x
        self._origin_y = event.y
        self._canvas.bind("<Motion>", self.mouse_motion)

    def mouse_released(self, event):
        self._canvas.unbind("<Motion>")

    def mouse_motion(self, event):
        self._master.move(self._origin_x - event.x, self._origin_y - event.y)
        
    def extract_window(self, event):
        self._master.extract_window()
    
    def minimize_window(self, event):
        self._master.minimize_window()


