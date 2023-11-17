# pip3 install adafruit-circuitpython-pca9685
from devices.Device import Device
import DeviceExceptions as errors
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from board import SCL, SDA
import busio

class PWM:
    def __init__(self,off):
        self.off = off
    def __str__(self):
        return str({ "duty cycle": self.off})

class Servos(Device):
    def __init__(self,name,id,port):
        super().__init__(name,id,port)
        self._keys=()
        self._data["frequency"]=50

        self._servos=[servo.Servo]*16
        
        for i in range(16):
            self._data["pwm"+str(i)]=0
            self._data["offset"+str(i)]=0


        self._towrite=("frequency","pwm0","pwm1","pwm2","pwm3","pwm4","pwm5",
        "pwm6","pwm7","pwm8","pwm9","pwm10","pwm11","pwm12","pwm13","pwm14","pwm15","offset0","offset1","offset2","offset3","offset4"
        ,"offset5","offset6","offset7","offset8","offset9","offset10","offset11","offset12","offset13","offset14","offset15")

    def set_frequency(self,frequency):
        self._data["frequency"]=frequency
        self._toupdate=True

    def set_channel(self,channel,pwm):
        if channel is int and pwm is int:
            self._data["pwm"+str(channel)]=pwm
            self._toupdate=True

    def set_offset(self,channel,offset):
        if channel is int and offset is int:
            self._data["offset"+str(channel)]=offset
            
    def set_frequency(self,frequency):
        self._data["frequency"]=frequency
        self._toupdate=True

    def start(self):
        try:
            self.i2c=busio.I2C(SCL,SDA)
            self.pda=PCA9685(self.i2c)

            for i in range(16):
                self._servos[i]=servo.Servo(self.pda.channels[i])

            self._toupdate=True

            self.upload()
        except:
            raise errors.DeviceInitError(self.name(),"Cannot connect to i2c")
    
    def process(self):
        pass

    def download(self):
        pass

    def upload(self):
        #try:
        if self._toupdate:
            self.pda.frequency=self._data["frequency"]
            for i in range(16):
                ang=abs(self._data["pwm"+str(i)]+self._data["offset"+str(i)])

                self._servos[i].angle=ang
                
            self._toupdate = False
        #except:
        #    self._toupdate = False
        #    raise errors.DeviceGeneralFault(self.name(),"Cannot update servos")
        
