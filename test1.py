import struct
import time
import serial

class GY25:
    def __init__(self, port, baudrate=115200):  # دقت کن بعضی ماژول‌ها 9600 یا 115200 دارن
        self.ser = serial.Serial(port, baudrate, timeout=0.1)
        time.sleep(2)
        # فعال‌سازی continuous output
        self.ser.write(b'\xA5\x54')
        time.sleep(0.1)
        self.ser.write(b'\xA5\x51')

    def read_angles(self):
        # بخون 8 بایت
        self.ser.write(b'\xA5\x51')
        buf = self.ser.read(8)
        if not buf or len(buf) < 8:
            return None
        if buf[0] != 0xAA or buf[7] != 0x55:
            return None
        # print(buf)
        yaw   = struct.unpack(">h", buf[1:3])[0] / 100.0
        pitch = struct.unpack(">h", buf[3:5])[0] / 100.0
        roll  = struct.unpack(">h", buf[5:7])[0] / 100.0
        return (roll, pitch, yaw)
    
gy25 = GY25("COM14")
while True:
    print(gy25.read_angles())
    time.sleep(0.01)