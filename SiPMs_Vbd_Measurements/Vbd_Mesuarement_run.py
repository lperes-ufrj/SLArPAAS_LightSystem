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
SiPMs_channels = [[2,1,0],[7,6,5,4,3,2]]

def options():

    parser = argparse.ArgumentParser(usage=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-n",
                        default="X",
                        help="name of the SiPM sets (A-E)")
    return parser.parse_args()


def select_relay(board_address,channel):
    bus.write_byte(board_address, ~(0x01 << (channel )))


def my_makedirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)

ops = options()
SiPM_set_name = ops.n

dt_now = datetime.datetime.now()
dirname = 'data/'+dt_now.strftime('%m%d%H%M')+SiPM_set_name+'/'
filename = dt_now.strftime('%m%d%H%M')+SiPM_set_name+'.csv'

my_makedirs(dirname)
output_file = open(dirname+filename,"a")

try:
    for i_board, board_address in enumerate(boards_address):
        select_relay(0x27,9) # Turn off all relay channels in the board)
        select_relay(0x25,9) # Turn off all relay channels in the board 
        for i_ch in SiPMs_channels[i_board]:
            select_relay(board_address,i_ch)
            # print(i_board,i_ch) 
            Vbr = SiPM.VBD_Measurement(label_sipm=str(i_ch)+'_'+str(i_board), dir=dirname)
            time.sleep(1.)

            if(board_address == 0x25):
                SiPM_number = 3-i_ch # i_ch = 2, 1, 0 -> SiPM_number = 1, 2, 3
            else: # board_address == 0x27
                SiPM_number = 11-i_ch # i_ch = 7, 6, 5, 4, 3, 2 -> SiPM_number = 4, 5, 6, 7, 8, 9
            line = dt_now.strftime('%m%d%H%M')+'_'+SiPM_set_name+str(SiPM_number)+", "+str(Vbr)
            output_file.write(line+'\n')

except KeyboardInterrupt:
    output_file.close()
    select_relay(boards_address[1],9) # Turn off all channels 

output_file.close()
select_relay(boards_address[1],9) # Turn off all channels 
