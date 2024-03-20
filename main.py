import tkinter as tk
from tkinter import messagebox
from pygame import mixer
from PIL import Image, ImageTk
import sqlite3
import pyglet


class Application(tk.Tk):

    def __init__(self):
        super().__init__()
        self.sorted_circuits = None
        self.title("F1 Metrics")
        self.eval("tk::PlaceWindow . center")

        self.frame1 = tk.Frame(self, width=500, height=600, bg='white')
        self.frame2 = tk.Frame(self, bg="#FF1801")
        self.frame3 = tk.Frame(self, bg="#FF1801")

        for frame in (self.frame1, self.frame2, self.frame3):
            frame.grid(row=0, column=0, sticky="nesw")

        mixer.init()
        audio_file = 'assets/F1_song.mp3'  # Ensure this path is correct
        mixer.music.load(audio_file)
        mixer.music.set_volume(0.4)
        mixer.music.play(-1, fade_ms=1000)
        self.load_frame1()

    def clear_widgets(self, frame):
        # select all frame widgets and delete them
        for widget in frame.winfo_children():
            widget.destroy()

    def toggle_music(self):
        if mixer.music.get_volume() > 0:
            mixer.music.set_volume(0)  # Mute the music
        else:
            mixer.music.set_volume(0.5)  # Unmute the music (restore volume)

    def load_frame1(self):
        # Assuming clear_widgets is a method to remove widgets from a frame
        self.clear_widgets(self.frame2)
        self.clear_widgets(self.frame3)

        self.frame1.tkraise()
        self.frame1.pack_propagate(False)

        # Ensure the path to your image file is correct
        logo_img = ImageTk.PhotoImage(Image.open("assets/F1_logo.png"))
        logo_widget = tk.Label(self.frame1, image=logo_img, bg='white')
        logo_widget.image = logo_img
        logo_widget.pack(pady=75)

        tk.Label(self.frame1, text="Please Select an Option", bg='white', fg="#FF1801", font=("Shanti", 18)).pack()

        tk.Button(self.frame1, text="Driver Info", font=("Ubuntu", 20), bg="#28393a", fg="white",
                  cursor="hand2", activebackground="#badee2", activeforeground="black",
                  command=self.load_frame2).pack(side='left', pady=20, padx=25)

        tk.Button(self.frame1, text="Circuit Info", font=("Ubuntu", 20), bg="#28393a", fg="white", cursor="hand2",
                  activebackground="#badee2", activeforeground="black", command=self.load_frame3).pack(side='right',
                                                                                                       pady=20, padx=25)

        # Assuming toggle_music is a method to mute/unmute the music
        tk.Button(self.frame1, text="Mute", font=("Ubuntu", 12), bg="#28393a", fg="white", cursor="hand2",
                  activebackground="#badee2", activeforeground="black", command=self.toggle_music).pack(side='bottom',
                                                                                                        pady=20)

    # Implement these methods according to your requirements
    def load_frame2(self):
        self.clear_widgets(self.frame1)
        # stack frame 2 above frame 1
        self.frame2.tkraise()

        leftframe = tk.Frame(self.frame2, bg="white", bd=5, relief=tk.SUNKEN)
        leftframe.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        (tk.Label(leftframe, text="Please Make A Selection", bg="light blue", fg="black", font=("Shanti", 14)).
         pack(side='top', pady=20))

        self.scrollbar = tk.Scrollbar(leftframe)
        self.scrollbar.pack(side=tk.RIGHT, fill='y')

        self.listbox = tk.Listbox(leftframe, yscrollcommand=self.scrollbar.set, height=10)
        self.listbox.pack(side='top', fill='both', expand=True)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        toprightframe = tk.Frame(self.frame2, bg="white", bd=5, relief=tk.SUNKEN)
        toprightframe.pack(side="top", fill=tk.X, padx=10,
                           pady=10)  # Change the packing to `side="top"` and `fill=tk.X`
        tk.Button(toprightframe, text="Search", font=("Ubuntu", 14), bg="#28393a", fg="white", cursor="hand2",
                  activebackground="#badee2", activeforeground="black").pack(side='top', pady=10, padx=50)

        botrightframe = tk.Frame(self.frame2, bg="white", bd=5, relief=tk.SUNKEN)
        botrightframe.pack(side="top", fill=tk.X, padx=10, pady=10)

        tk.Label(botrightframe, text="Nationality:", bg="light blue", fg="black", font=("Shanti", 14)).grid(row=0,
                                                                                                            column=0)

        tk.Label(botrightframe, text="Number:", bg="light blue", fg="black", font=("Shanti", 14)).grid(row=1, column=0)

        tk.Label(botrightframe, text="# Pole Positions", bg="light blue", fg="black", font=("Shanti", 14)).grid(row=3,
                                                                                                                column=0)

        tk.Label(botrightframe, text="Last Win", bg="light blue", fg="black", font=("Shanti", 14)).grid(row=4, column=0)

        tk.Label(botrightframe, text="Most Won Circuit", bg="light blue", fg="black", font=("Shanti", 14)).grid(row=5,
                                                                                                                column=0)

        tk.Label(botrightframe, text="Total Wins", bg="light blue", fg="black", font=("Shanti", 14)).grid(row=6,
                                                                                                          column=0)

        tk.Label(botrightframe, text="Total Podiums", bg="light blue", fg="black", font=("Shanti", 14)).grid(row=7,
                                                                                                             column=0)

        # 'back' button widget
        tk.Button(toprightframe, text="BACK", font=("Ubuntu", 14), bg="#28393a", fg="white", cursor="hand2",
                  activebackground="#badee2",
                  activeforeground="black", command=lambda: self.load_frame1()).pack(pady=20)

    def load_frame3(self):
        self.clear_widgets(self.frame1)
        # stack frame 2 above frame 1
        self.frame3.tkraise()

        def fetchcircuitlist_db():
            # Use context manager to ensure the connection is closed properly
            with sqlite3.connect("data/f1stats.db") as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT name FROM circuits")
                names = [row[0] for row in cursor.fetchall()]
            # Connection and cursor will be closed automatically here
            print(names)
            return names

        # Fetch the list of circuit names from the database
        circuit_names = fetchcircuitlist_db()
        self.sorted_circuits = sorted(circuit_names)

        def populate_listbox_from_tuple(listbox, data_tuple):
            # Clear the listbox
            listbox.delete(0, tk.END)
            # Insert items into the listbox
            for item in data_tuple:
                listbox.insert(tk.END, item)

        def on_select(event):
            # Note that calling `curselection` returns a tuple of selected indices
            selected_indices = event.widget.curselection()
            if selected_indices:  # Proceed only if something is selected
                # Get the first selected index
                index = selected_indices[0]
                # Retrieve the text of the selected item
                value = event.widget.get(index)
                print(f"You selected item {index}: {value}")

                conn = sqlite3.connect("data/f1stats.db")
                cursor = conn.cursor()

                # Execute a query to retrieve the first three rows
                cursor.execute("SELECT alt FROM circuits WHERE name = ?", (value,))

                # Fetch all the results
                altitude = cursor.fetchone()
                try:
                    altitude = float(altitude[0])
                    print(altitude)
                    altitude_input = {f"Altitude : {altitude} meters"}
                    altitude_input.__str__()
                    print(altitude_input)
                    self.circuit_label_altitude.config(text=altitude_input)
                except sqlite3.Error as e:
                    self.circuit_label_altitude.config(text="Altitude not available")

                # Close the connection
                conn.close()

                self.circuit_label_altitude.config(text='')

                self.circuit_label_country.config(text='')

                self.circuit_label_longitude.config(text='')

                self.circuit_label_latitude.config(text='')

                self.circuit_label_wiki.config(text='')

                self.circuit_label_fastestlap.config(text='')

        # Create the left frame
        leftframe = tk.Frame(self.frame3, bg="white", bd=5, relief=tk.SUNKEN)
        leftframe.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Create and pack the label in the left frame
        label = tk.Label(leftframe, text="Please Make A Selection", bg="light blue", fg="black", font=("Shanti", 14))
        label.pack(side="top", pady=20)
        # Create the scrollbar in the left frame
        scrollbar = tk.Scrollbar(leftframe)
        scrollbar.pack(side=tk.RIGHT, fill='y')

        # Create the listbox and associate it with the scrollbar
        listbox = tk.Listbox(leftframe, yscrollcommand=scrollbar.set, height=10)
        listbox.pack(side="top", fill="both", expand=True)
        listbox.config(yscrollcommand=scrollbar.set)
        listbox.bind('<<ListboxSelect>>', on_select)
        # Ensure the scrollbar controls the listbox view
        scrollbar.config(command=listbox.yview)

        # Fetch data from database and populate the listbox
        names_tuple = self.sorted_circuits
        populate_listbox_from_tuple(listbox, names_tuple)

        toprightframe = tk.Frame(self.frame3, bg="white", bd=5, relief=tk.SUNKEN)
        toprightframe.pack(side="top", fill=tk.X, padx=10,
                           pady=10)  # Change the packing to `side="top"` and `fill=tk.X`
        tk.Button(toprightframe, text="Search", font=("Ubuntu", 14), bg="#28393a", fg="white", cursor="hand2",
                  activebackground="#badee2", activeforeground="black").pack(side='top', pady=10, padx=50)

        botrightframe = tk.Frame(self.frame3, bg="white", bd=5, relief=tk.SUNKEN)
        botrightframe.pack(side="top", fill=tk.X, padx=10, pady=10)

        self.circuit_label_altitude = tk.Label(botrightframe, text="Altitude: ", bg="light blue", fg="black",
                                               font=("Shanti", 14))
        self.circuit_label_altitude.grid(row=0, column=0)

        self.circuit_label_country = tk.Label(botrightframe, text="Country: ", bg="light blue", fg="black",
                                              font=("Shanti", 14))
        self.circuit_label_country.grid(row=1, column=0)

        self.circuit_label_longitude = tk.Label(botrightframe, text="Longitude: ", bg="light blue", fg="black",
                                                font=("Shanti", 14))
        self.circuit_label_longitude.grid(row=2, column=0)

        self.circuit_label_latitude = tk.Label(botrightframe, text="Latitude: ", bg="light blue", fg="black",
                                               font=("Shanti", 14))
        self.circuit_label_latitude.grid(row=3, column=0)

        self.circuit_label_wiki = tk.Label(botrightframe, text="Wiki Link: ", bg="light blue", fg="black",
                                           font=("Shanti", 14))
        self.circuit_label_wiki.grid(row=4, column=0)

        self.circuit_label_fastestlap = tk.Label(botrightframe, text="Fastest Lap: ", bg="light blue", fg="black",
                                                 font=("Shanti", 14))
        self.circuit_label_fastestlap.grid(row=5, column=0)

        # 'back' button widget
        tk.Button(toprightframe, text="BACK", font=("Ubuntu", 14), bg="#28393a", fg="white", cursor="hand2",
                  activebackground="#badee2",
                  activeforeground="black", command=lambda: self.load_frame1()).pack(pady=20)

    # def clear_widgets(self, frame):
    #     for widget in frame.winfo_children():
    #         widget.destroy()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
