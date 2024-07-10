## Simplest Code possible for the SiPMs, Drops the Bias voltage for -60V and measures the current.

import os
import serial   
import numpy as np
import matplotlib.pyplot as plt
# Import necessary packages
from pymeasure.instruments.keithley import Keithley2450
import pyvisa
import pandas as pd
from time import sleep

from pymeasure.adapters import VISAAdapter

adapter = VISAAdapter("USB0::0x05e6::0x2450::04614968::INSTR")
keithley = Keithley2450(adapter)

keithley.apply_voltage()                # Sets up to source voltage
keithley.source_voltage_range = -55  # Sets the source voltage range to -55 V
keithley.compliance_current = 1e-4        # Sets the compliance current to 100 mu A.
keithley.source_voltage = 0             # Sets the source voltage to 0 Volts.
keithley.enable_source()                # Enables the source output

keithley.measure_current()              # Sets up to measure voltage

keithley.ramp_to_voltage(-60)           # Ramps the voltage to -60V.
sleep(2.0)
print(keithley.current)                 # Prints the voltage in Volts
keithley.shutdown()                     # Ramps the current to 0 mA and disables output