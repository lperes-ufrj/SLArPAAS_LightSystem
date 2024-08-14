import smbus
import time
import datetime
import numpy as np 
import SiPM
import os
import argparse


# Initialize I2C bus
bus = smbus.SMBus(1)

# I2C address of the relay board
boards_address = np.array([0x25,0x27])
SiPMs_channels = [[2,1,0],[7,6,5,2,1,0]]

def options():

    parser = argparse.ArgumentParser(usage=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-n", "--name",
                        default="X",
                        help="name of the SiPM sets (A-E)")
    parser.add_argument("-c", "--condition",
                        default="non-specified",
                        help="conditions (room, before, cold)")
    parser.add_argument("-m", "--measurement",
                        default="non-specified",
                        help="measurement (vbd, rq, both)")
    return parser.parse_args()


def select_relay(board_address,channel):
    bus.write_byte(board_address, ~(0x01 << (channel )))


def turn_off_relaychs():
    select_relay(0x27,9) # Turn off all relay channels in the board)
    select_relay(0x25,9) # Turn off all relay channels in the board 


def my_makedirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)


ops = options()
SiPM_set_name = ops.name
condition_name = ops.condition
measurement_name = ops.measurement

print("SiPM set name (-n) =", SiPM_set_name)
print("condition (-c) =", condition_name)
print("measurement (-m) =", measurement_name)

dt_now = datetime.datetime.now()
dirname = 'data/'+dt_now.strftime('%m%d%H%M')+SiPM_set_name+'_'+condition_name+'/'
filename = measurement_name+dt_now.strftime('%m%d%H%M')+SiPM_set_name+condition_name+'.csv'
measurement_label = measurement_name+'_'+dt_now.strftime('%m%d%H%M')+SiPM_set_name+'_'+condition_name

my_makedirs(dirname)
output_file = open(dirname+filename,"a")

try:
    for i_board, board_address in enumerate(boards_address):

        turn_off_relaychs()

        for i_ch in SiPMs_channels[i_board]:
            select_relay(board_address,i_ch)

            if(board_address == 0x25):
                SiPM_number = 3-i_ch # i_ch = 2, 1, 0 -> SiPM_number = 1, 2, 3
            else: # board_address == 0x27
                if(i_ch>3):
                    SiPM_number = 11-i_ch # i_ch = 7, 6, 5 -> SiPM_number = 4, 5, 6
                else:
                    SiPM_number = 9-i_ch # i_ch = 2, 1, 0 -> SiPM_number = 7, 8, 9
            
            if measurement_name == 'vbd':
                Vbr = SiPM.VBD_Measurement(dir=dirname, measurement_label=measurement_label, SiPM_number=SiPM_number)
            if measurement_name == 'rq':
                Rq = SiPM.RQ_Measurement(dir=dirname, measurement_label=measurement_label, SiPM_number=SiPM_number)
            if measurement_name == 'both':
                Vbr = SiPM.VBD_Measurement(dir=dirname, measurement_label=measurement_label+'_vbd', SiPM_number=SiPM_number)
                time.sleep(1.)
                Rq = SiPM.RQ_Measurement(dir=dirname, measurement_label=measurement_label+'_rq', SiPM_number=SiPM_number)

            time.sleep(.5)

            line = dt_now.strftime('%m%d%H%M')+'_'+SiPM_set_name+'_'+str(SiPM_number)+", "+str(Vbr)
            output_file.write(line+'\n')
            print(SiPM_number, "Vbr =", round(Vbr,2))

except KeyboardInterrupt:
    output_file.close()
    turn_off_relaychs()
    SiPM.ShutdownPowerSupply()

output_file.close()
turn_off_relaychs()
SiPM.ShutdownPowerSupply()
