import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# Constants
DATA_FILE = 'bookings.json'
ROWS = 5
COLS = 5
SHOWTIMES = ["10:00 AM", "1:00 PM", "4:00 PM", "7:00 PM", "10:00 PM"]

# Initialize data
def load_data():
    if not os.path.exists(DATA_FILE):
        # Initialize data structure
        data = {showtime: [['O' for _ in range(COLS)] for _ in range(ROWS)] for showtime in SHOWTIMES}
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f)
    else:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    return data

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

class MovieBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Advanced Movie Booking System")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        self.data = load_data()
        self.current_showtime = SHOWTIMES[0]
        self.user = None  # Placeholder for user authentication

        self.create_widgets()

    def create_widgets(self):
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')  # Modern look
        style.configure("TButton", padding=6)
        style.configure("TLabel", padding=6, font=("Helvetica", 12))
        style.configure("Header.TLabel", font=("Helvetica", 16, "bold"))

        # Header
        header_label = ttk.Label(self.root, text="🎥 Advanced Movie Booking System", style="Header.TLabel")
        header_label.pack(pady=10)

        # Showtime Selection
        showtime_frame = ttk.Frame(self.root)
        showtime_frame.pack(pady=10)

        showtime_label = ttk.Label(showtime_frame, text="Select Showtime:")
        showtime_label.pack(side=tk.LEFT, padx=5)

        self.showtime_var = tk.StringVar()
        self.showtime_var.set(self.current_showtime)
        showtime_menu = ttk.OptionMenu(showtime_frame, self.showtime_var, self.current_showtime, *SHOWTIMES, command=self.change_showtime)
        showtime_menu.pack(side=tk.LEFT, padx=5)

        # Statistics
        stats_frame = ttk.Frame(self.root)
        stats_frame.pack(pady=10)

        self.total_booked_var = tk.StringVar()
        self.total_revenue_var = tk.StringVar()
        self.update_statistics()

        total_booked_label = ttk.Label(stats_frame, textvariable=self.total_booked_var)
        total_booked_label.pack(side=tk.LEFT, padx=20)

        total_revenue_label = ttk.Label(stats_frame, textvariable=self.total_revenue_var)
        total_revenue_label.pack(side=tk.LEFT, padx=20)

        # Seat Frame
        self.seat_frame = ttk.Frame(self.root)
        self.seat_frame.pack(pady=20)

        self.create_seat_layout()

        # Action Buttons
        action_frame = ttk.Frame(self.root)
        action_frame.pack(pady=10)

        book_btn = ttk.Button(action_frame, text="Book Selected Seats", command=self.book_selected_seats)
        book_btn.pack(side=tk.LEFT, padx=10)

        cancel_btn = ttk.Button(action_frame, text="Cancel Selected Seats", command=self.cancel_selected_seats)
        cancel_btn.pack(side=tk.LEFT, padx=10)

        reset_btn = ttk.Button(action_frame, text="Reset All Bookings", command=self.reset_seats)
        reset_btn.pack(side=tk.LEFT, padx=10)

    def create_seat_layout(self):
        # Clear previous seats
        for widget in self.seat_frame.winfo_children():
            widget.destroy()

        # Column Headers
        for col in range(1, COLS + 1):
            lbl = ttk.Label(self.seat_frame, text=f" {col} ", font=("Helvetica", 12, "bold"))
            lbl.grid(row=0, column=col, padx=10, pady=10)

        # Rows with Seat Buttons
        self.seat_buttons = {}
        self.selected_seats = set()
        for row in range(ROWS):
            row_label = ttk.Label(self.seat_frame, text=chr(65 + row), font=("Helvetica", 12, "bold"))
            row_label.grid(row=row + 1, column=0, padx=10, pady=10)
            for col in range(COLS):
                seat_status = self.data[self.current_showtime][row][col]
                if seat_status == 'O':
                    bg_color = 'green'
                else:
                    bg_color = 'red'
                btn = tk.Button(self.seat_frame, text='O' if seat_status == 'O' else 'X',
                                width=4, height=2, bg=bg_color,
                                command=lambda r=row, c=col: self.toggle_select_seat(r, c))
                btn.grid(row=row + 1, column=col + 1, padx=5, pady=5)
                self.seat_buttons[(row, col)] = btn

    def toggle_select_seat(self, row, col):
        seat = (row, col)
        btn = self.seat_buttons[seat]
        if seat in self.selected_seats:
            # Deselect seat
            self.selected_seats.remove(seat)
            if self.data[self.current_showtime][row][col] == 'O':
                btn.config(bg='green', text='O')
            else:
                btn.config(bg='red', text='X')
        else:
            # Select seat
            self.selected_seats.add(seat)
            btn.config(bg='yellow', text='S')

    def book_selected_seats(self):
        if not self.selected_seats:
            messagebox.showwarning("No Selection", "Please select at least one seat to book.")
            return
        for seat in self.selected_seats:
            row, col = seat
            if self.data[self.current_showtime][row][col] == 'X':
                messagebox.showwarning("Seat Unavailable", f"Seat {chr(65+row)}{col+1} is already booked.")
                continue
            self.data[self.current_showtime][row][col] = 'X'
            btn = self.seat_buttons[seat]
            btn.config(text='X', bg='red')
        save_data(self.data)
        self.selected_seats.clear()
        self.update_statistics()
        messagebox.showinfo("Booking Successful", "Selected seats have been booked successfully!")

    def cancel_selected_seats(self):
        if not self.selected_seats:
            messagebox.showwarning("No Selection", "Please select at least one seat to cancel.")
            return
        for seat in self.selected_seats:
            row, col = seat
            if self.data[self.current_showtime][row][col] == 'O':
                messagebox.showwarning("Seat Available", f"Seat {chr(65+row)}{col+1} is already available.")
                continue
            self.data[self.current_showtime][row][col] = 'O'
            btn = self.seat_buttons[seat]
            btn.config(text='O', bg='green')
        save_data(self.data)
        self.selected_seats.clear()
        self.update_statistics()
        messagebox.showinfo("Cancellation Successful", "Selected seats have been canceled successfully!")

    def reset_seats(self):
        confirm = messagebox.askyesno("Confirm Reset", "Are you sure you want to reset all bookings?")
        if not confirm:
            return
        for showtime in SHOWTIMES:
            for row in range(ROWS):
                for col in range(COLS):
                    self.data[showtime][row][col] = 'O'
        save_data(self.data)
        self.create_seat_layout()
        self.update_statistics()
        messagebox.showinfo("Reset Successful", "All bookings have been reset.")

    def change_showtime(self, value):
        self.current_showtime = value
        self.create_seat_layout()
        self.update_statistics()

    def update_statistics(self):
        total_booked = 0
        total_revenue = 0
        seat_price = 10  # Base price per seat
        for showtime in SHOWTIMES:
            for row in range(ROWS):
                for col in range(COLS):
                    if self.data[showtime][row][col] == 'X':
                        total_booked += 1
                        # Example pricing: Front rows are cheaper
                        price = seat_price - (row * 2)  # Row A: $10, B: $8, etc.
                        total_revenue += price
        self.total_booked_var.set(f"Total Booked Seats: {total_booked}")
        self.total_revenue_var.set(f"Total Revenue: ${total_revenue}")

def main():
    root = tk.Tk()
    app = MovieBookingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
