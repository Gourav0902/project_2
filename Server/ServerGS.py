import socket
import os, time
import json

s = socket.socket()
host = ''
port = 5000
s.blind((host, port))
s.listen(5)

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



try:
    while True:
      c, addr = s.accept()
      print ('Got connection from',addr)
      res = bytes(str(f_dict), 'utf-8') # needs to be a byte
      c.send(res) # sends data as a byte type
except KeyboardInterrupt:
    print ("Good Bye")
    exit()

