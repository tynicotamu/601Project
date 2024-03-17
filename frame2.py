import tkinter as tk
from PIL import ImageTk
import sqlite3
from numpy import random
import pyglet


# set colours
bg_colour = "#FF1801"

# load custom fonts
pyglet.font.add_file("fonts/Ubuntu-Bold.ttf")
pyglet.font.add_file("fonts/Shanti-Regular.ttf")

# Create the main window
root = tk.Tk()
root.title("Two Frame Tkinter Box - Sunken Frames")
root.configure(bg=bg_colour)

# Configure the root window size if desired
root.geometry("600x400")  # Width x Height

# Create the first frame with a sunken relief
frame1 = tk.Frame(root, bg="white", bd=5, relief=tk.SUNKEN)
frame1.pack(side="left", fill="both", expand=True, padx=10, pady=10)


# Example of adding widgets to the first frame
(tk.Label(frame1, text="Please Make A Selection", bg="light blue", fg="black", font=("Shanti", 14)).
    pack(side='top', pady=20))


scrollbar = tk.Scrollbar(frame1)
scrollbar.pack(side=tk.RIGHT, fill='y')


listbox = tk.Listbox(frame1, yscrollcommand=scrollbar.set, height=10)
listbox.pack(side='top', fill='both', expand=True)
listbox.config(yscrollcommand=scrollbar.set)



frame2 = tk.Frame(root, bg="white", bd=5, relief=tk.SUNKEN)
frame2.pack(side="top", fill=tk.X, padx=10, pady=10)  # Change the packing to `side="top"` and `fill=tk.X`
tk.Button(frame2, text="Search", font=("Ubuntu", 14), bg="#28393a", fg="white", cursor="hand2",activebackground="#badee2",
      activeforeground="black").pack(side='top', pady=10, padx=50)


frame3 = tk.Frame(root, bg="white", bd=5, relief=tk.SUNKEN)
frame3.pack(side="top", fill=tk.X, padx=10, pady=10)
tk.Label(frame3, text="Nationality:", bg="light blue", fg="black", font=("Shanti", 14)).grid(row=0, column=0)

tk.Label(frame3, text="Number:", bg="light blue", fg="black", font=("Shanti", 14)).grid(row=1, column=0)

tk.Label(frame3, text="Race Wins", bg="light blue", fg="black", font=("Shanti", 14)).grid(row=2, column=0)

tk.Label(frame3, text="# Polls", bg="light blue", fg="black", font=("Shanti", 14)).grid(row=3, column=0)

tk.Label(frame3, text="Last Win", bg="light blue", fg="black", font=("Shanti", 14)).grid(row=4, column=0)

tk.Label(frame3, text="Most Won Circuit", bg="light blue", fg="black", font=("Shanti", 14)).grid(row=5, column=0)

tk.Label(frame3, text="Total Wins", bg="light blue", fg="black", font=("Shanti", 14)).grid(row=6, column=0)

tk.Label(frame3, text="Total Podiums", bg="light blue", fg="black", font=("Shanti", 14)).grid(row=7, column=0)





# Start the Tkinter event loop
root.mainloop()
