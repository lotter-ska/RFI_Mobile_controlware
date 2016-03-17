#!/usr/bin/python
# -*- coding: utf-8 -*-

"Minimal gui2py application (to be used as skeleton)"

from __future__ import with_statement   # for python 2.5 compatibility

__author__ = "Lotter Kock"
__copyright__ = "SKA"
__license__ = "LGPL 3.0"

import gui


##import RSA5106A_Control_Functions003 as RSA_Control
import hardware01 as hw
import numpy as np
import time
import os.path
import visa
##from threading import Thread
##import sys

# --- here goes your event handlers ---
####################################################################################################################333
def check_file_name():
    file_test=mywin['notebook']['tabpanel_184']['panel_169']['textbox_160'].value
    if file_test=="":
        filestat=False
        sys_mes('Please enter a filename')
    elif os.path.isfile(file_test)==True:
        filestat=gui.confirm('Append data file?','File already exists')
    else:
        filestat=True
    return filestat


def sys_mes(mess):
    import wx, sys
    gui.alert(mess)


##check if gpib is connected and then check if it is agilent or tektronix
def check_for_analyzer():
    rm = visa.ResourceManager()
    ss=rm.list_resources()
    if 'GPIB0' in str(ss):
        print 'Found GPIB Object'
        
        for p in ss:
                if "GPIB" in str(p):
                        GPIB_port = str(p)
                        
        my_instrument = rm.open_resource(GPIB_port)
        try:
            sa_name=my_instrument.query("ID?")
            sa='HP'
        except:
            sa_name=my_instrument.query("*IDN?")
            sa='TEK'
        
        gpib=True
    else:
        sys_mes('Please check your connection to the Spectrum Analyzer')
        gpib=False
        sa='NOT'
    return gpib, sa, my_instrument



def int_or_hold(evt):
##    print 'change'
    if (mywin['notebook']['tabpanel_184']['panel_217_164']['checkbox_250_146'].value and mywin['notebook']['tabpanel_184']['panel_217_164']['checkbox_250'].value)==True:
        mywin['notebook']['tabpanel_184']['panel_217_164']['checkbox_250_146'].value=False
        mywin['notebook']['tabpanel_184']['panel_217_164']['checkbox_250'].value=False

    

#################################################################################################################3
#################################################################################################################3
#################################################################################################################3
    


def mode_main(mode,centre_freq,span,gain,cal,No_ware):
    z=check_file_name()
    gpib, sa, my_instrument=check_for_analyzer()
    if z==True and gpib==True:
        
        base_file=mywin['notebook']['tabpanel_184']['panel_169']['textbox_160'].value
        max_hold=mywin['notebook']['tabpanel_184']['panel_217_164']['checkbox_250'].value
        avg=mywin['notebook']['tabpanel_184']['panel_217_164']['checkbox_250_146'].value
        att=mywin['notebook']['tabpanel_184']['panel_217_164']['combobox_173'].value
        if att==[]:
            att='0'
        r_bw=mywin['notebook']['tabpanel_184']['panel_217_164']['combobox_177'].value
        if r_bw==[]:
            r_bw='2e6'
        ref=mywin['notebook']['tabpanel_184']['panel_217_164']['textbox_528_168_436_833'].value        
        max_hold_time=mywin['notebook']['tabpanel_184']['panel_217_164']['textbox_528_168_625'].value
        avg_times=mywin['notebook']['tabpanel_184']['panel_217_164']['textbox_528_168_625_169'].value

        if No_ware==True:
            hw.mode_sel_no_ware(my_instrument,mode,base_file,centre_freq, span,ref, att, r_bw, max_hold, max_hold_time, avg, avg_times, base_file,gain,cal)
        else:
            hw.mode_sel(my_instrument,mode,base_file,centre_freq, span,ref, att, r_bw, max_hold, max_hold_time, avg, avg_times, base_file,gain,cal)
        



def mode_no_ware(evt):
    mode='MOD_no'
    gain=0
    cal=False
    
    if (mywin['notebook']['tabpanel_184']['panel_215']['textbox_256'].value)==[] or (mywin['notebook']['tabpanel_184']['panel_215']['textbox_256_492'].value)==[]:
        sys_mes('Please enter valid freq.')
    else:
        span=float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256'].value)-float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256_492'].value)
        centre_freq=float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256_492'].value)+span/2
        No_ware=True
        mode_main(mode,centre_freq,span,gain,cal,No_ware)
        





