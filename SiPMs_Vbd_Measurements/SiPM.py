## Simplest Code possible for the SiPMs, Drops the Bias voltage for -60V and measures the current.

import os
import sys
import usb.core
import serial   
import numpy as np
import matplotlib.pyplot as plt
# Import necessary packages
from pymeasure.instruments.keithley import Keithley2450
import pyvisa
import pandas as pd
import time
from pymeasure.adapters import VISAAdapter

def Derivative(x,y):
    
    dydx = np.diff(np.array(-y)) / np.diff(x)
    x = np.array(x) 
    x2 = (x[:-1] + x[1:]) / 2
    return dydx,x2 
    

def MakePlots(df, dir='', measurement='', SiPM_number=0, justIV = False):
    #df = pd.read_csv(csv_file, skiprows=0,usecols=['Current (A)', 'Voltage (V)'])  
    voltage = df.iloc[:, 0]  # the first column is Voltage
    current = df.iloc[:, 1]  # the second column is Current\

    current = np.array(current)
    der_ , x2_  = Derivative(voltage, current)
    current_ = (current[:-1] + current[1:]) / 2
    der_I = der_/current_
    max_index = np.argmax(der_I)

    # Plot the data
    # IVCurve_mmddhhmmX_ch.pdf
    plt.figure(figsize=(10, 6))
    plt.plot(voltage, current, marker='.', linestyle='--', label = measurement+str(SiPM_number))
    # plt.ylabel(r'Current ($\mu$A)')
    plt.ylabel('Current (A)')
    plt.xlabel('Reverse Voltage (V)')
    plt.title('Plot of CSV Data Oscilloscope')
    plt.legend()
    plt.grid()
    plt.savefig(dir+'IVCurve_'+measurement+'_'+str(SiPM_number)+'.pdf', dpi = 150, format = 'pdf')
    plt.close()

    if (not justIV):    
        plt.figure(figsize=(10, 6))
        plt.plot(voltage, -current, marker='.', linestyle='--', label = measurement+str(SiPM_number))
        plt.yscale('log')
        # plt.ylabel(r'Current ($\mu$A)')
        plt.ylabel('Current (A)')
        plt.xlabel('Reverse Voltage (V)')
        plt.title('Plot of CSV Data 2450 SourceMeter')
        plt.legend()
        plt.grid()
        plt.savefig(dir+'IVCurve_LogScale_'+measurement+'_'+str(SiPM_number)+'.pdf', dpi = 150, format = 'pdf')
        plt.close()


        plt.figure(figsize=(10, 6))
        # print(der_.size, x2_.size,current_.size)
        # Plot the data
        plt.figure(figsize=(10, 6))
        plt.plot(x2_, der_/current_, marker='*', linestyle='--', label = measurement+str(SiPM_number))
        plt.ylabel(r'$\frac{dI}{IdV}$', fontsize =17, rotation = 'vertical')
        #plt.xticks(np.round(np.linspace(50,60,20)))
        plt.legend()
        plt.grid(axis='x', color='lightgray', linestyle='-')
        plt.xlabel('Reverse Voltage (V)')
        plt.title('Plot of CSV Data 2450 SourceMeter')
        plt.savefig(dir+'dI_IdV_'+measurement+'_'+str(SiPM_number)+'.pdf', dpi = 150, format = 'pdf')
        plt.close()


    return x2_[max_index]

def ShutdownPowerSupply():

    dev = usb.core.find(idVendor=0x05e6,idProduct=0x2450)
    dev.reset()

    adapter = VISAAdapter("USB0::0x05e6::0x2450::04614968::INSTR")
    keithley = Keithley2450(adapter)
    keithley.reset()
    keithley.shutdown()


