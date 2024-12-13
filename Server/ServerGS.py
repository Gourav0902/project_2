'''Gouravjeet Singh (Fall 2024)
# Student id- 100920691

This program is strictly my own work. Any material
beyond course learning materials that is taken from
the Web or other sources is properly cited, giving.
credit to the original author(s)'''


import socket
import json, time
import PySimpleGUI as sg

sg. theme ('Light Brown 4')# Setting a theme for the GUI window

sock = socket.socket()
# Server address and port
adddress = ''
port = 5000
 
            

# Binding the socket to the address and port
sock.bind((adddress, port)) # to run on Pi with local client
sock.listen(5)

# Accepting a client connection
c, addr = sock.accept()

# Defining LED symbols for status
CIRCLE = '\u26AB'
CIRCLE_OUTLINE = '⚪'
# Initial LED state (off)
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
window = sg.Window("Server Monitoring", layout)# Creating the window for the server GUI
# Function to blink the LED (toggle between on/off states)
def led_blink(window, key):
    global led
    led = 1 - led
    window[key].update(LED_STATE[led])

# Main function that handles the server logic and GUI updates    
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
                ret7 = data["Throttling"]# Throttling information

                window['-ITERATION-'].update(f"{ret1}")
                window['-TEMP-'].update(f"{ret2}\u2103")
                window['-VOLT-'].update(f"{ret3} V")
                window['-ARM_MEMORY-'].update(f"{ret4}\u3386\n")
                window['-ARM_CLOCK-'].update(f"{ret5}\u3392\n")
                window['-GPU_MEMORY-'].update(f"{ret6}\u3386\n")
                window['-THROTTLING-'].update(f"{ret7}")
      # Blinking the LED to indicate new data         
                led_blink(window, '-LED0-')
                
                iteration_count += 1
 # After 50 iterations, show a popup and exit                
                if iteration_count == 50:
                    sg.popup("50 Iterations Complete!", "Thank you for using the server. Goodbye!")
                    break
        except (socket.error, json.JSONDecodeError):
            sg.popup("Check server connection")
            break
    window.close()
    c.close()


# Main entry point of the program
if __name__== '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sg.popup("Bye .... ")
        exit()
