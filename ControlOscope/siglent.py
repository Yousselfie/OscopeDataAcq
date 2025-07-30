import pyvisa

rm = pyvisa.ResourceManager('@py')
print(rm.list_resources())

#my_instrument = rm.open_resource('ASRL/dev/ttyS4')
#print(my_instrument)
