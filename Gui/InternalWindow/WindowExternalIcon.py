from tkinter import Canvas, PhotoImage


class WindowExternalIcon():
    def __init__(self, root, master):
        self._root = root
        self._canvas = Canvas(root, height=26, width=26)
        self._master = master

        self._image = PhotoImage(file="Icons/external.png")


        self._canvas.create_image(0, 0, image=self._image, anchor='nw')
        self._canvas.bind("<ButtonRelease-1>", self.mouse_released)
        self._canvas.bind("<Enter>", self.mouse_hover)
        self._canvas.bind("<Leave>", self.mouse_leave)

    def mouse_released(self, event):
        self._master.extract_window()

    def mouse_hover(self, event):
        self._image = PhotoImage(file="Icons/external_hover.png")
       
        self._canvas.create_image(0, 0, image=self._image, anchor='nw')

    def mouse_leave(self, event):
        
        self._image = PhotoImage(file="Icons/external.png")
        self._canvas.create_image(0, 0, image=self._image, anchor='nw')
