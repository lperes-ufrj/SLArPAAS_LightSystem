import smbus
import time
import numpy as np 
import SiPM


# Initialize I2C bus
bus = smbus.SMBus(1)

# I2C address of the relay board
boards_address = np.array([0x25,0x27])
SiPMs_channels = [[2,1,0],[7,6,5,4,3,2]]

def select_relay(board_address,channel):
        bus.write_byte(board_address, ~(0x01 << (channel )))

for i_board, board_address in enumerate(boards_address):
   select_relay(0x27,9) # Turn off all relay channels in the board)
   select_relay(0x25,9) # Turn off all relay channels in the board 
   for i_ch in SiPMs_channels[i_board]:
      select_relay(board_address,i_ch)
      #print(i_board,i_ch) 
      SiPM.VBD_Measurement(label_sipm=str(i_ch)+'_'+str(i_board))
      time.sleep(1.)
select_relay(boards_address[1],9) # Turn off all channels 
