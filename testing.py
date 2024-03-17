import tkinter as tk
from PIL import ImageTk
import sqlite3
from numpy import random
import pyglet
from pygame import mixer



root = tk.Tk()
root.title("Recipe Picker")
root.eval("tk::PlaceWindow . left")

frame3 = tk.Frame(root)


# stack frame 2 above frame 1
frame3.tkraise()

leftframe = tk.Frame(frame3, bg="white", bd=5, relief=tk.SUNKEN)
leftframe.pack(side="left", fill="both", expand=True, padx=10, pady=10)

(tk.Label(leftframe, text="Please Make A Selection", bg="light blue", fg="black", font=("Shanti", 14)).
 pack(side='top', pady=20))

scrollbar = tk.Scrollbar(leftframe)
scrollbar.pack(side=tk.RIGHT, fill='y')

listbox = tk.Listbox(leftframe, yscrollcommand=scrollbar.set, height=10)
listbox.pack(side='top', fill='both', expand=True)
listbox.config(yscrollcommand=scrollbar.set)

toprightframe = tk.Frame(frame3, bg="white", bd=5, relief=tk.SUNKEN)
toprightframe.pack(side="top", fill=tk.X, padx=10, pady=10)  # Change the packing to `side="top"` and `fill=tk.X`
tk.Button(toprightframe, text="Search", font=("Ubuntu", 14), bg="#28393a", fg="white", cursor="hand2",
          activebackground="#badee2", activeforeground="black").pack(side='top', pady=10, padx=50)

botrightframe = tk.Frame(frame3, bg="white", bd=5, relief=tk.SUNKEN)
botrightframe.pack(side="top", fill=tk.X, padx=10, pady=10)

tk.Label(botrightframe, text="Altitude: ", bg="light blue", fg="black", font=("Shanti", 14)).grid(row=0, column=0)

tk.Label(botrightframe, text="Country: ", bg="light blue", fg="black", font=("Shanti", 14)).grid(row=1, column=0)

tk.Label(botrightframe, text="Longitude: ", bg="light blue", fg="black", font=("Shanti", 14)).grid(row=2, column=0)

tk.Label(botrightframe, text="Latitude: ", bg="light blue", fg="black", font=("Shanti", 14)).grid(row=3, column=0)

tk.Label(botrightframe, text="Wiki Link: ", bg="light blue", fg="black", font=("Shanti", 14)).grid(row=4, column=0)

tk.Label(botrightframe, text="Fastest Lap: ", bg="light blue", fg="black", font=("Shanti", 14)).grid(row=5, column=0)

# 'back' button widget
tk.Button(toprightframe, text="BACK", font=("Ubuntu", 14), bg="#28393a", fg="white", cursor="hand2",
          activebackground="#badee2",
          activeforeground="black", command=lambda: load_frame1()).pack(pady=20)


root.mainloop()