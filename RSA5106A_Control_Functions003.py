
"""     AUTHOR: Braam Otto   L%tter Kock           """
"""     MESA Solutions (Pty) Ltd. and SKA SA"""
"""     WEB: http://www.mesasolutions.co.za/       """
"""     CONTACT: braam@mesasolutions.co.za         """

import visa as vs
import numpy as np
import time
import serial
import serial.tools.list_ports
import gui
import agilent_func as agi

def GPIB_Init(resource_name):
    GPIB_Found = False
    RSA = None
    IDN_company = None
    IDN_model = None
    IDN_serial = None
    IDN_firmware = None
    RSA_OPT = None       
    for a in range(0,np.shape(vs.get_instruments_list(True))[0]):
        if vs.get_instruments_list(True)[a] == resource_name:
            GPIB_Found = True
            RSA = vs.instrument(resource_name)    
            RSA_IDN = vs.instrument(resource_name).ask('*idn?')
            [IDN_company, IDN_model, IDN_serial, IDN_firmware]=RSA_IDN.split(',')
            RSA_OPT = vs.instrument(resource_name).ask('*opt?')
            RSA.write('*rst') # reset instrument to start from known state                            
    return GPIB_Found, RSA, IDN_company, IDN_model, IDN_serial, IDN_firmware, RSA_OPT

def GPIB_SetFreq(centre_freq, span, RSA):
    while RSA.ask('*OPC?') != '1':
        time.sleep(0.5) # delays for 5 seconds
        print 'FREQ SET SLEEPING...'
    else:
        print 'FREQ SET DELAY DONE'
    RSA.timeout=500
    RSA.write('abort') # stop acquisitions while measurement is configured    
    RSA.write('spectrum:frequency:center %e' % centre_freq) 
    RSA.write('spectrum:frequency:span %e' % span)
    while RSA.ask('*OPC?') != '1':
        time.sleep(0.5) # delays for 5 seconds
        print 'FREQ SET SLEEPING...'
    else:
        print 'FREQ SET DELAY DONE'
    RSA.timeout=500
    RSA.write('CALCulate:MARKer1:DELete')
    RSA.write('calculate:marker1:add')
    RSA.write('calculate:spectrum:marker0:x %e' % centre_freq)
    print centre_freq

def GPIB_SetAcq(ref, att, acq_time, acq_bw, samples, RSA, preamp):
    print 'About to SET ACQ PARAMS...'
    while RSA.ask('*OPC?') != '1':
        time.sleep(0.5) # delays for 5 seconds
        print 'ACQ SET SLEEPING...'
    else:
        print 'ACQ SET DELAY DONE'            
    RSA.timeout=1000
    RSA.write('SENSe:ACQuisition:MODE SAMPles')         
    RSA.timeout=1000    
    RSA.write('SENSe:ANALysis:LENGth:AUTO 0')
    RSA.timeout=1000
    print 'AUTO OFF...'
    print 'ACQ BW SET TO ', acq_bw    
    RSA.write('SENSE:ACQUISITION:BANDWIDTH %i' %acq_bw)
    RSA.timeout=1000  
    print 'SENSe:ACQUISITION:SAMPLES %i' %samples
    RSA.write('SENSe:ACQUISITION:SAMPLES %i' %samples)        
    RSA.write('SENSe:ANALysis:LENGth %i s' %acq_time)
    RSA.timeout=1000    
    RSA.write('INP:ATT:AUTO OFF')
    RSA.timeout=1000
    RSA.write('INP:ATT:MON:STAT OFF')
    RSA.timeout = 1000
    while RSA.ask('*OPC?') != '1':
        time.sleep(0.5) # delays for 5 seconds
        print 'ACQ SET SLEEPING...'
    else:
        print 'ACQ SET DELAY DONE'     
    RSA.timeout=1000    
    RSA.write('INP:ATT %i' %np.int(att))       
    RSA.timeout=1000
    if preamp==True:
        print "PRE-AMPLIFIER SELECTED>>>"
        RSA.write('INPUT:RF:GAIN:STATE ON')
    else:
        print "PRE-AMPLIFIER NOT SELECTED>>>"
        RSA.write('INPUT:RF:GAIN:STATE OFF')
    
    RSA.timeout=1000
    print "SETTING REFERENCE LEVEL>>>"
    RSA.write('INPUT:RLEVEL %i' %np.int(ref))
    
    RSA.timeout=1000
    RSA.write('INITiate:IMMediate')
    RSA.timeout=1000
    RSA.write('SENSe:USETtings')
    RSA.timeout=1000                   

def GPIB_Acquire(RSA, centre_freq, span, acq_time, total_count, acq_bw, base_filename):
    RSA.write('initiate:CONtinuous OFF') # start acquisitions
    while RSA.ask('*OPC?') != '1':
        time.sleep(0.5) # delays for 5 seconds
        print 'ACQ SLEEPING...'
    else:
        print 'ACQ DELAY DONE'
        
    RSA.write('FETCh:SPECtrum:TRACe1?') 
    RSA.timout=500           
    data = RSA.read_values(vs.single)        
    
    while RSA.ask('*OPC?') != '1':
        time.sleep(0.5) # delays for 5 seconds
        print 'TRACE SLEEPING...'
    else:
        print 'TRACE DELAY DONE'
        
    if RSA.ask('*opc?') == '1': # query to check if acquisitions started
        print 'Acquisition Started...'
    else:
        print 'Error: Acquisition NOT started...'
        
    RSA.write('INITiate:IMMediate')
    RSA.write('[SENSe]:IQVTime:CLEar:RESults')
    RSA.timeout=500
    RSA.write('FETCh:IQVTime:RESult?')
    
    while RSA.ask('*OPC?') != '1':
        time.sleep(0.5) # delays for 5 seconds
        print 'TRACE SLEEPING...'
    else:
        print 'TRACE DELAY DONE'
        
    RSA.write('MMEMORY:STORE:IQ "Z:\\'+base_filename+np.str(total_count)+'.tiq"')
  
    
    while RSA.ask('*OPC?') != '1':
        time.sleep(0.5) # delays for 5 seconds
        print 'IQ FILE TRANSFER SLEEPING...'
    else:
        print 'IQ FILE TRANSFER DELAY DONE'
        
    freq=np.linspace(centre_freq-acq_bw/2,centre_freq+acq_bw/2,len(data))
    
    
    return freq, data        








