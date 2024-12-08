import pyautogui
import tkinter as tk
import time
from threading import Thread


class LiveCoordinates:
    def __init__(self):
        self.is_running = False
        self.logging_active = False
        self.root = None
        self.log_thread = None

        # Create the coordinate window immediately on the main thread
        self.setup_window()

    def setup_window(self):
        """Setup the coordinate display window"""
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='black')
        self.root.withdraw()  # Hide window initially

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

    def start_tracking(self):
        """Start the coordinate tracking"""
        if not self.is_running:
            self.is_running = True
            self.logging_active = True

            # Show the window
            self.root.deiconify()

            # Start the logging thread
            self.log_thread = Thread(target=self.log_positions, daemon=True)
            self.log_thread.start()

            # Start updating position
            self.update_position()

    def stop_tracking(self):
        """Stop the coordinate tracking"""
        if self.is_running:
            self.is_running = False
            self.logging_active = False
            self.root.withdraw()  # Hide the window

    def update_position(self):
        """Update the coordinate display"""
        if self.is_running:
            x, y = pyautogui.position()
            self.label.configure(text=f'X: {x}, Y: {y}')
            self.root.geometry(f'+{x + 20}+{y - 30}')

        if self.root:
            self.root.after(50, self.update_position)

    def log_positions(self):
        """Log positions that remain static for more than 10 seconds"""
        last_position = None
        last_time = None

        with open("CoordinatesInfo.txt", 'a') as log_file:
            while self.logging_active:
                current_position = pyautogui.position()

                if current_position != last_position:
                    last_position = current_position
                    last_time = time.time()
                else:
                    if last_time and time.time() - last_time > 10:
                        log_message = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Position: {current_position}\n"
                        log_file.write(log_message)
                        log_file.flush()
                        print(log_message.strip())
                        last_time = time.time()

                time.sleep(0.1)

    def run(self):
        """Start the main loop"""
        if self.root:
            self.root.mainloop()

    def cleanup(self):
        """Cleanup resources"""
        self.stop_tracking()
        if self.root:
            self.root.quit()
            self.root.destroy()