# Lookup environment variable OSCOPE_IP and use it as the resource
# name or use the TCPIP0 string if the environment variable does
# not exist
from oscope_scpi import Oscilloscope
from os import environ
resource = environ.get('OSCOPE_IP', 'USB0::10893::6006::MY58262555::0::INSTR')

# create your visa instrument
instr = Oscilloscope(resource)

# Upgrade Object to best match based on IDN string
instr = instr.getBestClass()

# Open connection to instrument
instr.open()


instr.waveform(points=300, filename='test.csv')

# set to channel 1
#
# NOTE: can pass channel to each method or just set it
# once and it becomes the default for all following calls. If pass the
# channel to a Class method call, it will become the default for
# following method calls.
instr.channel = '1'

# Enable output of channel, if it is not already enabled
if not instr.isOutputOn():
    instr.outputOn()



# Install measurements to display in statistics display and also
# return their current values here
print('Ch. {} Settings: {:6.4e} V  PW {:6.4e} s\n'.
          format(instr.channel, instr.measureVoltAverage(install=True),
                     instr.measurePosPulseWidth(install=True)))

# Add an annotation to the screen before hardcopy
instr.annotate("{} {} {}".format('Example of Annotation','for Channel',instr.channel), 'ch1')


# Change label of the channel to "MySig1"
instr.channelLabel('MySig1')

# Make sure the statistics display is showing for the hardcopy
instr.measureStatistics()

# STOP Oscilloscope (not required for hardcopy - only showing example of how to do it)
instr.modeStop()

# Save a hardcopy of the screen to file 'outfile.png'
instr.hardcopy('outfile.png')

# SINGLE mode (just an example)
instr.modeSingle()

# Change label back to the default
#
# NOTE: can use instr.channelLabelOff() but showing an example of sending a SCPI command directly
instr._instWrite('DISPlay:LABel OFF')

# RUN mode (since demo Stop and Single, restore Run mode)
instr.modeRun()

# Turn off the annotation
instr.annotateOff()
    
# turn off the channel
instr.outputOff()

# return to LOCAL mode
instr.setLocal()

instr.close()