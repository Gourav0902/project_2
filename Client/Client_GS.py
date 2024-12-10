# This server runs on Pi, sends Pi's your 4 arguments from the vcgencmds, sent as Json object.

# details of the Pi's vcgencmds - https://www.tomshardware.com/how-to/raspberry-pi-benchmark-vcgencmd
# more vcgens on Pi 4, https://forums.raspberrypi.com/viewtopic.php?t=245733
# more of these at https://www.nicm.dev/vcgencmd/

import socket
import os, time
import json
import PySimpleGUI as sg
def Hardware_check():
    try:
        with open("/proc/cpuinfo", "r") as cpuinfo:
            for line in cpuinfo:
                if "Raspberry Pi" in line:
                    return True
    except FileNotFoundError:
        pass
    return false
if not Hardware_check():
    sg.pop("Check Device")
    exit(0)

s = socket.socket()
host = '' # Localhost
port = 5000
s.bind((host, port))
s.listen(5)
s.setblocking(False)
s.settimeout(1.0)

#gets the Core Temperature from Pi, ref https://github.com/nicmcd/vcgencmd/blob/master/README.md
def get_temp():
    t = os.popen('vcgencmd measure_temp').readline() #gets from the os, using vcgencmd - the core-temperature
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
# initialising json object string

ini_string = {"Temperature":get_temp(),
              "Voltage": get_volt(),
              "Arm_Memory":get_Arm_memory(),
              "Arm_Clock":get_Clock_frequency() ,
              "GPU_Memory": get_gpu_memory()
              }

f_dict = json.dumps(ini_string) # The eval() function evaluates JavaScript code represented as a string and returns its completion value.
sg. theme ('Light Brown 4')
CIRCLE = '⚫' # unicode symbol 9899
CIRCLE_OUTLINE = '⚪' # unicode symbol 9890

def LED(color, key) :
  
    return sg.Text(CIRCLE_OUTLINE, text_color=color, key=key)

layout = [
    [sg.Text('Status '), sg.Text('Disconnected', key="-STATUS-")],  
    [sg.Button("Exit")],
    [sg.Text('', size=(30, 1), key='-Message-')],
]

window = sg.Window("Client Monitoring",layout)

try:
    while True:
        try:
            c, addr = s.accept()
            print(f'Got connection from {addr}')
            window['-STATUS-'].update("Connected")
            res = bytes(str(f_dict), 'utf-8')  # Convert JSON string to byte format
            c.send(res)  # Send the data
            c.close()  # Properly close the connection after sending data
        except socket.timeout:
            # If no connection, just continue and allow the GUI to update
            pass

        # Read events from the GUI
        event, values = window.read(timeout=1000)  # Timeout of 100ms to allow non-blocking GUI interaction

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
except KeyboardInterrupt:
    print ("Good Bye")
finally:
    window.close()  # Ensure that the window is properly closed
    exit()