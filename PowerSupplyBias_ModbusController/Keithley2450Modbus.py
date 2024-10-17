#from CAENDesktopHighVoltagePowerSupply import CAENDesktopHighVoltagePowerSupply
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server import StartTcpServer
import threading
import time

import sys
import usb.core
import numpy as np
import matplotlib.pyplot as plt

# Import necessary packages
from pymeasure.instruments.keithley import Keithley2450
import time
from pymeasure.adapters import VISAAdapter



address = ('0.0.0.0', '5020')  # to use local loopback interface: 127.0.0.1
ch_num = 1
n_hr = 4*ch_num + 1    # set current, set voltage, set ramp speed up and down
n_ir = 5*ch_num + 1    # reading voltage and current and channel status 
n_coil = ch_num + 1   # set on/off status


def server_thread(context, address):
    StartTcpServer(context = context, address = address)
    
def start_server_thread(context, address):

    t = threading.Thread(target = server_thread, args = (context, address), daemon = True)
    t.start()
    return t

def setup_context():
    store = ModbusSlaveContext (
        co = ModbusSequentialDataBlock(0, [0]*n_coil),
        hr = ModbusSequentialDataBlock(0, [0]*n_hr),
        ir = ModbusSequentialDataBlock(0, [0]*n_ir)
    )
    context = ModbusServerContext(slaves = store, single = True)
    return context



#address = ('0.0.0.0', '5020')  # to use local loopback interface: 127.0.0.1
#ch_num = 4
#n_hr = 4*ch_num + 1    # set current, set voltage, set ramp speed up and down
#n_ir = 5*ch_num + 1    # reading voltage and current and channel status and polarity and monitoring filter voltage
#n_coil = ch_num + 1   # set on/off status
#
#def setup_context():
#    store = ModbusSlaveContext (
#        co = ModbusSequentialDataBlock(0, [0]*n_coil),
#        hr = ModbusSequentialDataBlock(0, [0]*n_hr),
#        ir = ModbusSequentialDataBlock(0, [0]*n_ir)
#    )
#    context = ModbusServerContext(slaves = store, single = True)
#    return context
#    
#def server_thread(context, address):
#    StartTcpServer(context = context, address = address)
#    
#def start_server_thread(context, address):
#
#    t = threading.Thread(target = server_thread, args = (context, address), daemon = True)
#    t.start()
#    return t
    
if __name__ == '__main__':
    
    
    # connecting to power supply
    dev = usb.core.find(idVendor=0x05e6,idProduct=0x2450)
    dev.reset()

    adapter = VISAAdapter("USB0::0x05e6::0x2450::04614968::INSTR")
    keithley = Keithley2450(adapter)
    keithley.reset() 
    
    #print("connected with: ", idn)
    
    # setting up modbus server
    context = setup_context()
    start_server_thread(context, address)
    
    # fc as hex for each register type
    fx_co = 5
    fx_hr = 3
    fx_ir = 4
    
    # setting intial current limit as 100 microamps and ramp voltage (up and down) as 5 V/s for all channels
    current_initial = context[0].getValues(fx_hr, ch_num, ch_num)
    current_initial = [cur + 100*100 for cur in current_initial]
    ramp_initial = context[0].getValues(fx_hr, 2*ch_num, 2*ch_num)
    ramp_initial = [ramp + 50 for ramp in ramp_initial]
    initial = current_initial + ramp_initial
    context[0].setValues(fx_hr, ch_num, initial)
    
    while True:
        # setting on/off status
        on_value = context[0].getValues(fx_co, 0, ch_num)
        for i in range(0, ch_num):
            if on_value[i] == 1: 
                keithley.reset()
                keithley.apply_voltage() # Sets up to source voltage
            else:
                keithley.shutdown()
                
        # reading voltage and current and channel status and polarity and filter voltage
        volt_value = context[0].getValues(fx_ir, 0, ch_num)
        current_value = context[0].getValues(fx_ir, ch_num, ch_num)
        ch_status = context[0].getValues(fx_ir, 2*ch_num, ch_num)
        polarity = context[0].getValues(fx_ir, 3*ch_num, ch_num)
        filter_volt = context[0].getValues(fx_ir, 4*ch_num, ch_num)
                
        for i in range(0, ch_num):
            #channel = caen.channels[i]
           
            
            # reading voltage
            voltage_string = str(keithley.voltage)  # power supply gives results with a semicolon at the end
            voltage_clean = ""
            for ch in voltage_string:        
                if ch.isnumeric() or ch == '.':
                    voltage_clean += ch
            volt_value[i] = int(float(keithley.voltage)*10)
            
            # reading current
            current_value[i] = int(keithley.current*1e8)
        
                
            # reading filter out put voltage from voltneter
            # voltmeter_val = (ads.read_adc(i)*(4.096/32767) - zero_error_fixing)
            # filter_volt[i] = int(voltmeter_val*((100*(10**3+10**6))/(100*(10**3)))*10) # high voltage filter in units of 0.1 V - V_out(voltage divider) = (R2/(R1+R2))*V_in and we are looking for V_in
            # filter_volt[i] = voltmeter_val*(((10**5+10**6))/(100*(10**3))) # low voltage filter  
            # print(voltmeter_val)
            
        read_values = volt_value + current_value   # combining all the read values
        context[0].setValues(fx_ir, 0, read_values) # updating registers
        
        # setting voltage, current limit, ramp speed
        volt_set = context[0].getValues(fx_hr, 0, ch_num)
        current_lim = context[0].getValues(fx_hr, ch_num, ch_num)
        ramp_speed_up = context[0].getValues(fx_hr, 2*ch_num, ch_num)
        ramp_speed_down = context[0].getValues(fx_hr, 3*ch_num, ch_num)
        
        for i in range(0, ch_num):
            
            # setting voltage
            vset_string = keithley.apply_voltage()
            vset_clean = ""
            for ch in vset_string:
                if ch.isnumeric() or ch == '.':
                    vset_clean += ch
            vset_val = int(float(vset_clean)*10)
            if int(volt_set[i]) != vset_val:
                channel.V_set = float(volt_set[i]/10)
                
            # setting current limit
            iset_string = channel.get('ISET')
            iset_clean = ""
            for ch in iset_string:
                if ch.isnumeric() or ch == '.':
                    iset_clean += ch
            iset_val = int(float(iset_clean)*100)
            if current_lim[i] != iset_val:
                channel.current_compliance = current_lim[i]/100
                
            # setting ramp up voltage    
            rv_string = channel.get('RUP')
            rv_clean = ""
            for ch in rv_string:
                if ch.isnumeric() or ch == '.':
                    rv_clean += ch
            rv_val = int(float(rv_clean)*10)
            if ramp_speed_up[i] != rv_val:
                channel.set('RUP', ramp_speed_up[i]/10)
                
                
            # setting ramp down voltage    
            rvd_string = channel.get('RDW')
            rvd_clean = ""
            for ch in rvd_string:
                if ch.isnumeric() or ch == '.':
                    rvd_clean += ch
            rvd_val = int(float(rvd_clean)*10)
            if ramp_speed_down[i] != rvd_val:
                channel.set('RDW', ramp_speed_down[i]/10)
                
        time.sleep(1)
        
        
    print(keithley.current)  # Save current
    time.sleep(1)

