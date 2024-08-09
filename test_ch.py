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


def select_relay(board_address,channel):
    bus.write_byte(board_address, ~(0x01 << (channel )))


select_relay(0x27,2)