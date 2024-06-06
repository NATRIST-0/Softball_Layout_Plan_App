#!/usr/bin/python3
# author: Tristan Gayrard

"""
Softball Layout Plan App
"""

import sys
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter.constants import BOTH, YES

root = tk.Tk()
root.title("Softball Layout Plan")
root.geometry('1152x648')

def on_close():
    root.destroy()
    exit()

def resize_image(event):
    new_width = event.width
    new_height = event.height
    image = copy_of_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)
    label.config(image = photo)
    label.image = photo
    
image = Image.open("Softball_App_Bkr.png")
copy_of_image = image.copy()
photo = ImageTk.PhotoImage(image)
label = ttk.Label(root, image = photo)


label.bind('<Configure>', resize_image)
label.pack(fill=BOTH, expand = YES)
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()