def mode0(evt):
    mode='MOD0'
    span=2e9-100e3
    centre_freq=100e3+span/2
    gain=42
    cal=False
    No_ware=False
    if mywin['notebook']['tabpanel_184']['panel_215']['checkbox_184'].value==True:
        if float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256'].value)>2e9 or float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256_492'].value)<100e3:
            sys_mes('Please check Frequencies')
        else:
            span=float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256'].value)-float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256_492'].value)
            centre_freq=float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256_492'].value)+span/2
            print span
            mode_main(mode,centre_freq,span,gain,cal,No_ware)
    else:
        
        mode_main(mode,centre_freq,span,gain,cal,No_ware)

    

def mode1(evt):
    mode='MOD1'
    fstart=0.85e9
    fstop=6e9
    span=fstop-fstart
    centre_freq=fstart+span/2
    gain=42
    cal=False
    No_ware=False
    if mywin['notebook']['tabpanel_184']['panel_215']['checkbox_184'].value==True:
        if float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256'].value)>fstop or float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256_492'].value)<fstart:
            sys_mes('Please check Frequencies')
        else:
            span=float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256'].value)-float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256_492'].value)
            centre_freq=float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256_492'].value)+span/2
            print span
            mode_main(mode,centre_freq,span,gain,cal,No_ware)
    else:
        mode_main(mode,centre_freq,span,gain,cal,No_ware)

def mode2(evt):
    mode='MOD2'
    fstart=0.85e9
    fstop=26.5e9
    span=fstop-fstart
    centre_freq=fstart+span/2
    gain=42
    cal=True
    No_ware=False
    if mywin['notebook']['tabpanel_184']['panel_215']['checkbox_184'].value==True:
        if float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256'].value)>fstop or float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256_492'].value)<fstart:
            sys_mes('Please check Frequencies')
        else:
            span=float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256'].value)-float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256_492'].value)
            centre_freq=float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256_492'].value)+span/2
            print span
            mode_main(mode,centre_freq,span,gain,cal,No_ware)
    else:
        mode_main(mode,centre_freq,span,gain,cal,No_ware)

def mode3(evt):
    mode='MOD3'
    fstart=0.1e9
    fstop=2e9
    span=fstop-fstart
    centre_freq=fstart+span/2
    gain=14
    cal=False
    No_ware=False
    if mywin['notebook']['tabpanel_184']['panel_215']['checkbox_184'].value==True:
        if float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256'].value)>fstop or float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256_492'].value)<fstart:
            sys_mes('Please check Frequencies')
        else:
            span=float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256'].value)-float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256_492'].value)
            centre_freq=float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256_492'].value)+span/2
            print span
            mode_main(mode,centre_freq,span,gain,cal,No_ware)
    else:
        mode_main(mode,centre_freq,span,gain,cal,No_ware)
   

def mode4(evt):
    mode='MOD4'
    fstart=0.85e9
    fstop=12e9
    span=fstop-fstart
    centre_freq=fstart+span/2
    gain=14
    cal=False
    No_ware=False
    if mywin['notebook']['tabpanel_184']['panel_215']['checkbox_184'].value==True:
        if float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256'].value)>fstop or float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256_492'].value)<fstart:
            sys_mes('Please check Frequencies')
        else:
            span=float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256'].value)-float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256_492'].value)
            centre_freq=float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256_492'].value)+span/2
            print span
            mode_main(mode,centre_freq,span,gain,cal,No_ware)
    else:
        mode_main(mode,centre_freq,span,gain,cal,No_ware)


def mode5(evt):
    mode='MOD5'
    fstart=0.85e9
    fstop=26.5e9
    span=fstop-fstart
    centre_freq=fstart+span/2
    gain=14
    cal=True
    No_ware=False
    if mywin['notebook']['tabpanel_184']['panel_215']['checkbox_184'].value==True:
        if float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256'].value)>fstop or float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256_492'].value)<fstart:
            sys_mes('Please check Frequencies')
        else:
            span=float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256'].value)-float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256_492'].value)
            centre_freq=float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256_492'].value)+span/2
            print span
            mode_main(mode,centre_freq,span,gain,cal,No_ware)
    else:
        mode_main(mode,centre_freq,span,gain,cal,No_ware)

def mode6(evt):
    mode='MOD6'
    fstart=0.85e9
    fstop=26.5e9
    span=fstop-fstart
    centre_freq=fstart+span/2
    gain=0
    cal=False
    No_ware=False
    if mywin['notebook']['tabpanel_184']['panel_215']['checkbox_184'].value==True:
        if float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256'].value)>fstop or float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256_492'].value)<fstart:
            sys_mes('Please check Frequencies')
        else:
            span=float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256'].value)-float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256_492'].value)
            centre_freq=float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256_492'].value)+span/2
            print span
            mode_main(mode,centre_freq,span,gain,cal,No_ware)
    else:
        mode_main(mode,centre_freq,span,gain,cal,No_ware)

