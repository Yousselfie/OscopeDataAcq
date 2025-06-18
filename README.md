# Oscilloscope Data Acquisition
Programs related to the gathering of EM (electromagnetic) wave data from the processing unit of a PLC (programmable logic controller) as it runs various control logic.

## Use of Arduino
In order to capture the EM data of a specific control logic, it must be running on the controller. Normally, this would mean connecting the PLC to the PC, downloading the control logic to the PLC, then running it. This becomes a tedious process when there are many possible symbolic paths of specific control logic for the PLC to run and for data to be collected from. To make this process more efficient, we make use of a microcontroller (Arduino) to automatically modify the inputs of a PLC to simulate new control logic. Given all the symbolic execution paths in a control logic, the Arduino will set and unset inputs on the PLC to match each one for a set amount of time before the next path is simulated. This allows for continous data collection using the oscilloscope.  
## Project Directories
**./ControlPLC** - Contains code relating to writing/reading to the Arduino controlling the PLC inputs and accessing the PLC outputs.
**./ControlPLC/src** - Contains the source code and pseudocode for the main cpp file uploaded into the microcontroller. This code defines how the Arduino communicates with and interprets data from the local machine (Python controller).  
**./ControlPLC/python_controllers** - Contains multiple different Python programs that each establish communication with the Arduino, send data to be parsed, and ultimately determine PLC I/O from the Arduino. Each of these has been used for a different testing purpose (such as turning on all the PLC inputs or running through all symbolic paths of a sample program and turning on/off inputs based on each path).  

**./SignalProcessing** - 

