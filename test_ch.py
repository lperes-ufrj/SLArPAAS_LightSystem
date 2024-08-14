import smbus
import time
import datetime
import numpy as np 
import os
import argparse

# Initialize I2C bus
bus = smbus.SMBus(1)

# I2C address of the relay board
boards_address = np.array([0x25,0x27])
SiPMs_channels = [[2,1,0],[7,6,5,4,3,2]]

def options():

    parser = argparse.ArgumentParser(usage=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-c", "--channel",
                        default=-1,
                        help="channel (1-9)")
    parser.add_argument("-b", "--board",
                        default=0xFF,
                        help="board (0x25/0x27)")
    parser.add_argument("-r", "--relay",
                        default=-1,
                        help="relay channel (0-7)")
    return parser.parse_args()


def select_relay(board_address,channel):
    bus.write_byte(board_address, ~(0x01 << (channel )))



ops = options()
ch = int(ops.channel)
board_address = ops.board
relay_channel = int(ops.relay)

if(ch<1 or ch>9):
    select_relay(0x25, 9)
    select_relay(0x27, 9)

if(board_address != 0x25 & board_address != 0x27):
    if(ch > 0 & ch < 4):
        select_relay(0x25, 3-ch)
    elif(ch > 0 & ch < 8):
        select_relay(0x27, 11-ch)
    elif(ch > 0 & ch < 10):
        select_relay(0x27, 10-ch)

if(board_address == 0x25 | board_address == 0x27):
    select_relay(board_address, relay_channel)