def mode7(evt):
    mode='MOD7'
    fstart=0.85e9
    fstop=26.5e9
    span=fstop-fstart
    centre_freq=fstart+span/2
    gain=0
    cal=True
    No_ware=False
    if mywin['notebook']['tabpanel_184']['panel_215']['checkbox_184'].value==True:
        if float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256'].value)>fstop or float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256_492'].value)<fstart:
            sys_mes('Please check Frequencies')
        else:
            span=float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256'].value)-float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256_492'].value)
            centre_freq=float(mywin['notebook']['tabpanel_184']['panel_215']['textbox_256_492'].value)+span/2
            print span
            mode_main(mode,centre_freq,span,gain,cal,No_ware)
    else:
        mode_main(mode,centre_freq,span,gain,cal,No_ware)


    
#################################################################################################################3
#################################################################################################################3
def show_max_time(evt):
    acq_bw=float(mywin['notebook']['tabpanel']['freq_191']['combobox_248'].value)
    if acq_bw==0.3125:
        acq_length = 1374.0        
    if acq_bw==0.625:
        acq_length = 687.193        
    if acq_bw==1.25:
        acq_length = 343.596        
    if acq_bw==2.50:
        acq_length = 171.798        
    if acq_bw==5.00:
        acq_length = 152.710       
    if acq_bw==10.0:
        acq_length = 76.355        
    if acq_bw==20.0:
        acq_length = 38.177        
    if acq_bw==25.0:
        acq_length = 30.542       
    if acq_bw==30.0:
        acq_length = 28.633       
    if acq_bw==60:
        acq_length = 14.317       
    if acq_bw==110:
        acq_length = 7.158
    
    mywin['notebook']['tabpanel']['freq_191']['label_715_163_193'].text = 'Acq T(Max = %s )' % acq_length
    if float(mywin['notebook']['tabpanel']['freq_191']['time_ac'].value) > acq_length:
        mywin['notebook']['tabpanel']['freq_191']['time_ac'].value = str(acq_length)

def show_max_time1(evt):
    acq_bw=float(mywin['notebook']['tabpanel_184']['panel_217']['combobox_166'].value)
    if acq_bw==0.3125:
        acq_length = 1374.0        
    if acq_bw==0.625:
        acq_length = 687.193        
    if acq_bw==1.25:
        acq_length = 343.596        
    if acq_bw==2.50:
        acq_length = 171.798        
    if acq_bw==5.00:
        acq_length = 152.710       
    if acq_bw==10.0:
        acq_length = 76.355        
    if acq_bw==20.0:
        acq_length = 38.177        
    if acq_bw==25.0:
        acq_length = 30.542       
    if acq_bw==30.0:
        acq_length = 28.633       
    if acq_bw==60:
        acq_length = 14.317       
    if acq_bw==110:
        acq_length = 7.158
    
    mywin['notebook']['tabpanel_184']['panel_217']['label_474'].text = 'Acq T(Max = %s )' % acq_length
    if float(mywin['notebook']['tabpanel_184']['panel_217']['textbox_528'].value) > acq_length:
        mywin['notebook']['tabpanel_184']['panel_217']['textbox_528'].value = str(acq_length)

#################################################################################################################3
#################################################################################################################3
#################################################################################################################3
def check_max(evt):
    try:
        acq_length=float(mywin['notebook']['tabpanel']['freq_191']['time_ac'].value)
        acq_bw=float(mywin['notebook']['tabpanel']['freq_191']['combobox_248'].value)
        if acq_bw==0.3125 and acq_length > 1374.0:
            sys_mes('Check Acq Time')
            acq_length=1374.0
            mywin['notebook']['tabpanel']['freq_191']['time_ac'].value = str(acq_length)
        if acq_bw==0.625 and acq_length > 687.193:
            sys_mes('Check Acq Time')
            acq_length=687.193
            mywin['notebook']['tabpanel']['freq_191']['time_ac'].value = str(acq_length)
        if acq_bw==1.25 and acq_length > 343.596:
            sys_mes('Check Acq Time')
            acq_length=343.596
            mywin['notebook']['tabpanel']['freq_191']['time_ac'].value = str(acq_length)
        if acq_bw==2.50 and acq_length > 171.798:
            sys_mes('Check Acq Time')
            acq_length=171.798
            mywin['notebook']['tabpanel']['freq_191']['time_ac'].value = str(acq_length)
        if acq_bw==5.00 and acq_length > 152.710:
            sys_mes('Check Acq Time')
            acq_length=152.710
            mywin['notebook']['tabpanel']['freq_191']['time_ac'].value = str(acq_length)
        if acq_bw==10.0 and acq_length > 76.355:
            sys_mes('Check Acq Time')
            acq_length=76.355
            mywin['notebook']['tabpanel']['freq_191']['time_ac'].value = str(acq_length)
        if acq_bw==20.0 and acq_length > 38.177:
            sys_mes('Check Acq Time')
            acq_length=38.177
            mywin['notebook']['tabpanel']['freq_191']['time_ac'].value = str(acq_length)
        if acq_bw==25.0 and acq_length > 30.542:
            sys_mes('Check Acq Time')
            acq_length=30.542
            mywin['notebook']['tabpanel']['freq_191']['time_ac'].value = str(acq_length)
        if acq_bw==30.0 and acq_length > 28.633:
            sys_mes('Check Acq Time')
            acq_length=28.633
            mywin['notebook']['tabpanel']['freq_191']['time_ac'].value = str(acq_length)
        if acq_bw==60 and acq_length > 14.317:
            sys_mes('Check Acq Time')
            acq_length=14.317
            mywin['notebook']['tabpanel']['freq_191']['time_ac'].value = str(acq_length)
        if acq_bw==110 and acq_length > 7.158:
            sys_mes('Check Acq Time')
            acq_length=7.158
            mywin['notebook']['tabpanel']['freq_191']['time_ac'].value = str(acq_length)
    except ValueError:
        sys_mes('NaN')
        mywin['notebook']['tabpanel']['freq_191']['time_ac'].value = str(7)



