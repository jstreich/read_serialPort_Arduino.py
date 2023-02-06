###########################################################################
##### Script listens to serial port and writes contents into a file #######
###########################################################################
## requires pySerial to be installed 

import serial  # sudo pip install pyserial should work
from datetime import datetime
import time as tm
import subprocess
import os
import os.path
from os import path
import numpy
import statistics
import os


###########################################################################
############################# Define file UID #############################
###########################################################################

##### Define input file name to append to
filename = input('Input the filename record to save as, without extension .txt and any spaces use an underscore or dash:\n')

##### Connect to Arduino via Serial port
serial_port = '/dev/cu.usbserial-1410';
baud_rate = 9600; #In arduino, Serial.begin(baud_rate)
ser = serial.Serial(serial_port, baud_rate)

##### Define beep sound
beep = lambda x: os.system("echo -n '\a';sleep 0.2;" * x)

LF = '\n'
CRLF = '\r\n'

def mean(data):
    """Return the sample arithmetic mean of data."""
    n = len(data)
    if n < 1:
        raise ValueError('mean requires at least one data point')
    return sum(data)/n # in Python 2 use sum(data)/float(n)

def _ss(data):
    """Return sum of square deviations of sequence data."""
    c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss

def stddev(data, ddof=0):
    """Calculates the population standard deviation
    by default; specify ddof=1 to compute the sample
    standard deviation."""
    n = len(data)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    ss = _ss(data)
    pvar = ss/(n-ddof)
    return pvar**0.5


##### Set to step 1
step = 1

while step != 0:

##### Step 1
  if step == 1:
    os.system("say Get Barcode")
    samp = input('Get sample ID, typed, RFID reader, or Barcode reader = ')
    step = 2

##### Step 2
  if step == 2:
    os.system("say Get Leaf Measurement")
    x = input("press enter to mearsure Leaf")
    j = 1
    lines = ser.readline();
    lines = lines.decode("utf-8") #ser.readline returns a binary, convert to string
    lines = str(lines)
    lines = lines.rstrip()
    lines = str(lines + "\t")
    while j <= 50:
      line = ser.readline();
      line = line.decode("utf-8") #ser.readline returns a binary, convert to string
      line = line.rstrip()
      #line = line.rstrip('\r')
      lines = str(str(lines) + "\t" + str(line))
      j += 1
    leaf=lines
    step = 3

##### Step 3
  if step == 3:
    os.system("say Get Pet e ole")
    x = input("Get Petiole")
    j = 1
    lines = ser.readline();
    lines = lines.decode("utf-8") #ser.readline returns a binary, convert to string
    lines = str(lines)
    lines = lines.rstrip()
    lines = str(lines + "\t")
    while j <= 50:
      line = ser.readline();
      line = line.decode("utf-8") #ser.readline returns a binary, convert to string
      line = line.rstrip()
      #line = line.rstrip('\r')
      lines = str(str(lines) + "\t" + str(line))
      j += 1
    pet = lines
    beep(2)
    step = 4

##### Step 4
  if step == 4:
    os.system("say Get Blank Measurement")
    x = input("Get Blank Measurement")
    j = 1
    lines = ser.readline();
    lines = lines.decode("utf-8") #ser.readline returns a binary, convert to string
    lines = str(lines)
    lines = lines.rstrip()
    lines = str(lines + "\t")
    while j <= 50:
      line = ser.readline();
      line = line.decode("utf-8") #ser.readline returns a binary, convert to string
      line = line.rstrip()
      #line = line.rstrip('\r')
      lines = str(str(lines) + "\t" + str(line))
      j += 1
    blank = lines
    beep(2)
    step = 5

##### Step 5
  if step == 5:
    time=datetime.now() #format date as year:month:day:hour:min:sec
    f_time = str(time.year) + ':' + str(time.month) + ":" + str(time.day) + ":" + str(time.hour) + ":" + str(time.minute) + ":" + str(time.second)
    file = open(filename,'a')
    file.write(str(samp) + "\t" + str(f_time) + "\t" + str(leaf) + "\t" + str(pet) + "\t" + str(blank) + "\n")
    file.close()  
    print("--------------------------------------")
    print("---------- Get Next Sample -----------")
    print("--------------------------------------")
    step = 1






###############################
########### Citation ##########
###############################
# 1. https://stackoverflow.com/questions/40480737/how-to-write-data-to-a-text-file-on-arduino
