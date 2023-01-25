import serial
import operator
from time import sleep
port = serial.Serial()
port.baudrate = 9600
port.port = 'COM3'
port.bytesize = 8
port.open()
print("Please insert an RFID card")
data = ['0']
while True:
    ID = ""
    read_byte = port.read()
    if read_byte == b'\x02':
        while read_byte != b'\x03':
            read_byte = port.read(1)
            ID = ID + read_byte.decode()
    checksum = hex(int(ID[10:-1].encode('utf-8').decode(), 16))
    csm1 = int(ID[2:-9].encode('utf-8').decode(), 16)
    csm2 = int(ID[4:-7].encode('utf-8').decode(), 16)
    csm3 = int(ID[6:-5].encode('utf-8').decode(), 16)
    csm4 = int(ID[:-11].encode('utf-8').decode(), 16)
    csm5 = int(ID[8:-3].encode('utf-8').decode(), 16)
    r1 = operator.xor(csm1, csm2)
    r2 = operator.xor(csm3, csm4)
    r3 = operator.xor(r1, r2)
    r4 = operator.xor(r3, csm5)
    result = hex(r4)
    ID = ID[2:-3].encode('utf-8').decode()
    ID = int(ID, 16)
    if result == checksum:
        if data[0] == ID:
            sleep(5)
            data.clear()
            data.append("")
        else:
            data.clear()
            data.append(ID)
            print("ID:", ID)
    else:
        print("error")