def check_max1(evt):
    try:
        acq_length=float(mywin['notebook']['tabpanel_184']['panel_217']['textbox_528'].value)
        acq_bw=float(mywin['notebook']['tabpanel_184']['panel_217']['combobox_166'].value)
        if acq_bw==0.3125 and acq_length > 1374.0:
            sys_mes('Check Acq Time')
            acq_length=1374.0
            mywin['notebook']['tabpanel_184']['panel_217']['textbox_528'].value = str(acq_length)
        if acq_bw==0.625 and acq_length > 687.193:
            sys_mes('Check Acq Time')
            acq_length=687.193
            mywin['notebook']['tabpanel_184']['panel_217']['textbox_528'].value = str(acq_length)
        if acq_bw==1.25 and acq_length > 343.596:
            sys_mes('Check Acq Time')
            acq_length=343.596
            mywin['notebook']['tabpanel_184']['panel_217']['textbox_528'].value = str(acq_length)
        if acq_bw==2.50 and acq_length > 171.798:
            sys_mes('Check Acq Time')
            acq_length=171.798
            mywin['notebook']['tabpanel_184']['panel_217']['textbox_528'].value = str(acq_length)
        if acq_bw==5.00 and acq_length > 152.710:
            sys_mes('Check Acq Time')
            acq_length=152.710
            mywin['notebook']['tabpanel_184']['panel_217']['textbox_528'].value = str(acq_length)
        if acq_bw==10.0 and acq_length > 76.355:
            sys_mes('Check Acq Time')
            acq_length=76.355
            mywin['notebook']['tabpanel_184']['panel_217']['textbox_528'].value = str(acq_length)
        if acq_bw==20.0 and acq_length > 38.177:
            sys_mes('Check Acq Time')
            acq_length=38.177
            mywin['notebook']['tabpanel_184']['panel_217']['textbox_528'].value = str(acq_length)
        if acq_bw==25.0 and acq_length > 30.542:
            sys_mes('Check Acq Time')
            acq_length=30.542
            mywin['notebook']['tabpanel_184']['panel_217']['textbox_528'].value = str(acq_length)
        if acq_bw==30.0 and acq_length > 28.633:
            sys_mes('Check Acq Time')
            acq_length=28.633
            mywin['notebook']['tabpanel_184']['panel_217']['textbox_528'].value = str(acq_length)
        if acq_bw==60 and acq_length > 14.317:
            sys_mes('Check Acq Time')
            acq_length=14.317
            mywin['notebook']['tabpanel_184']['panel_217']['textbox_528'].value = str(acq_length)
        if acq_bw==110 and acq_length > 7.158:
            sys_mes('Check Acq Time')
            acq_length=7.158
            mywin['notebook']['tabpanel_184']['panel_217']['textbox_528'].value = str(acq_length)
    except ValueError:
        sys_mes('NaN')
        mywin['notebook']['tabpanel_184']['panel_217']['textbox_528'].value = str(7)

#################################################################################################################3
#################################################################################################################3
#################################################################################################################3
#####