def VBD_Measurement(NegBiasStart = -54,NegBiasEnd = -51,data_points = 40, SaveCSV = True, dir = '', measurement_label = '', SiPM_number = 0):

    if (NegBiasStart>0 or NegBiasEnd>0):
        sys.exit("It is expected a negative Bias voltage.")

    dev = usb.core.find(idVendor=0x05e6,idProduct=0x2450)
    #e = dev[0].interfaces()[0].endpoints()[0]
    #i = dev[0].interfaces()[0].bInterfaceNumber
    dev.reset()
    #if dev.is_kernel_driver_active(i):
    #    try:
    #        dev.detach_kernel_driver(i)
    #    except usb.core.USBError as e:
    #        sys.exit("Could not detatch kernel driver from interface({0}): {1}".format(i, str(e)))


    adapter = VISAAdapter("USB0::0x05e6::0x2450::04614968::INSTR")
    keithley = Keithley2450(adapter)
    keithley.reset()
    keithley.apply_voltage()                # Sets up to source voltage
    keithley.source_voltage_range = NegBiasStart  # Sets the source voltage range to -55 V
    keithley.compliance_current = 2e-4        # Sets the compliance current to 100 mu A.
    keithley.source_voltage = NegBiasStart          # Sets the source voltage to 0 Volts.
    keithley.enable_source()                # Enables the source output
    keithley.measure_current()              # Sets up to measure voltage


    # Allocate arrays to store the measurement results
    voltage_probe = np.linspace(NegBiasStart,NegBiasEnd,data_points)
    currents = np.zeros_like(voltage_probe)
    currents_stds = np.zeros_like(voltage_probe)
    #print(currents)
    #print(currents_stds)

    for i in range(data_points):

        keithley.source_voltage = voltage_probe[i]# Ramps the current to 5 mA
        currents[i] = keithley.current  # Save current
        time.sleep(.2)
        #currents_stds[i] = keithley.std_current # Save current std

    # Save the data columns in a CSV file
    data = pd.DataFrame({
        'Voltage (V)': voltage_probe,
        'Current (A)': currents,
        #'Current Std (A)': currents_stds,
    })

    if SaveCSV:
        data.to_csv(dir+'IV_Curve_'+measurement_label+'_'+str(SiPM_number)+'.csv')

    Vbr = MakePlots(data,dir,measurement_label,SiPM_number)
    return Vbr

def RQ_Measurement(PosBiasStart = 0.,PosBiasEnd = 3,data_points = 70, SaveCSV = True, dir = '', measurement_label = '', SiPM_number = 0):
    
    if (PosBiasStart!=0 or PosBiasEnd>7):
        sys.exit("The forward Bias range is out of the boundaries for this measurement.")

    dev = usb.core.find(idVendor=0x05e6,idProduct=0x2450)
    dev.reset()

    adapter = VISAAdapter("USB0::0x05e6::0x2450::04614968::INSTR")
    keithley = Keithley2450(adapter)
    keithley.reset()
    keithley.apply_voltage()                # Sets up to source voltage
    keithley.source_voltage_range = PosBiasEnd  # Sets the source voltage range to PosBiasEnd
    keithley.compliance_current = 1e-2        # Sets the compliance current to 100 mu A.
    keithley.source_voltage = PosBiasStart          # Sets the source voltage to 0 Volts.
    keithley.enable_source()                # Enables the source output
    keithley.measure_current()              # Sets up to measure voltage


    # Allocate arrays to store the measurement results
    voltage_probe = np.linspace(PosBiasStart,PosBiasEnd,data_points)
    currents = np.zeros_like(voltage_probe)
    currents_stds = np.zeros_like(voltage_probe)
    #print(currents)
    #print(currents_stds)

    for i in range(data_points):

        keithley.source_voltage = voltage_probe[i]# Ramps the current to 5 mA
        currents[i] = keithley.current  # Save current
        time.sleep(.2)
        #currents_stds[i] = keithley.std_current # Save current std

    # Save the data columns in a CSV file
    data = pd.DataFrame({
        'Voltage (V)': voltage_probe,
        'Current (A)': currents,
        #'Current Std (A)': currents_stds,
    })

    if SaveCSV:
        data.to_csv(dir+'IV_Curve_'+measurement_label+'_'+str(SiPM_number)+'.csv')

    Rq = MakePlots(data,dir,measurement_label,SiPM_number, justIV = True)
    return Rq
