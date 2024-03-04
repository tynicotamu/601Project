import tkinter as tk
from tkinter import ttk

class F1DriverStatsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("F1 Driver Statistics")

        # Example data structure
        self.drivers_data = {
            "Lewis Hamilton": {
                "last_win": "2020-12-13",
                "total_wins": 95,
                "best_finish": {"Silverstone": "1st", "Monza": "2nd"},
                "races_per_track": {"Silverstone": 14, "Monza": 15},
            },
            "Max Verstappen": {
                "last_win": "2020-12-12",
                "total_wins": 10,
                "best_finish": {"Silverstone": "2nd", "Monza": "3rd"},
                "races_per_track": {"Silverstone": 6, "Monza": 6},
            },
        }

        # Setup UI
        self.setup_ui()

    def setup_ui(self):
        # Dropdown for selecting driver
        driver_select_label = ttk.Label(self.root, text="Select Driver:")
        driver_select_label.pack()
        self.driver_select = ttk.Combobox(self.root, values=list(self.drivers_data.keys()))
        self.driver_select.pack()
        self.driver_select.bind('<<ComboboxSelected>>', self.update_display)

        # StringVars for dynamic labels
        self.last_win = tk.StringVar()
        self.total_wins = tk.StringVar()
        self.best_finish = tk.StringVar()
        self.races_per_track = tk.StringVar()

        # Labels for displaying statistics
        last_win_label = ttk.Label(self.root, textvariable=self.last_win)
        last_win_label.pack()

        total_wins_label = ttk.Label(self.root, textvariable=self.total_wins)
        total_wins_label.pack()

        best_finish_label = ttk.Label(self.root, textvariable=self.best_finish)
        best_finish_label.pack()

        races_per_track_label = ttk.Label(self.root, textvariable=self.races_per_track)
        races_per_track_label.pack()

    def update_display(self, event):
        driver = self.driver_select.get()
        data = self.drivers_data.get(driver, {})
        self.last_win.set(f"Last Win: {data.get('last_win', 'N/A')}")
        self.total_wins.set(f"Total Wins: {data.get('total_wins', 'N/A')}")

        best_finish_text = "Best Finish:\n" + "\n".join([f"{track}: {finish}" for track, finish in data.get("best_finish", {}).items()])
        self.best_finish.set(best_finish_text)

        races_per_track_text = "Races Per Track:\n" + "\n".join([f"{track}: {races}" for track, races in data.get("races_per_track", {}).items()])
        self.races_per_track.set(races_per_track_text)

def main():
    root = tk.Tk()
    app = F1DriverStatsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