def init1(evt):
    resource_name='GPIB0::1'
    [GPIB_Found, RSA, IDN_company, IDN_model, IDN_serial, IDN_firmware, RSA_OPT] = RSA_Control.GPIB_Init(resource_name)

    ## To move into if TRUE:
    ## Get Variable values from GUI
    
    Fstart=1e6*float(mywin['notebook']['tabpanel']['freq']['textbox_244_161'].value)
    Fstop=1e6*float(mywin['notebook']['tabpanel']['freq']['textbox_491_1217_165'].value)
    acq_bw=float(mywin['notebook']['tabpanel']['freq_191']['combobox_248'].value)
    preamp=mywin['notebook']['tabpanel']['ampl']['checkbox_187'].value
    ref=mywin['notebook']['tabpanel']['ampl']['textbox_491_1217_165_175'].value
    att=mywin['notebook']['tabpanel']['ampl']['textbox_244_161_171'].value
    acq_length=float(mywin['notebook']['tabpanel_184']['panel_217']['textbox_528'].value)
    
##    ref
##    att
##    acq_time
    if acq_bw==0.3125:
        
        samples = acq_length/2600e-9
    if acq_bw==0.625:
        
        samples = acq_length/1300e-9
    if acq_bw==1.25:
        
        samples = acq_length/640e-9
    if acq_bw==2.50:
        
        samples = acq_length/320e-9
    if acq_bw==5.00:
        
        samples = acq_length/160e-9
    if acq_bw==10.0:
        
        samples = acq_length/80e-9
    if acq_bw==20.0:
        
        samples = acq_length/40e-9
    if acq_bw==25.0:
        
        samples = acq_length/32e-9
    if acq_bw==30.0:
        
        samples = acq_length/26.7e-9
    if acq_bw==60:
        
        samples = acq_length/13.3e-9
    if acq_bw==110:
        
        samples = acq_length/6.7e-9


    ##############################3
    print Fstart
    spanf = Fstop - Fstart
    cenf = spanf/2 + Fstart
    print Fstart
    print Fstop
    print spanf
    print cenf
    print ref
    print samples
    if GPIB_Found == True:
        print RSA

        RSA_Control.GPIB_SetFreq(cenf,spanf,RSA)
##        RSA_Control.GPIB_SetAcq(ref, att, acq_length, acq_bw, samples, RSA, preamp)

    else:
        print 'nada'



####################################################################################################################333

# --- gui2py designer generated code starts ---

