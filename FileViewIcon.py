import tkinter as tk
from tkinter import ttk
from Event import Event
from PIL import ImageTK, Image
import os

class FileViewIcon(object):
    def __init__(self, master):
        return 0


class Icon(object):
    def __init__(self, name, path, img):
        self.name = name
        self.path = path
        if os.path.isdir(path):
            self.img = ImageTk.PhotoImage(Image.open('../Lib/img/directory.png'))
        else:
            self.img = ImageTK.PhotoImage(Image.open('../Lib/img/file.png'))
        frame = tk.Frame(master)