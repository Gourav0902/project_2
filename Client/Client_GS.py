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

def Hardware_check():
    try:
        with open("/proc/cpuinfo", "r") as cpuinfo:
            for line in cpuinfo:
                if "Raspberry Pi" in line:
                    return True
    except FileNotFoundError:
        pass
    return False

if not Hardware_check():
    sg.popup("Check Device")
    exit(0)


sock = socket. socket()
   

port = 5000
#address = "192.168.10.121" # of server, so we can read the vcgencmd data
address = "10.102.13.149"# to run on Pi with local server

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
sg.theme('Light Brown 4')
CIRCLE = '\u26AB'
CIRCLE_OUTLINE = '⚪'
def LED(color, key) :
    return sg.Text(CIRCLE_OUTLINE, text_color=color, key=key)
layout = [
    [sg.Text('Status '),LED('Green', '-LED0-'), sg.Text('Disconnected', key="-STATUS-")],  
    [sg.Button("Exit")],
    
]


window = sg.Window("Client Monitoring", layout, finalize = True)
def send_data():
      
        
        try:
            sock.connect((address, port))
            window['-STATUS-'].update("Connected")
            window['-LED0-'].update(CIRCLE)
            for i in range(50):
                jsonResult = {
                                    "Iteration": i+1,
                                    "Temperature": get_temp(),
                                    "Voltage": get_volt(),
                                    "Arm_Memory": get_Arm_memory(),
                                    "Arm_Clock": get_Clock_frequency(),
                                    "GPU_Memory": get_gpu_memory(),
                                    "Throttling": get_throttling()
                                }

                    #jsonResult = {"thing": [{"temp":"You're"}], "volts":v, "temp-core":core, "it =": i}

                jsonResult = json.dumps(jsonResult)
                jsonbyte = bytearray(jsonResult,"UTF-8")
                try:  
                    sock.send(jsonbyte)
                    
                    

                except (socket.error, ConnectionRefusedError): # = short form for getaddrinfo()
                    window['-STATUS-'].update("Disconnected")  # Update status to "Disconnected"
                    window['-LED0-'].update(CIRCLE_OUTLINE)  # Change LED to disconnected color
                    print("Connection lost")
                    break
                time.sleep(2)
                
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
def main():
    send_data()  # Start the data transmission and GUI updates loop
    window.close()  # Close the window after the loop ends

if __name__ == "__main__":
    main()




