import serial, platform, glob

X = 0
Y = 0
Z = 0

# A function that tries to list serial ports on most common platforms
def list_serial_ports():
    system_name = platform.system()
    if system_name == "Windows":
        # Scan for available ports.
        available = []
        for i in range(256):
            try:
                s = serial.Serial(i)
                available.append(i)
                s.close()
            except serial.SerialException:
                pass
        return available
    elif system_name == "Darwin":
        # Mac
        return glob.glob('/dev/tty*') + glob.glob('/dev/cu*')
    else:
        # Assume Linux or something else
        return glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')
	
port = list_serial_ports()
print (port)
number = input("Which port? ")
arduino = serial.Serial(port[number-1], 115200, timeout = 0.01)
    
def getSerial():
    global X
    data = arduino.readline()[:-2] #the last bit gets rid of the new-line chars
    try:
	if data[5] == "X" :
	    X = int( data[9:] )
	'''
	if data[5] == "Y" :
	    Y = int( data[9:] )
	if data[5] == "Z" :
	    Z = int( data[9:] )
	'''
    except:
        pass
	
    #print X,Y,Z
    
    return X
    
