import RingBuffer as rb

import serial
import time
import io

class Im920s:

    crlf:str = '\r\n'

    def __init__(self, port:str, baudrate:int):
        self.last_send_time = time.time()
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = baudrate
        self.ser.timeout = 0.1
        self.serial_open()
        self.buf = rb.RingBuffer(64)

    def serial_open(self):
        try:
            #self.ser = serial.Serial(port = self.port, baudrate = self.baudrate, timeout = 0.1)
            self.ser.open()
        except serial.SerialException:
            print('can\'t open serial port')
            return 0
        else:
            #self.sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
            return 1

    #im920s send
    def im920s_writef(self, command, data):
        self.ser.write((str(command) + ' ' + str(data) + str(crlf)).encode('utf-8'))
        return

    def read_serial_buffer(self):
        if self.ser.inWaiting():
            data = self.ser.read().decode('utf-8')
            self.buf.add(data)
        return

    def read_data(self):
        if self.ser.inWaiting():
            data = self.ser.readline().decode('utf-8')
        return data
