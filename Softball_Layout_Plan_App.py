#!/usr/bin/python3
# author: Tristan Gayrard

"""
Softball Layout Plan App
"""

import sys
import json
import openpyxl
import pandas as pd
from sys import exit
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from PIL import Image, ImageTk
from tkinter.constants import BOTH, YES

# Détermine le répertoire du script actuel
if getattr(sys, 'frozen', False):  # Exécution empaquetée avec Auto PY to EXE
    current_dir = Path(sys._MEIPASS)
else:  # Exécution normale du script Python
    current_dir = Path(__file__).parent

icon_file = 'icon.ico'
image_file = 'Softball_App_Bkr.png'

# Charger les données
data = pd.read_excel('PlayerSheet.xlsx')

# Extraire les informations des joueurs
boys = data['Boys'].dropna().tolist()
girls = data['Girls'].dropna().tolist()

root = tk.Tk()
root.title("Softball Layout Plan")
root.geometry('1152x648')
root.iconbitmap(icon_file)

def save_positions():
    positions = {label.cget("text"): {"x": label.winfo_x(), "y": label.winfo_y()} for label in labels}
    with open("player_positions.json", "w") as file:
        json.dump(positions, file)
    print("Positions saved.")
    
def load_positions():
    try:
        with open("player_positions.json", "r") as file:
            positions = json.load(file)
        for label in labels:
            player_name = label.cget("text")
            if player_name in positions:
                label.place(x=positions[player_name]["x"], y=positions[player_name]["y"])
        print("Positions loaded.")
    except FileNotFoundError:
        print("No saved positions found.")

def on_drag_start(event):
    event.widget.start_x = event.x
    event.widget.start_y = event.y

def on_drag_motion(event):
    dx = event.x - event.widget.start_x
    dy = event.y - event.widget.start_y

    event.widget.place(x=event.widget.winfo_x() + dx, y=event.widget.winfo_y() + dy)

def on_close():
    root.destroy()
    exit()

def resize_image(event):
    new_width = event.width
    new_height = event.height
    image = copy_of_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)
    background_label.config(image=photo)
    background_label.image = photo

def reset():
    for label, (x, y) in initial_positions:
        label.place(x=x, y=y)
         
def change_bkr():
    global image_file, copy_of_image, photo, background_label

    # Changer l'image de fond en fonction de l'image actuelle
    if image_file == 'Softball_App_Bkr.png':
        image_file = 'Softball_App_Bkr_Positions.png'
    else:
        image_file = 'Softball_App_Bkr.png'

    # Charger la nouvelle image
    image = Image.open(image_file)
    copy_of_image = image.copy()

    # Obtenir la taille actuelle de la fenêtre
    window_width = root.winfo_width()
    window_height = root.winfo_height()

    # Redimensionner l'image à la taille de la fenêtre
    resized_image = copy_of_image.resize((window_width, window_height))
    photo = ImageTk.PhotoImage(resized_image)

    # Mettre à jour l'image de fond existante
    background_label.config(image=photo)
    background_label.image = photo

    # Ajuster l'image quand la fenêtre est redimensionnée
    background_label.bind('<Configure>', resize_image)

# Charger et configurer l'image de fond
image = Image.open(image_file)
copy_of_image = image.copy()
photo = ImageTk.PhotoImage(image)
background_label = ttk.Label(root, image=photo)
background_label.pack(fill=BOTH, expand=YES)

labels = []
initial_positions = []

for i, player_name in enumerate(boys):
    player_label = tk.Label(root, text=f"{player_name}", bg="white",
                            highlightbackground="blue", highlightthickness=2)
    initial_x = 10
    initial_y = 10 + i * 30
    player_label.place(x=initial_x, y=initial_y)
    player_label.bind("<Button-1>", on_drag_start)
    player_label.bind("<B1-Motion>", on_drag_motion)
    labels.append(player_label)
    initial_positions.append((player_label, (initial_x, initial_y)))

for i, player_name in enumerate(girls):
    player_label = tk.Label(root, text=f"{player_name}", bg="white",
                            highlightbackground="pink", highlightthickness=2)
    initial_x = 200
    initial_y = 10 + i * 30
    player_label.place(x=initial_x, y=initial_y)
    player_label.bind("<Button-1>", on_drag_start)
    player_label.bind("<B1-Motion>", on_drag_motion)
    labels.append(player_label)
    initial_positions.append((player_label, (initial_x, initial_y)))

reset_button = ttk.Button(root, text="Reset", command=reset)
reset_button.place(relx=0.1, rely=0.95, anchor='s')

load_button = ttk.Button(root, text="Load Positions", command=load_positions)
load_button.place(relx=0.1, rely=0.85, anchor='s')

save_button = ttk.Button(root, text="Save Positions", command=save_positions)
save_button.place(relx=0.1, rely=0.75, anchor='s')

bkr_button = ttk.Button(root, text="Change Background", command=change_bkr)
bkr_button.place(relx=0.1, rely=0.65, anchor='s')

background_label.bind('<Configure>', resize_image)
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
