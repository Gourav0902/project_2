'''This is the server, should run first, in sperarte thonny instance,
gets client (pi) data'''

import socket
import json, time
import PySimpleGUI as sg

sock = socket.socket()
print("Socket created ... ")

port = 5000
#sock.bind(('', port))ret1 = data["Temperature"] # Temperature value
            


sock.bind(('10.102.13.191', port)) # to run on Pi with local client
sock.listen(5)


c, addr = sock.accept()
sg. theme ('Light Brown 4')
layout = [
    [sg.Text('Temperature:', size=(15, 1)), sg.Text('', size=(15, 1), key='-TEMP-')],
    [sg.Text('Voltage:', size=(15, 1)), sg.Text('', size=(15, 1), key='-VOLT-')],
    [sg.Text('Arm Memory:', size=(15, 1)), sg.Text('', size=(15, 1), key='-ARM_MEMORY-')],
    [sg.Text('Arm Clock:', size=(15, 1)), sg.Text('', size=(15, 1), key='-ARM_CLOCK-')],
    [sg.Text('GPU Memory:', size=(15, 1)), sg.Text('', size=(15, 1), key='-GPU_MEMORY-')],
    [sg.Button("Exit")],
]
window = sg.Window("Server Monitoring", layout)
def main():
    while True:
        event, values = window.read(timeout=100)  # Timeout of 100ms to allow non-blocking GUI interaction

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        try:
            jsonReceived = (c.recv(1024).decode())
            
            if jsonReceived == '':
                print("connection lost")
                exit()
            data = json.loads(jsonReceived) #creates the Json string
            ret1 = data["Temperature"] # Temperature value
            ret2 = data["Voltage"] # Voltage value
            ret3 = data["Arm_Memory"]# ARM memory usage
            ret4 = data["Arm_Clock"]# ARM clock speed
            ret5 = data["GPU_Memory"]# GPU memory usage

            window['-TEMP-'].update(f"{ret1}\u2103")
            window['-VOLT-'].update(f"{ret2} V")
            window['-ARM_MEMORY-'].update(f"{ret3} MB")
            window['-ARM_CLOCK-'].update(f"{ret4} MHz")
            window['-GPU_MEMORY-'].update(f"{ret5} MB")
        except (socket.error, json.JSONDecodeError):
            print("Check server connection")
            break
    window.close()
    c.close



if _name== 'main_':
    try:
        main()
    except KeyboardInterrupt:
        print("Bye .... ")
        exit()