import tkinter as tk
from tkinter import messagebox
from pygame import mixer
from PIL import Image, ImageTk
import sqlite3
import pyglet
import webbrowser


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

    def load_frame2(self):
        self.clear_widgets(self.frame1)
        # stack frame 2 above frame 1
        self.frame2.tkraise()

        leftframe = tk.Frame(self.frame2, bg="white", bd=5, relief=tk.SUNKEN)
        leftframe.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        (tk.Label(leftframe, text="Please Make A Selection", bg="white", fg="black", font=("Shanti", 14)).
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
        botrightframe.pack(side="top", fill='both', expand=1, padx=10, pady=10)

        self.NatLabel = tk.Label(botrightframe, text="Nationality:", bg="white",
                                fg="black", font=("Shanti", 14))
        self.NatLabel.grid(row=0, column=0, sticky='w')

        self.NumLabel = tk.Label(botrightframe, text="Number:", bg="white",
                                fg="black", font=("Shanti", 14))
        self.NumLabel.grid(row=1, column=0, sticky='w')

        self.PolesLabel = tk.Label(botrightframe, text="# Pole Positions:", bg="white",
                                fg="black", font=("Shanti", 14))
        self.PolesLabel.grid(row=3, column=0, sticky='w')

        self.LastWinLabel = tk.Label(botrightframe, text="Last Win:", bg="white",
                                fg="black", font=("Shanti", 14))
        self.LastWinLabel.grid(row=4, column=0, sticky='w')

        self.MostWonLabel = tk.Label(botrightframe, text="Most Won Circuit:", bg="white",
                                fg="black", font=("Shanti", 14))
        self.MostWonLabel.grid(row=5, column=0, sticky='w')

        self.TotalWinsLabel = tk.Label(botrightframe, text="Total Wins:", bg="white",
                                fg="black", font=("Shanti", 14))
        self.TotalWinsLabel.grid(row=6, column=0, sticky='w')

        self.PodLabel = tk.Label(botrightframe, text="Total Podiums:", bg="white",
                                fg="black", justify='left', font=("Shanti", 14))
        self.PodLabel.grid(row=7, column=0, sticky='w')

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

            def open_hyperlink(url):
                webbrowser.open_new(url)

            if selected_indices:  # Proceed only if something is selected
                # Get the first selected index
                index = selected_indices[0]
                # Retrieve the text of the selected item
                value = event.widget.get(index)
                print(f"You selected item {index}: {value}")

                conn = sqlite3.connect("data/f1stats.db")
                cursor = conn.cursor()
                error_string = "Altitude not available"

                # Check if the query fetched a result
                try:
                    # Convert the altitude to float and format the output string
                    cursor.execute("SELECT alt FROM circuits WHERE name = ?", (value,))
                    altitude_data = cursor.fetchone()
                    # Load data
                    altitude = float(altitude_data[0])
                    altitude_input = f"Altitude: {altitude} meters"
                    self.circuit_label_altitude.config(text=altitude_input)
                except sqlite3.Error as e:
                    # If no altitude is found, set a default message
                    self.circuit_label_altitude.config(text=error_string)

                try:
                    # Convert the altitude to float and format the output string
                    cursor.execute("SELECT country FROM circuits WHERE name = ?", (value,))
                    country_data = cursor.fetchone()
                    # Load data
                    country_data_input = str(country_data[0])
                    country_data_input = f"Country: {country_data_input}"
                    self.circuit_label_country.config(text=country_data_input)

                except sqlite3.Error as e:
                    # If no altitude is found, set a default message
                    self.circuit_label_country.config(text=error_string)

                try:
                    # Convert the altitude to float and format the output string
                    cursor.execute("SELECT lng FROM circuits WHERE name = ?", (value,))
                    longitude_data = cursor.fetchone()
                    # Load data
                    longitude = float(longitude_data[0])
                    print('Test')
                    print(longitude)
                    longitude = f"Longitude: {longitude} degrees"
                    self.circuit_label_longitude.config(text=longitude)

                except sqlite3.Error as e:
                    # If no altitude is found, set a default message
                    self.circuit_label_country.config(text=error_string)

                try:
                    # Convert the altitude to float and format the output string
                    cursor.execute("SELECT lat FROM circuits WHERE name = ?", (value,))
                    latitude = cursor.fetchone()
                    # Load data
                    latitude = float(latitude[0])
                    latitude = f"Latitude: {latitude} degrees"
                    self.circuit_label_latitude.config(text=latitude)

                except sqlite3.Error as e:
                    # If no altitude is found, set a default message
                    self.circuit_label_country.config(text=error_string)

                try:
                    # Execute the query to fetch the URL
                    cursor.execute("SELECT url FROM circuits WHERE name = ?", (value,))
                    url_data = cursor.fetchone()

                    # Check if the query fetched a result
                    if url_data and url_data[0]:
                        # Extract the URL from the tuple
                        url = url_data[0]
                        print(f'URL fetched: {url}')

                        # Set the label with the URL
                        label_text = f"Link to URL"
                        self.circuit_label_wiki.config(text=label_text, fg="blue", cursor="hand2")

                        # Bind the label to open the hyperlink when clicked
                        self.circuit_label_wiki.bind("<Button-1>", lambda e, link=url: open_hyperlink(link))

                    else:
                        self.circuit_label_wiki.config(text="URL not available")

                    try:
                        # Query to get the fastest lap time for a given circuit name from the new table or view
                        cursor.execute("""
                            SELECT fastest_lap_time
                            FROM fastest_lap_per_circuit
                            WHERE circuit_name = ?
                        """, (value,))

                        # Fetch the result
                        result = cursor.fetchone()
                        print("Fast Test")
                        print(result)
                        # If a result is found, extract the lap time and update the label
                        if result and result[0] is not None:
                            fastest_lap_time = result[0]
                            print(f"Fastest Lap Time: {fastest_lap_time}")
                            fastest_lap_time = round(fastest_lap_time / 1000, 2)
                            self.circuit_label_fastestlap.config(text=f"Fastest Lap Time: {fastest_lap_time} seconds")
                        else:
                            self.circuit_label_fastestlap.config(text="No fastest lap time available")
                    except sqlite3.Error as e:
                        error_string = f"Database error: {e}"
                        print(error_string)
                        self.circuit_label_fastestlap.config(text=error_string)

                    except sqlite3.Error as e:
                        # If no altitude is found, set a default message
                        self.circuit_label_country.config(text=error_string)

                finally:
                    # Close the connection
                    conn.close()

        # Create the left frame
        leftframe = tk.Frame(self.frame3, bg="white", bd=5, relief=tk.SUNKEN)
        leftframe.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Create and pack the label in the left frame
        label = tk.Label(leftframe, text="Please Make A Selection", bg="white", fg="black", font=("Shanti", 14))
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

        self.circuit_label_altitude = tk.Label(botrightframe, text="Altitude: ", bg="white", fg="black",
                                               font=("Shanti", 14))
        self.circuit_label_altitude.grid(row=0, column=0)

        self.circuit_label_country = tk.Label(botrightframe, text="Country: ", bg="white", fg="black",
                                              font=("Shanti", 14))
        self.circuit_label_country.grid(row=1, column=0)

        self.circuit_label_longitude = tk.Label(botrightframe, text="Longitude: ", bg="white", fg="black",
                                                font=("Shanti", 14))
        self.circuit_label_longitude.grid(row=2, column=0)

        self.circuit_label_latitude = tk.Label(botrightframe, text="Latitude: ", bg="white", fg="black",
                                               font=("Shanti", 14))
        self.circuit_label_latitude.grid(row=3, column=0)

        self.circuit_label_wiki = tk.Label(botrightframe, text="Wiki Link: ", bg="white", fg="black",
                                           font=("Shanti", 14))
        self.circuit_label_wiki.grid(row=4, column=0)

        self.circuit_label_fastestlap = tk.Label(botrightframe, text="Fastest Lap: ", bg="white", fg="black",
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