with gui.Window(name='mywin', title=u'Frequency Setup', resizable=True, 
                height='835px', left='60', top='60', width='825px', 
                bgcolor=u'#ABABAB', fgcolor=u'#000000', image='', ):
    with gui.Notebook(name='notebook', height='846', left='3', top='6', 
                      width='811', selection=1, ):
        with gui.TabPanel(id=171, name='tabpanel', selected=False, 
                          text=u'Reverb Lab Test', visible=False, ):
            gui.Button(id=170, label=u'Set Values', name='button', left='473', 
                       top='761', fgcolor=u'#000000', )
            with gui.Panel(id=160, label=u'Frequency Setup', name=u'freq', 
                           height='112', left='24', top='88', width='761', 
                           bgcolor=u'#F0F0F0', fgcolor=u'#000000', image='', ):
                gui.TextBox(id=161, name='textbox_244_161', height='28', 
                            left='148', top='40', width='100', text=u'70', 
                            value=u'70', )
                gui.Label(id=163, name='label_715_163', height='22', 
                          left='404', top='45', width='105', 
                          text=u'Stop Freq (MHz)', )
                gui.TextBox(id=165, name='textbox_491_1217_165', height='28', 
                            left='532', top='41', width='100', text=u'6000', 
                            value=u'6000', )
                gui.Label(id=166, name='label_715_1007_1453_166', height='22', 
                          left='14', top='39', width='105', 
                          text=u'Start Freq (MHz)', )
            with gui.Panel(id=179, label=u'New Data File Name', 
                           name=u'File_name', height='71', left='20', 
                           top='10', width='761', bgcolor=u'#F0F0F0', 
                           fgcolor=u'#000000', image='', ):
                gui.TextBox(id=288, name=u'filename', height='31', left='41', 
                            top='30', width='638', bgcolor=u'#FFFFFF', 
                            fgcolor=u'#000000', )
            with gui.Panel(id=170, 
                           label=u'Amplitude Setup - Spectrum Analyzer', 
                           name=u'ampl', height='105', left='14', top='343', 
                           width='761', bgcolor=u'#F0F0F0', 
                           fgcolor=u'#000000', image='', ):
                gui.TextBox(id=171, name='textbox_244_161_171', height='28', 
                            left='148', top='40', width='100', text=u'0', 
                            value=u'0', )
                gui.Label(id=173, name='label_715_163_173', height='22', 
                          left='273', top='40', width='105', 
                          text=u'Ref Level (dBm)', )
                gui.Label(id=174, name='label_715_1007_164_174', height='22', 
                          left='528', top='41', width='92', text=u'Preamp', )
                gui.TextBox(id=175, name='textbox_491_1217_165_175', 
                            height='28', left='404', top='39', width='100', 
                            text=u'-30', value=u'-30', )
                gui.Label(id=176, name='label_715_1007_1453_166_176', 
                          height='22', left='14', top='39', width='105', 
                          text=u'Attenuation (dB)', )
                gui.CheckBox(id=187, label=u'On/Off', name='checkbox_187', 
                             height='20', left='662', top='43', width='75', 
                             bgcolor=u'#F0F0F0', fgcolor=u'#000000', )
            with gui.Panel(id=191, label=u'Acquisition Setup', 
                           name=u'freq_191', height='112', left='20', 
                           top='212', width='761', bgcolor=u'#F0F0F0', 
                           fgcolor=u'#000000', image='', ):
                gui.Label(id=193, name='label_715_163_193', height='22', 
                          left='412', top='44', width='109', 
                          text=u'Acquisition Time (s)', )
                gui.TextBox(id=194, name='time_ac', height='28', left='565', 
                            top='44', width='100', text=u'1', value=u'1', )
                gui.Label(id=195, name='label_715_1007_1453_166_195', 
                          height='22', left='14', top='46', width='109', 
                          text=u'Acquisition BW(MHz)', )
                gui.ComboBox(id=248, name='combobox_248', left='176', 
                             top='46', helptext=u'110', 
                             items=[u'0.3125', u'0.625', u'1.25', u'2.50', u'5.00', u'10.0', u'20.0', u'25.0', u'30.0', u'60.0', u'110.0'], )
        with gui.TabPanel(id=184, name='tabpanel_184', selected=True, 
                          text=u'Field Tests - Mode Select', ):
            with gui.Panel(id=169, label=u'New Data File Name', 
                           name='panel_169', height='71', left='19', top='8', 
                           width='761', bgcolor=u'#F0F0F0', 
                           fgcolor=u'#000000', image='', ):
                gui.TextBox(id=160, name='textbox_160', height='31', 
                            left='41', top='30', width='638', 
                            bgcolor=u'#FFFFFF', fgcolor=u'#000000',text=u'data.txt', 
                            value=u'data.txt', )
            with gui.Panel(id=163, label=u'Mode Selection', name='panel_163', 
                           height='361', left='18', top='77', width='477', 
                           helptext=u'Mode Selection:  Gain and freq will be assigned as per label.  If Mode Freq Override is selected, that freq range will be selected', 
                           image='', ):
                gui.Button(id=538, label=u'Mode 1', name='button_538', 
                           left='25', top='40', fgcolor=u'#000000', )
                gui.Button(id=223, label=u'Mode 2', name='button_223', 
                           left='25', top='80', fgcolor=u'#000000', )
                gui.Button(id=385, label=u'Mode 3', name='button_385', 
                           left='25', top='120', fgcolor=u'#000000', )
                gui.Button(id=469, label=u'Mode 4', name='button_469', 
                           left='25', top='160', fgcolor=u'#000000', )
                gui.Button(id=413, label=u'Mode 5', name='button_413', 
                           left='25', top='200', fgcolor=u'#000000', )
                gui.Button(id=337, label=u'Mode 6', name='button_337', 
                           left='25', top='240', fgcolor=u'#000000', )
                gui.Button(id=441, label=u'Mode 7', name='button_441', 
                           left='25', top='280', fgcolor=u'#000000', )
                gui.Button(id=497, label=u'Mode 8', name='button_497', 
                           left='25', top='320', fgcolor=u'#000000', )
                gui.Label(id=642, name='label_642', left='175', top='40', 
                          text=u'0.1-2 GHz;  42dB Gain', )
                gui.Label(id=728, name='label_728', left='175', top='80', 
                          text=u'0.85-6 GHz; 42dB Gain', )
                gui.Label(id=783, name='label_783', left='175', top='120', 
                          text=u'0.85-26.5 GHz; 42dB Gain; High gain Cal.', )
                gui.Label(id=815, name='label_815', left='175', top='160', 
                          text=u'0.1-2 GHz; 14dB Gain', )
                gui.Label(id=897, name='label_897', left='175', top='200', 
                          text=u'0.85-12\tGHz; 14dB Gain', )
                gui.Label(id=987, name='label_987', left='175', top='240', 
                          text=u'0.85-26.5 GHz; 14dB Gain; Medium gain Cal.', )
                gui.Label(id=160, name='label_160', left='175', top='280', 
                          text=u'0.85-26.5 GHz; 0dB Gain', )
                gui.Label(id=190, name='label_190', left='175', top='320', 
                          text=u'0.85-26.5 GHz; 0dB Gain; Zero gain Cal.', )
            with gui.Panel(id=217, 
                           label=u'Spectrum Analyzer Setup -TEKTRONIX', 
                           name='panel_217', height='87', left='22', 
                           top='570', width='751', bgcolor=u'#F0F0F0', 
                           fgcolor=u'#000000', image='', ):
                gui.Label(id=261, name='label_261', left='25', top='28', 
                          text=u'Acquisition BW(MHz)', )
                gui.ComboBox(id=166, name='combobox_166', left='184', 
                             top='24', 
                             items=[u'0.3125', u'0.625', u'1.25', u'2.50', u'5.00', u'10.0', u'20.0', u'25.0', u'30.0', u'60.0', u'110.0'], )
                gui.Label(id=474, name='label_474', left='350', top='26', 
                          text=u'Acquisition Time (s)', )
                gui.TextBox(id=528, name='textbox_528', left='493', top='23', 
                            text=u'1', value=u'1', )
            with gui.Panel(id=164, label=u'Spectrum Analyzer Setup -AGILENT', 
                           name='panel_217_164', height='122', left='20', 
                           top='446', width='756', bgcolor=u'#F0F0F0', 
                           fgcolor=u'#000000', image='', ):
                gui.Label(id=165, name='label_261_165', height='22', 
                          left='602', top='72', width='142', text=u'x Sweeps', )
                gui.Label(id=167, name='label_474_167', height='22', 
                          left='525', top='27', width='131', 
                          text=u'Attenuation', )
                gui.Label(id=196, name='label_261_165_196', height='22', 
                          left='25', top='28', width='82', 
                          text=u'Res BW (Hz)', )
                gui.TextBox(id=625, name='textbox_528_168_625', height='28', 
                            left='520', top='70', width='54', text=u'1', 
                            value=u'1', )
                gui.Label(id=781, name='label_474_167_781', height='22', 
                          left='282', top='28', width='89', 
                          text=u'Ref Lvl (dBm)', )
                gui.TextBox(id=833, name='textbox_528_168_436_833', 
                            height='28', left='394', top='26', width='100', 
                            text=u'-30', value=u'-30', )
                gui.CheckBox(id=146, label=u'Int', name='checkbox_250_146', 
                             height='20', left='23', top='74', width='75', 
                             bgcolor=u'#F0F0F0', fgcolor=u'#000000', )
                gui.CheckBox(id=250, label=u'Max H', name='checkbox_250', 
                             height='20', left='423', top='74', width='75', 
                             bgcolor=u'#F0F0F0', fgcolor=u'#000000', )
                gui.TextBox(id=169, name='textbox_528_168_625_169', 
                            height='28', left='89', top='73', width='54', 
                            text=u'1', value=u'1', )
                gui.Label(id=295, name='label_261_165_295', height='22', 
                          left='164', top='76', width='90', 
                          text=u'x Integrations', )
                gui.ComboBox(id=173, name='combobox_173', left='615', 
                             top='24', width='91', 
                             items=[u'0', u'10', u'20', u'30', u'40', u'50', u'60'], )
                gui.ComboBox(id=177, name='combobox_177', left='133', 
                             top='28', width='127', 
                             items=[u'1', u'3', u'10', u'30', u'100', u'300', u'1000', u'3000', u'10000', u'30000', u'100e3', u'300e3', u'1e6', u'2e6'], )
            with gui.Panel(id=231, label=u'Antenna Control', name='panel_231', 
                           height='116', left='22', top='668', width='753', 
                           bgcolor=u'#F0F0F0', fgcolor=u'#000000', image='', ):
                gui.Label(id=279, name='label_279', left='37', top='24', 
                          text=u'Start (Deg)', )
                gui.Label(id=309, name='label_309', left='375', top='26', 
                          text=u'Increment (Deg)', )
                gui.Label(id=183, name='label_309_183', height='22', 
                          left='37', top='77', width='73', text=u'Stop (Deg)', )
                gui.Label(id=144, name='label_309_144', height='22', 
                          left='374', top='74', width='108', 
                          text=u'Set Polarization', )
                gui.ComboBox(id=162, name='combobox_162', left='527', 
                             top='71', items=[u'Horizontal', u'Vertical'], )
                gui.TextBox(id=278, name='textbox_278', left='154', top='25', 
                            text=u'0', value=u'0', )
                gui.TextBox(id=380, name='textbox_380', left='154', top='74', 
                            text=u'360', value=u'360', )
                gui.ComboBox(id=177, name='combobox_177', left='526', 
                             top='23', 
                             items=[u'5', u'15', u'30', u'45', u'60', u'90', u'180'], )
            with gui.Panel(id=215, label=u'Mode Frequency Override', 
                           name='panel_215', height='353', left='507', 
                           top='85', width='269', bgcolor=u'#F0F0F0', 
                           fgcolor=u'#000000', image='', ):
                gui.Label(id=164, name='label_164', left='19', top='77', 
                          text=u'Freq. Start', )
                gui.Label(id=210, name='label_210', left='19', top='138', 
                          text=u'Freq. Stop', )
                gui.TextBox(id=256, name='textbox_256', left='112', top='135', 
                            width='141', text=u'3e9', 
                            value=u'3e9',  )
                gui.TextBox(id=492, name='textbox_256_492', height='28', 
                            left='110', top='73', width='141', text=u'70e6', 
                            value=u'70e6',  )
                gui.CheckBox(id=184, label=u'Override', name='checkbox_184', 
                             height='20', left='21', top='33', width='75', 
                             bgcolor=u'#F0F0F0', fgcolor=u'#000000', )
                gui.Button(id=162, label=u'No HW Mode', name='button_162', 
                           left='43', top='233', width='193', 
                           fgcolor=u'#000000', )
        with gui.TabPanel(id=147, name='tabpanel_147', selected=False, 
                          text=u'Full Manual', visible=False, ):
            with gui.Panel(id=167, label=u'Antenna Position Setup', 
                           name=u'An_pos', height='260', left='15', top='463', 
                           width='761', bgcolor=u'#F0F0F0', 
                           fgcolor=u'#000000', image='', ):
                gui.TextBox(id=244, name='textbox_244', left='135', top='126', 
                            text=u'0', value=u'0', )
                gui.TextBox(id=491, name='textbox_491', left='623', top='132', 
                            text=u'5', value=u'5', )
                gui.Label(id=715, name='label_715', left='249', top='130', 
                          text=u'Stop Pos (Deg)', )
                gui.Label(id=1007, name='label_715_1007', height='22', 
                          left='18', top='50', width='105', 
                          text=u'Activate Antenna Position Control', )
                gui.TextBox(id=1217, name='textbox_491_1217', height='28', 
                            left='365', top='129', width='100', text=u'360', 
                            value=u'360', )
                gui.Label(id=1453, name='label_715_1007_1453', height='22', 
                          left='18', top='128', width='105', 
                          text=u'Start Pos (Deg)', )
                gui.Label(id=218, name='label_218', left='17', top='181', 
                          text=u'Antenna Polarization', )
                gui.Label(id=817, name='label_715_1007_817', height='22', 
                          left='477', top='132', width='108', 
                          text=u'Increment (Deg)', )
                gui.CheckBox(id=853, label=u'On/Off', name='checkbox_853', 
                             height='20', left='281', top='48', width='75', 
                             bgcolor=u'#F0F0F0', fgcolor=u'#000000', )
                gui.ComboBox(id=160, name='combobox_160', height='28', 
                             left='184', top='183', width='145', 
                             bgcolor=u'#FFFFFF', fgcolor=u'#000000', 
                             helptext=u'Pol', 
                             items=[u'Horizontal', u'Vertical'], )
    gui.Button(id=276, name='button_276', left='129', top='284', )

