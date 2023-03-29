

from tkinter import Canvas, PhotoImage


class WindowResizer():
    def __init__(self, root,master):
        self._root = root
        self._canvas = Canvas(root, borderwidth=0)
        self._master = master
        
        self._image = PhotoImage(file="Icons/resize.png")        
        self._canvas.create_image(0,0, image=self._image, anchor='nw')

        self._canvas.bind("<Button-1>", self.mouse_pressed)
        self._canvas.bind("<ButtonRelease-1>", self.mouse_released)
 

    def mouse_pressed(self, event):
        self._canvas.bind("<Motion>", self.mouse_moved)

    def mouse_released(self,event):
        self._canvas.unbind("<Motion>")


    def mouse_moved(self, event):
        self._canvas.unbind("<Motion>")
        x_size = self._master._frame.winfo_width() 
        y_size = self._master._frame.winfo_height()
        x_size = x_size + event.x
        y_size = y_size + event.y
        self._master.resize(x_size, y_size)
        self._canvas.bind("<Motion>", self.mouse_moved)  # still useful ??




