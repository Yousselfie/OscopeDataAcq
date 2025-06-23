import serial
import time

serialInstance = serial.Serial()
serialInstance.baudrate = 9600
serialInstance.port = "COM3"
serialInstance.open()
time.sleep(2)

serialInstance.write(("1\n").encode('utf-8'))
serialInstance.write(("--- Symbolic Execution Path ---\n").encode('utf-8'))
serialInstance.write("Inputs: {'IN0': True, 'IN1': True, 'IN2': True, 'IN3': True, 'IN4': True, 'IN5': True, 'IN6': True, 'IN7': True}\n".encode('utf-8'))
serialInstance.write("Outputs: {'Q0': False, 'Q1': False, 'Q2': False, 'Q3': True, 'Q4': True, 'Q5': True, 'Q6': False, 'Q7': True}\n".encode('utf-8'))
serialInstance.write("Timers: {'Timer0_Elapsed': True, 'Timer1_Elapsed': True, 'Timer2_Elapsed': False, 'Timer3_Elapsed': True, 'Timer4_Elapsed': False}\n".encode('utf-8'))
serialInstance.flush()
time.sleep(1)
# Read back Arduino's response (optional)
print("Arduino:")
while serialInstance.in_waiting > 0:
    print("\t", serialInstance.readline().decode('utf-8').strip())