# --- gui2py designer generated code ends ---


mywin = gui.get("mywin")

# assign your event handlers:

mywin['notebook']['tabpanel']['button'].onclick = init1
mywin['notebook']['tabpanel']['freq_191']['combobox_248'].onchange = show_max_time
mywin['notebook']['tabpanel_184']['panel_217']['combobox_166'].onchange = show_max_time1
mywin['notebook']['tabpanel']['freq_191']['time_ac'].onchange = check_max
mywin['notebook']['tabpanel_184']['panel_217']['textbox_528'].onchange = check_max1


## TAB: Field test events
mywin['notebook']['tabpanel_184']['panel_163']['button_538'].onclick = mode0
mywin['notebook']['tabpanel_184']['panel_163']['button_223'].onclick = mode1
mywin['notebook']['tabpanel_184']['panel_163']['button_385'].onclick = mode2
mywin['notebook']['tabpanel_184']['panel_163']['button_469'].onclick = mode3
mywin['notebook']['tabpanel_184']['panel_163']['button_413'].onclick = mode4
mywin['notebook']['tabpanel_184']['panel_163']['button_337'].onclick = mode5
mywin['notebook']['tabpanel_184']['panel_163']['button_441'].onclick = mode6
mywin['notebook']['tabpanel_184']['panel_163']['button_497'].onclick = mode7

mywin['notebook']['tabpanel_184']['panel_215']['button_162'].onclick = mode_no_ware

mywin['notebook']['tabpanel_184']['panel_217_164']['checkbox_250_146'].onclick = int_or_hold
mywin['notebook']['tabpanel_184']['panel_217_164']['checkbox_250'].onclick = int_or_hold

if __name__ == "__main__":
    mywin.show()    
    gui.main_loop()


