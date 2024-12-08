import pyautogui
import tkinter as tk
import time
from threading import Thread


class LiveCoordinates:
    def __init__(self):
        # Create the main window
        self.root = tk.Tk()
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.attributes('-topmost', True)  # Keep window on top
        self.root.configure(bg='black')

        # Create label for coordinates
        self.label = tk.Label(
            self.root,
            text="",
            fg='white',
            bg='black',
            font=('Arial', 10),
            padx=5,
            pady=2
        )
        self.label.pack()

        # Start the logging thread
        self.logging_active = True
        self.log_thread = Thread(target=self.log_positions, daemon=True)
        self.log_thread.start()

        # Update coordinates
        self.update_position()

    def update_position(self):
        """Update the coordinate display"""
        x, y = pyautogui.position()
        self.label.configure(text=f'X: {x}, Y: {y}')

        # Move the window near the cursor
        self.root.geometry(f'+{x + 20}+{y - 30}')

        # Schedule the next update
        self.root.after(50, self.update_position)

    def log_positions(self):
        """Log positions that remain static for more than 5 seconds"""
        last_position = None
        last_time = None

        with open("CoordinatesInfo.txt", 'a') as log_file:
            while self.logging_active:
                current_position = pyautogui.position()

                if current_position != last_position:
                    last_position = current_position
                    last_time = time.time()
                else:
                    if last_time and time.time() - last_time > 5:
                        log_message = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Position: {current_position}\n"
                        log_file.write(log_message)
                        log_file.flush()
                        print(log_message.strip())
                        last_time = time.time()

                time.sleep(0.1)

    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        finally:
            self.logging_active = False
