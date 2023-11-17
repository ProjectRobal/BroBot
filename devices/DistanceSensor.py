from devices.Device import Device
import DeviceExceptions as errors
import board
import busio
import adafruit_vl53l0x

class DistanceSensor(Device):
    def __init__(self,name,id,port):
        super().__init__(name,id,port)
        self._data={}
        self._keys=("distance","timing")
        self._towrite=()
    
    def start(self):
        try:
            self._i2c= busio.I2C(board.SCL, board.SDA)
            self._sensor=adafruit_vl53l0x.VL53L0X(self._i2c)
        except:
            raise errors.DeviceInitError(self.name(),"Cannot connect to I2C")

    def download(self):

        try:

            self._data[self._keys[0]]=float(self._sensor.range)

        except:
            self._data[self._keys[0]]=-1
            raise errors.DeviceGeneralFault(self.name(),"Cannot read distance data")



    def process(self):
        pass

    def upload(self):
        pass




