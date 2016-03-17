##Hardware execute funtions

import visa as vs
import numpy as np
import time
import serial
import serial.tools.list_ports
import gui
import agilent_func2 as agi
##import RSA_GUI026 as RSA


######################################################################################################################3
####################################HARDWARE CONTROL####################################################################3

def mode_sel(my_instrument,mode,filenm,centre_freq, span,ref, att, r_bw, max_hold, max_hold_time, avg, avg_times, base_file,gain,cal):
    
    ser_state=serial_connect(mode)
    
    if ser_state==True:
        agi.agilent(my_instrument,centre_freq, span,ref, att, r_bw, max_hold, max_hold_time, avg, avg_times, base_file,gain,cal)

def mode_sel_no_ware(my_instrument,mode,filenm,centre_freq, span,ref, att, r_bw, max_hold, max_hold_time, avg, avg_times, base_file,gain,cal):
    agi.agilent(my_instrument,centre_freq, span,ref, att, r_bw, max_hold, max_hold_time, avg, avg_times, base_file,gain,cal)

def test(evt):
    base_file=mywin['notebook']['tabpanel_184']['panel_169']['textbox_160'].value
##    print base_file
    print 'hallo'


def serial_connect(command):

    print 'Connecting to Arduino'
    ports = list(serial.tools.list_ports.comports())
    connected = 0
    for p in ports:
        if "Arduino" in str(p):
                print str(p)
                connected = 1
                s=str(p)
                SERIALPORT = s[s.find("'")+1:s.find("'")+5]
    if connected != 1:
        sys_mes('No Arduino connected. Please try again should you require hardware control')
        ctr_state=False
    else:
        try:
            ser = serial.Serial(SERIALPORT, 9600, timeout=3.0)   
        except serial.SerialException:
            print "failed to write to port %s" % SERIALPORT
        time.sleep(2)
        ser.write(command)
        ##time.sleep(3)
        rx_mes = ser.readline()
        mes = 'Hardware set to state: %s'  %rx_mes
        sys_mes(mes)
        ser.close()
        ctr_state=True
    return ctr_state


def sys_mes(mess):
    import wx, sys
    gui.alert(mess)
