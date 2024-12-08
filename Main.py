import PySimpleGUI as sg
from LiveCoordinates import LiveCoordinates


def main():
    # Create the coordinate tracker instance
    tracker = LiveCoordinates()

    # Set the theme
    sg.theme('DarkBlue3')

    # Define the layout
    layout = [
        [sg.Text('Mouse Coordinate Tracker', font=('Helvetica', 16))],
        [sg.Text('Click Start to begin tracking mouse coordinates')],
        [sg.Button('Start', key='-START-', size=(10, 1)),
         sg.Button('Stop', key='-STOP-', size=(10, 1), disabled=True),
         sg.Button('Exit', key='-EXIT-', size=(10, 1))],
        [sg.Text('Coordinates will be logged to CoordinatesInfo.txt when mouse is static for 10 seconds',
                 size=(50, 2), text_color='gray')]
    ]

    # Create the window
    window = sg.Window('Coordinate Tracker', layout, finalize=True)

    # Event loop
    while True:
        event, values = window.read(timeout=100)

        if event == sg.WIN_CLOSED or event == '-EXIT-':
            tracker.cleanup()
            break

        elif event == '-START-':
            window['-START-'].update(disabled=True)
            window['-STOP-'].update(disabled=False)
            tracker.start_tracking()

        elif event == '-STOP-':
            window['-START-'].update(disabled=False)
            window['-STOP-'].update(disabled=True)
            tracker.stop_tracking()

    window.close()


if __name__ == "__main__":
    main()