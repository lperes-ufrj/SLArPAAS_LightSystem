<!-- GETTING STARTED -->
## SLArPAAS Light Detection System Repository

This is repository contains data collected and codes used from the first stage of R&D for the SLArPAAS Light Detection System. All the data in this repository were taken with an oscilloscope. Below, one can find a description of each folder.

---
### ./FirstsPlotsLogs

Jupyter Notebooks of the firsts measurements with one SiPM, includes some data taking with the scope with the nEXO preAmplifier and OpAmp. Also, first Breakdown voltage measument of the SiPM. 

### ./FirstSiPM_ScopeData

Data took with the Scope used in the jupyter notebooks above.

---
### PreAmplifiers Data

These folder have the early R&D for the Pre Amplifier board. All data collected in the folders listed below were took with one SiPM.

#### ./OpAmpMeasurements

Data collected with the PreAmplifier prototype later used in the final design of the 9-channels Pre Amplifier board. 

#### ./2chMeasurements

Data collected with a first 2-channel prototype.

#### ./nEXOMeasurements

Data collected with the nEXO preAmplifier Board.

---
### ./SiPMs_Vbd_Measurements

Folder with data and codes regarding the breakdown voltage and queenching resistor of the SiPMs.

#### ./SiPMs_Vbd_Measurements/data

All the data collected 
1. 84_Before : Data taking in the fridge, but before cooling down, roughly at room temperature ~300K.
2. Cold : Data taking at 80K.
3. IR2_Measurements: First data taking at IR2 building, saved for consistency. 

#### ./SiPMs_Vbd_Measurements/Measurement_run.py

Interface code for the relay channels, for loop in each relay channel and to call the functions to take data with Reverse Voltage and Forward Voltage.

#### ./SiPMs_Vbd_Measurements/Plot_Vbd_Rq.ipynb

Jupyter notebook with the final plots of the measurements.

#### ./SiPMs_Vbd_Measurements/SiPM.py

Small python library to be called at Measurement_run.py for the interface with Keithley 2450 Power Supply.

#### ./SiPMs_Vbd_Measurements/SiPMsMeasurements_Cold.py

Data sheet with the measurements in the cold.

#### ./SiPMs_Vbd_Measurements/SiPMsMeasurements_Room.py

Data sheet with the measurements at room temperature.

---

### RTDs_ColdTest

Non-related to light detection system, RTDs measurements at LN temperature for tests.

---

### PowerSupplyBias_ModbusController

First attempt to connect the Keithley 2450 Power Supply at the Ignition with ModBus. This is an attempt to combine the codes in ./SiPMs_Vbd_Measurements/SiPM.py with the ones used in the CAEN High Voltage Supply.

---