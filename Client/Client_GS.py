import socket
import os
import json
import PySimpleGUI as sg

# Initialize the socket
s = socket.socket()
host = '10.102.13.151'  # Localhost
port = 5000
s.bind((host, port))
s.listen(5)

# Get system information functions
def collect_data():
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

    return  {
        "Temperature": get_temp(),
        "Voltage": get_volt(),
        "Arm_Memory": get_Arm_memory(),
        "Arm_Clock": get_Clock_frequency(),
        "GPU_Memory": get_gpu_memory(),
    }

# Initialize GUI window
def gui_window():
    layout = [
        [sg.Text("Status:"), sg.Text(u"\u1F534", key="-STATUS-", font=("Helvetica", 20))],
        [sg.Button("Exit")],
        [sg.Text('', size=(30, 1), key='-Message-')],
    ]
    return sg.Window("Client Monitoring", layout)  # Return the window object

try:
    # Create the window
    window = gui_window()
    iteration_count = 0

    while True:
        event, values = window.read(timeout=2000)

        if event in (sg.WINDOW_CLOSED, "Exit"):
            window.close()
            break
        
        c.addr = s.accept()
        iteration_count +=1
        data = collect_data()
        data["Iteration"] = iteration_count
        
        jason_data = json.dumps(data)
        s.sendall(jason_data.encode("utf-8"))
        time.sleep(2)
        # Wait for a connection
        
        window['-STATUS-'].update("  Connected", text_color='green')
        
        if iteration_count >= 50:
            break

except KeyboardInterrupt:
    print("Good Bye")
    window.close()  # Close the window properly
    exit()