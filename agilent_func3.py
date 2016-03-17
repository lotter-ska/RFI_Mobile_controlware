import visa
import time
import numpy as np
import matplotlib.pyplot as plt

from threading import Thread
import thread
import math

def agilent(my_instrument,centre_freq, span,ref, att, r_bw, max_hold, max_hold_time, avg, avg_times, base_file,gain,cal):



    ##Write setup info to file
    info_to_file = """Centre Freq: %(centre_freq)s Hz
Span: %(span)s Hz
Res BW: %(r_bw)s Hz
Ref Level: %(ref)s dBm
Attenuation: %(att)s dB
Averaging: %(avg_times)s times
Max Hold: %(max_hold_time)s seconds
    
    \n""" % {'centre_freq': centre_freq, 'span': span, 'r_bw': r_bw, 'ref': ref, 'att': att, 'avg_times': avg_times, 'max_hold_time': max_hold_time}

    f_handle = file(base_file, 'a')
    f_handle.write(info_to_file)
    f_handle.write('\n')


    ##check if avg and max hold selected: choose avg!
    if (avg==True and max_hold==True):
        max_hold=False

    
##Break range into chunks not wider than RBW
    gates=float(span)/float(r_bw)
##    print gates
    runs=gates/601
##    print runs
    fsto_fin=centre_freq+span/2
    fsta=centre_freq-span/2
    fsto=fsta+float(r_bw)*601
    f_all=[]
    dat_all=[]
    

########################################START OF FOR LOOP#################################################
    
    for i in range(0,int(math.ceil(runs))):
        print fsta
        print fsto
        span=fsto-fsta
        centre_freq=fsta+span/2
        ##Setup Instrument
        command = 'IP;CF %(centre_freq)s;SP %(span)s;RB %(r_bw)s;AT %(att)s;RL %(ref)s' %{'centre_freq':centre_freq, 'span':span, 'att':att, 'r_bw':r_bw, 'ref':ref}
        my_instrument.write(command) 
        sweep_time=my_instrument.query('ST?')

        ##Use max hold
        if max_hold==1:
            my_instrument.write('MXMH TRA')
            sleep_time=(float(max_hold_time)-1.0)*float(sweep_time)
            time.sleep(sleep_time)
            my_instrument.write('SNGLS;TS')     #single sweep
            time.sleep(float(sweep_time))
            my_instrument.write('TDF P;TRA?')   #request data
            a=my_instrument.read()
            dat_to_file=np.fromstring(a, dtype=float, sep=",")
           

        ##Use Avging
        elif avg==1:
        ##    dat_cal=np.zeros((1, 601))
            dat_cal=0
            for x in range(0, int(avg_times)):
                my_instrument.write('SNGLS;TS')     #single sweep
                time.sleep(float(sweep_time))
                ##write data to GPIB - one line 601 values
                my_instrument.write('TDF P;TRA?')
                a=my_instrument.read()
                dat = np.fromstring(a, dtype=float, sep=",")
                dat_cal=dat+dat_cal

            dat_to_file=dat_cal/int(avg_times)
            

        ## Run without agv or max hold
        else:
            my_instrument.write('SNGLS;TS')     #single sweep
            my_instrument.write('TDF P;TRA?')   #request data
            a=my_instrument.read()
            dat_to_file=np.fromstring(a, dtype=float, sep=",")

        ## update freq start and stop
        fsta=fsto+float(r_bw)
        fsto=fsta+float(r_bw)*601
        if i==int(math.ceil(runs))-2:  ##check if last run, if so change f stop to end for mode
            print "laaste"
            fsto=fsto_fin
                
        f=np.linspace(centre_freq-span/2,centre_freq+span/2,601)
        f_all=np.append(f_all,f)
        dat_all=np.append(dat_all,dat_to_file)
###########################END OF FOR LOOP##############################################

    DATA=np.vstack((f_all,dat_all)).T
    np.savetxt(f_handle, DATA, delimiter=",")

    f_handle.write('\n')
    f_handle.close()
    f=np.linspace(centre_freq-span/2,centre_freq+span/2,601)
    plt.plot(f_all,dat_all)
    plt.ylabel('dBm')
    plt.xlabel('Frequency [Hz]')
    plt.title('Spectrum from previous measurement')
    plt.grid()
    plt.show()
    ########################################END OF FUNCTION###############################

def wait_fun(tot_time):
    import gui
    import time
    with gui.Window(name='wait',title=u'Please Wait', resizable=True, 
                height='50px', left='60', top='60', width='100px', 
                bgcolor=u'#ABABAB', fgcolor=u'#000000', image='', ) as win:
            gui.Label(name='prog',text=tot_time)

    wait = gui.get("wait")
    wait.show()
    t=float(tot_time)
    if t<1:
        t=1
    print t
    while t>-1:
        if t<0:
            t=0
        
        time_str='%d seconds remaining' %t
        wait['prog'].text=time_str
        time.sleep(1)
        t-=1

    wait.close()


##def time_calc()
