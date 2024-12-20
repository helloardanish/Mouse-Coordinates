import pyautogui
import tkinter as tk
from tkinter import TclError
import time
from threading import Thread


class LiveCoordinates:
    def __init__(self):
        self.label = None
        self.frame = None
        self.is_running = False
        self.logging_active = False
        self.root = None
        self.log_thread = None

        # Create the coordinate window immediately on the main thread
        self.setup_window()

    def setup_window(self):
        """Set up the coordinate display window"""
        self.root = tk.Tk()

        # Enhanced window attributes for better visibility
        self.root.attributes(
            '-topmost', True,  # Stay on top
            '-alpha', 0.8,  # Slight transparency
            '-fullscreen', False,
            '-type', 'normal'
        )

        # Additional platform-specific attributes for macOS
        try:
            self.root.attributes('-float', True)  # Makes window float above others on macOS
        except TclError as e:
            # Handle the exception (e.g., log the error or ignore it)
            print(f"Failed to set '-float' attribute: {e}")
        # except:
        #     pass  # Ignore if not on macOS

        self.root.overrideredirect(True)
        self.root.configure(bg='black')
        self.root.withdraw()  # Hide window initially

        # Create a frame with a border for better visibility
        self.frame = tk.Frame(
            self.root,
            bg='black',
            highlightbackground='white',
            highlightthickness=1
        )
        self.frame.pack(padx=1, pady=1)

        # Enhanced label with better visibility
        self.label = tk.Label(
            self.frame,
            text="",
            fg='lime',  # Bright color for better visibility
            bg='black',
            font=('Arial', 11, 'bold'),
            padx=5,
            pady=2
        )
        self.label.pack()

        # Lift window to top and force focus
        self.root.lift()
        self.root.focus_force()

    def start_tracking(self):
        """Start the coordinate tracking"""
        if not self.is_running:
            self.is_running = True
            self.logging_active = True

            # Show the window and ensure it's on top
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()

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
            self.root.withdraw()

    def update_position(self):
        """Update the coordinate display"""
        if self.is_running:
            try:
                x, y = pyautogui.position()
                self.label.configure(text=f'X: {x}, Y: {y}')

                # Keep window near cursor but not directly under it
                window_x = x + 20
                window_y = y - 40  # Moved slightly higher to avoid cursor overlap

                # Ensure window stays within screen bounds
                screen_width, screen_height = pyautogui.size()
                if window_x + 100 > screen_width:  # Assuming window width ~100px
                    window_x = x - 120  # Move to left of cursor
                if window_y < 0:
                    window_y = y + 20  # Move below cursor

                self.root.geometry(f'+{window_x}+{window_y}')

                # Ensure window stays on top
                self.root.lift()
                self.root.attributes('-topmost', True)

            except Exception as e:
                print(f"Error updating position: {e}")

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