'''Gouravjeet Singh (Fall 2024)
# Student id- 100920691

This program is strictly my own work. Any material
beyond course learning materials that is taken from
the Web or other sources is properly cited, giving.
credit to the original author(s)'''
import socket
import sys
import json, time
import os, io
import threading
import PySimpleGUI as sg
# Function to check if the device is a Raspberry Pi
def Hardware_check():
    try:
        with open("/proc/cpuinfo", "r") as cpuinfo:
            for line in cpuinfo:
                if "Raspberry Pi" in line:
                    return True
    except FileNotFoundError:
        pass
    return False
# Check if the device is a Raspberry Pi, if not exit the program
if not Hardware_check():
    sg.popup("Check Device")
    exit(0)

# Create a socket object for client-server communication
sock = socket. socket()
   
# Set the port number and server address
port = 5000

address = "10.102.13.149"

# Functions to get various Pi parameters using vcgencmd
def get_temp():
    t = os.popen('vcgencmd measure_temp').readline()
    return round(float(t.replace("temp=", "").replace("'C", "")), 1)

def get_volt():
    v = os.popen('vcgencmd measure_volts core').readline()
    return round(float(v.replace("volt=", "").replace("V", "")), 1)

def get_Arm_memory():
    m = os.popen('vcgencmd get_mem arm').readline()
    return round(float(m.replace("arm=", "").replace("M", "")), 1)

def get_Clock_frequency():
    c = os.popen('vcgencmd measure_clock arm').readline()
    return round(int(c.split('=')[1]) / 1_000_000, 1)

def get_gpu_memory():
    Gm = os.popen('vcgencmd get_mem gpu').readline()
    return round(float(Gm.replace("gpu=", "").replace("M", "")), 1)
def get_throttling():
    throttling = os.popen('vcgencmd get_throttled').readline()
    if throttling == '0x0':
        return "NO Throttling"
    else:
        return "Throttling Detected"
    
# Set GUI theme    
sg.theme('Light Brown 4')
# Define LED symbols (used for status indication)
CIRCLE = '\u26AB'
CIRCLE_OUTLINE = '⚪'

# Function to return a PySimpleGUI Text element representing an LED with a specific color
def LED(color, key) :
    return sg.Text(CIRCLE_OUTLINE, text_color=color, key=key)

# Define the layout for the GUI window
layout = [
    [sg.Text('Status '),LED('Green', '-LED0-'), sg.Text('Disconnected', key="-STATUS-")],  
    [sg.Button("Exit")],
    
]

# Create the window with the specified layout
window = sg.Window("Client Monitoring", layout, finalize = True)
# Function to handle data sending to the server
def send_data():
      
        
        try:
            sock.connect((address, port)) # Connect to the server at the specified address and port
            window['-STATUS-'].update("Connected")
            window['-LED0-'].update(CIRCLE)
            for i in range(50):
                # Create a dictionary with system data
                jsonResult = {
                                    "Iteration": i+1,
                                    "Temperature": get_temp(),
                                    "Voltage": get_volt(),
                                    "Arm_Memory": get_Arm_memory(),
                                    "Arm_Clock": get_Clock_frequency(),
                                    "GPU_Memory": get_gpu_memory(),
                                    "Throttling": get_throttling()
                                }

                    

                jsonResult = json.dumps(jsonResult)# Convert the dictionary to a JSON string
                jsonbyte = bytearray(jsonResult,"UTF-8")# Convert the JSON string to a bytearray for transmission
                try:  
                    sock.send(jsonbyte)
                    
                    

                except (socket.error, ConnectionRefusedError): # = short form for getaddrinfo()
                    window['-STATUS-'].update("Disconnected")  # Update status to "Disconnected"
                    window['-LED0-'].update(CIRCLE_OUTLINE)  # Change LED to disconnected color
                    print("Connection lost")
                    break
                time.sleep(2)
                # Read window events (such as button presses or window close)
                event, values = window.read(timeout=100)
                
            
                if event == sg.WIN_CLOSED or event == 'Exit':
                    sg.popup("Have a Good day")
                    break
                elif event == '-STATUS-':               
                    window['-STATUS-'].update(values['-STATUS-'])
                elif event == '-LED0-':
               
                    window['-LED0-'].update(values['-LED0-'])
                     
        except KeyboardInterrupt:
            sg.popup("Good Bye")
            exit(0)
            
        except (socket.error, ConnectionRefusedError) as e:
            print("connection error")
        finally:
            sock.close()
# Main function to initiate the process            
def main():
    send_data()  
    window.close()  

if __name__ == "__main__":
    main()




