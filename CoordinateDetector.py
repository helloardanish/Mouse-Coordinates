import pyautogui
import time


def log_mouse_position(file_path):
    """
    Monitors the mouse pointer location and logs it to a file if the position
    remains unchanged for more than 5 seconds.

    Args:
        file_path (str): Path to the file where mouse positions are logged.
    """
    last_position = None
    last_time = None

    with open(file_path, 'a') as log_file:
        while True:
            # Get current mouse position
            current_position = pyautogui.position()

            # Check if the position has changed
            if current_position != last_position:
                # Update last_position and reset timer
                last_position = current_position
                last_time = time.time()
            else:
                # Check how long the mouse has been at the same position
                if last_time and time.time() - last_time > 10:
                    # Log the position and time to the file
                    log_message = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Position: {current_position}\n"
                    log_file.write(log_message)
                    log_file.flush()  # Ensure the log is written immediately
                    print(log_message.strip())
