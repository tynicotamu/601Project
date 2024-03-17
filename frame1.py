import tkinter as tk
from PIL import ImageTk
import sqlite3
from numpy import random
import pyglet
from pygame import mixer


# set colours
bg_colour = "#FF1801"

# load custom fonts
pyglet.font.add_file("fonts/Ubuntu-Bold.ttf")
pyglet.font.add_file("fonts/Shanti-Regular.ttf")


def clear_widgets(frame):
    # select all frame widgets and delete them
    for widget in frame.winfo_children():
        widget.destroy()


def fetch_db():
    # connect an sqlite database
    connection = sqlite3.connect("data/recipes.db")
    cursor = connection.cursor()

    # fetch all the table names
    cursor.execute("SELECT * FROM sqlite_schema WHERE type='table';")
    all_tables = cursor.fetchall()

    # choose random table idx
    idx = random.randint(0, len(all_tables) - 1)

    # fetch records from table
    table_name = all_tables[idx][1]
    cursor.execute("SELECT * FROM " + table_name + ";")
    table_records = cursor.fetchall()

    connection.close()

    return table_name, table_records


def pre_process(table_name, table_records):
    # preprocess table name
    title = table_name[:-6]
    title = "".join([char if char.islower() else " " + char for char in title])

    # preprocess table records
    ingredients = []

    for i in table_records:
        name = i[1]
        qty = i[2]
        unit = i[3]
        ingredients.append(qty + " " + unit + " of " + name)

    return title, ingredients


def load_frame1():
    clear_widgets(frame2)

    # stack frame 1 above frame 2

    frame1.tkraise()

    # prevent widgets from modifying the frame
    frame1.pack_propagate(False)

    # create logo widget
    logo_img = ImageTk.PhotoImage(file="assets/F1_logo.png")
    logo_widget = tk.Label(frame1, image=logo_img, bg='white')
    logo_widget.image = logo_img
    logo_widget.pack(pady=75)

    # create label widget for instructions
    tk.Label(
        frame1,
        text="Please Select an Option",
        bg='white',
        fg="#FF1801",
        font=("Shanti", 18)
    ).pack()

    # create button widget
    tk.Button(
        frame1,
        text="Driver Info",
        font=("Ubuntu", 20),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        command=lambda: load_frame2()
    ).pack(side='left', pady=20, padx=25)

    tk.Button(
        frame1,
        text="Circuit Info",
        font=("Ubuntu", 20),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        command=lambda: load_frame3()
    ).pack(side='right', pady=20, padx=25)


    tk.Button(
        frame1,
        text="Mute", font=("Ubuntu", 12), bg="#28393a", fg="white", cursor="hand2", activebackground="#badee2",
        activeforeground="black",
        command=lambda: toggle_music()
    ).pack(side='bottom', pady=20)



def load_frame2():
    clear_widgets(frame1)
    # stack frame 2 above frame 1
    frame2.tkraise()

    leftframe = tk.Frame(frame2, bg="white", bd=5, relief=tk.SUNKEN)
    leftframe.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    (tk.Label(leftframe, text="Please Make A Selection", bg="light blue", fg="black", font=("Shanti", 14)).
     pack(side='top', pady=20))

    scrollbar = tk.Scrollbar(leftframe)
    scrollbar.pack(side=tk.RIGHT, fill='y')

    listbox = tk.Listbox(leftframe, yscrollcommand=scrollbar.set, height=10)
    listbox.pack(side='top', fill='both', expand=True)
    listbox.config(yscrollcommand=scrollbar.set)

    toprightframe = tk.Frame(frame2, bg="white", bd=5, relief=tk.SUNKEN)
    toprightframe.pack(side="top", fill=tk.X, padx=10, pady=10)  # Change the packing to `side="top"` and `fill=tk.X`
    tk.Button(toprightframe, text="Search", font=("Ubuntu", 14), bg="#28393a", fg="white", cursor="hand2",
              activebackground="#badee2", activeforeground="black").pack(side='top', pady=10, padx=50)

    botrightframe = tk.Frame(frame2, bg="white", bd=5, relief=tk.SUNKEN)
    botrightframe.pack(side="top", fill=tk.X, padx=10, pady=10)

    tk.Label(botrightframe, text="Nationality:", bg="light blue", fg="black", font=("Shanti", 14)).grid(row=0, column=0)

    tk.Label(botrightframe, text="Number:", bg="light blue", fg="black", font=("Shanti", 14)).grid(row=1, column=0)

    tk.Label(botrightframe, text="Race Wins", bg="light blue", fg="black", font=("Shanti", 14)).grid(row=2, column=0)

    tk.Label(botrightframe, text="# Polls", bg="light blue", fg="black", font=("Shanti", 14)).grid(row=3, column=0)

    tk.Label(botrightframe, text="Last Win", bg="light blue", fg="black", font=("Shanti", 14)).grid(row=4, column=0)

    tk.Label(botrightframe, text="Most Won Circuit", bg="light blue", fg="black", font=("Shanti", 14)).grid(row=5, column=0)

    tk.Label(botrightframe, text="Total Wins", bg="light blue", fg="black", font=("Shanti", 14)).grid(row=6, column=0)

    tk.Label(botrightframe, text="Total Podiums", bg="light blue", fg="black", font=("Shanti", 14)).grid(row=7, column=0)

    # 'back' button widget
    tk.Button(toprightframe, text="BACK", font=("Ubuntu", 14), bg="#28393a", fg="white", cursor="hand2", activebackground="#badee2",
        activeforeground="black", command=lambda: load_frame1()).pack(pady=20)


def load_frame3():
    clear_widgets(frame1)
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
    tk.Button(toprightframe, text="BACK", font=("Ubuntu", 14), bg="#28393a", fg="white", cursor="hand2", activebackground="#badee2",
        activeforeground="black", command=lambda: load_frame1()).pack(pady=20)





def toggle_music():
    if mixer.music.get_volume() > 0:
        mixer.music.set_volume(0)  # Mute the music
    else:
        mixer.music.set_volume(0.5)  # Unmute the music (restore volume)



# initiallize app with basic settings
root = tk.Tk()
root.title("F1 Metrics")
root.eval("tk::PlaceWindow . left")
mixer.init()

audio_file = 'assets//F1_song.mp3'  # Change this to the path of your audio file
mixer.music.load(audio_file)
mixer.music.set_volume(0.4)
mixer.music.play(-1, fade_ms=1000)




# place app in the center of the screen (alternative approach to root.eval())
# x = root.winfo_screenwidth() // 2
# y = int(root.winfo_screenheight() * 0.1)
# root.geometry('500x600+' + str(x) + '+' + str(y))

# create a frame widgets
frame1 = tk.Frame(root, width=500, height=600, bg='white')
frame2 = tk.Frame(root, bg=bg_colour)
frame3 = tk.Frame(root, bg=bg_colour)

# place frame widgets in window
for frame in (frame1, frame2,frame3):
    frame.grid(row=0, column=0, sticky="nesw")

# load the first frame
load_frame1()

# run app
root.mainloop()