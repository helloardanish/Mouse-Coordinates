import PySimpleGUI as sg
from PySimpleGUI import WIN_CLOSED



# All the stuff inside your window.
layout = [
    [sg.Text("What's your name?")],
    [sg.InputText()],[sg.Button('Ok'),
    sg.Button('Cancel')]
    ]

# Define the layout
layout1 = [
    [sg.Text("Click one of the buttons below:")],
    [sg.InputText()],
    [sg.Button('Ok', key="ok")],
    [sg.Button("Button 1", key="BUTTON_1"),
     sg.Button("Button 2", key="BUTTON_2"),
     sg.Button("Button 3", key="BUTTON_3"),
     sg.Button("Capture PRO", key="capture")],
    [sg.Button('Cancel', key="cancel")]
]


# Create the Window
window = sg.Window('Coordinates Detector', layout1)

# Event Loop to process "events" and get the "values" of the inputs


def on_button_click(buttonName):
    print(buttonName)

while True:
    event, values = window.read()

    # if user closes window or clicks cancel
    if event == sg.WIN_CLOSED or event == 'Cancel':
        window.close()
    elif event==WIN_CLOSED:
        print("Closed the window")
    elif event == "ok":
        print('Hello', values[0], '!')
    elif event == "BUTTON_1":  # Handle Button 1 click
        on_button_click("Button 1")
    elif event == "BUTTON_2":  # Handle Button 2 click
        on_button_click("Button 2")
    elif event == "BUTTON_3":  # Handle Button 3 click
        on_button_click("Button 3")
    elif event == "capture":
        on_button_click("Capture started")


# Close the window
window.close()
