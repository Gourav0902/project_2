import socket
import sys
import json, time
import os, io
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
address = "10.102.13.191"# to run on Pi with local server

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
sg.theme('Light Brown 4')

layout = [
    [sg.Text('Status '), sg.Text('Disconnected', key="-STATUS-")],  
    [sg.Button("Exit")],
    
]

window = sg.Window("Client Monitoring", layout)
while True:
    try:
        event, values = window.read(timeout=100)  # Timeout of 100ms to allow non-blocking GUI interaction

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        try:
            sock.connect((address, port))
           
            for i in range(50):
                jsonResult = {
                                "Temperature": get_temp(),
                                "Voltage": get_volt(),
                                "Arm_Memory": get_Arm_memory(),
                                "Arm_Clock": get_Clock_frequency(),
                                "GPU_Memory": get_gpu_memory()
                            }

                #jsonResult = {"thing": [{"temp":"You're"}], "volts":v, "temp-core":core, "it =": i}

                jsonResult = json.dumps(jsonResult)
                jsonbyte = bytearray(jsonResult,"UTF-8")
                
                

                #print(v, " it = ",i, " ",core)
                #sock. send(jsonResult)
                sock.send(jsonbyte)
                window['-STATUS-'].update("Connected")
                time.sleep(2)

        except socket.gaierror: # = short form for getaddrinfo()

            print('There an error resolving the host')
            sock.close()
            
    except KeyboardInterrupt:
        print("Good Bye")
        break
    finally:
        print("Good Bye")
        exit()