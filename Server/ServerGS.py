'''Gouravjeet Singh (Fall 2024)
# Student id- 100920691

This program is strictly my own work. Any material
beyond course learning materials that is taken from
the Web or other sources is properly cited, giving.
credit to the original author(s)'''


import socket
import json, time
import PySimpleGUI as sg
sg. theme ('Light Brown 4')
sock = socket.socket()
adddress = ''
port = 5000
 
            


sock.bind((adddress, port)) # to run on Pi with local client
sock.listen(5)


c, addr = sock.accept()
CIRCLE = '\u26AB'
CIRCLE_OUTLINE = '⚪'

LED_STATE = [CIRCLE_OUTLINE, CIRCLE]
led = 0

def LED(color, key) :
    return sg.Text(CIRCLE_OUTLINE, text_color=color, key=key)
layout = [
    [sg.Text('Data'),LED('Green', '-LED0-')],
    [sg.Text('Iteration:', size=(15, 1)), sg.Text('', size=(15, 1), key='-ITERATION-')],
    [sg.Text('Temperature:', size=(15, 1)), sg.Text('', size=(15, 1), key='-TEMP-')],
    [sg.Text('Voltage:', size=(15, 1)), sg.Text('', size=(15, 1), key='-VOLT-')],
    [sg.Text('Arm Memory:', size=(15, 1)), sg.Text('', size=(15, 1), key='-ARM_MEMORY-')],
    [sg.Text('Arm Clock:', size=(15, 1)), sg.Text('', size=(15, 1), key='-ARM_CLOCK-')],
    [sg.Text('GPU Memory:', size=(15, 1)), sg.Text('', size=(15, 1), key='-GPU_MEMORY-')],
    [sg.Text('Throttling:', size=(15, 1)), sg.Text('', size=(15, 1), key='-THROTTLING-')],
   
    [sg.Button("Exit")],
]
window = sg.Window("Server Monitoring", layout)

def led_blink(window, key):
    global led
    led = 1 - led
    window[key].update(LED_STATE[led])

    
def main():
    iteration_count = 0 
    while True:
        event, values = window.read(timeout=100)  # Timeout of 100ms to allow non-blocking GUI interaction

        if event == sg.WIN_CLOSED or event == 'Exit':
            print("Have a good day")
            break
        try:
            jsonReceived = c.recv(1024).decode('utf-8')
                
            if jsonReceived:
                             
                data = json.loads(jsonReceived) #creates the Json string
                
                ret1 = data["Iteration"]
                ret2 = data["Temperature"] # Temperature value
                ret3 = data["Voltage"] # Voltage value
                ret4 = data["Arm_Memory"]# ARM memory usage
                ret5 = data["Arm_Clock"]# ARM clock speed
                ret6 = data["GPU_Memory"]# GPU memory usage
                ret7 = data["Throttling"]

                window['-ITERATION-'].update(f"{ret1}")
                window['-TEMP-'].update(f"{ret2}\u2103")
                window['-VOLT-'].update(f"{ret3} V")
                window['-ARM_MEMORY-'].update(f"{ret4} MB")
                window['-ARM_CLOCK-'].update(f"{ret5} MHz")
                window['-GPU_MEMORY-'].update(f"{ret6} MB")
                window['-THROTTLING-'].update(f"{ret7}")
               
                led_blink(window, '-LED0-')
                
                iteration_count += 1
                
                if iteration_count == 50:
                    sg.popup("50 Iterations Complete!", "Thank you for using the server. Goodbye!")
                    break
        except (socket.error, json.JSONDecodeError):
            sg.popup("Check server connection")
            break
    window.close()
    c.close()



if __name__== '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sg.popup("Bye .... ")
        exit()
