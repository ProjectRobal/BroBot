from devices.Device import Device
import RPi.GPIO as GPIO
import DeviceExceptions as errors

#pwm pins number:

PWM_CHANNELS=(12,13)

PWM_FREQUENCY=50 #in Hz

# a module to control L298N
# I decided to use pwm channel included in RPI GPIOs
# It dosen't move upward for some reason

#default pins:

PIN0=6
PIN1=5

PIN2=8
PIN3=7

# a class that describes the motor 
# direction is the direction of upward or backward
# speed is from 0 to 100 in precentage

UPWARD=0
BACKWARD=1
FAST_STOP=2
SLOW_STOP=3

class Motor:
    def __init__(self):
        self.pin1=0
        self.pin2=0
        self.speed=0
        self.direction=FAST_STOP
        

    def set_pins(self,pin1,pin2):
        self.pin1 = pin1
        self.pin2 = pin2
        GPIO.setup(self.pin1,GPIO.OUT)
        GPIO.setup(self.pin2,GPIO.OUT)

    def clear_pins(self):
        GPIO.setup(self.pin1,GPIO.IN)
        GPIO.setup(self.pin2,GPIO.IN)


    def set_direction(self,direction):
        self.direction = direction

        if self.direction !=UPWARD and self.direction != BACKWARD and self.direction != FAST_STOP and self.direction != SLOW_STOP:
            self.direction=FAST_STOP
        
    
    def set_speed(self,speed):
            self.speed = speed
            if self.speed > 100:
                self.speed=100
            if self.speed<0:
                self.speed=0
        

    def set_pwm_pin(self,pwm_channel):
        if pwm_channel>len(PWM_CHANNELS) or pwm_channel<0:
            return
        self.pwm_pin = PWM_CHANNELS[pwm_channel]

        GPIO.setup(self.pwm_pin,GPIO.OUT)
        self.pwm=GPIO.PWM(self.pwm_pin,PWM_FREQUENCY)
        self.pwm.start(0)



    def update(self):
        self.pwm.ChangeDutyCycle(self.speed)
        if self.direction == UPWARD:
            GPIO.output(self.pin1,GPIO.HIGH)
            GPIO.output(self.pin2,GPIO.LOW)
        elif self.direction == BACKWARD:
            GPIO.output(self.pin1,GPIO.LOW)
            GPIO.output(self.pin2,GPIO.HIGH)
        elif self.direction == FAST_STOP:
            GPIO.output(self.pin1,GPIO.LOW)
            GPIO.output(self.pin2,GPIO.LOW)
        elif self.direction == SLOW_STOP:
            GPIO.output(self.pin1,GPIO.HIGH)
            GPIO.output(self.pin2,GPIO.HIGH)

    def __str__(self):
        return str({"direction":self.direction,"speed":self.speed})
    

class ToshibaMotors:
    def __init__(self):
        self.pin1=0
        self.speed=0
        self.direction=FAST_STOP

    def set_pins(self,pin1,pin2=None):
        self.pin1 = pin1
        GPIO.setup(self.pin1,GPIO.OUT)

    def clear_pins(self):
        GPIO.setup(self.pin1,GPIO.IN)

    def set_direction(self,direction):
        self.direction = direction

        if self.direction !=UPWARD and self.direction != BACKWARD and self.direction != FAST_STOP and self.direction != SLOW_STOP:
            self.direction=FAST_STOP
    
    def set_speed(self,speed):
            self.speed = speed
            if self.speed > 100:
                self.speed=100
            if self.speed<0:
                self.speed=0
        

    def set_pwm_pin(self,pwm_channel):
        if pwm_channel>len(PWM_CHANNELS) or pwm_channel<0:
            return
        self.pwm_pin = PWM_CHANNELS[pwm_channel]

        GPIO.setup(self.pwm_pin,GPIO.OUT)
        self.pwm=GPIO.PWM(self.pwm_pin,PWM_FREQUENCY)
        self.pwm.start(0)



    def update(self):
        
        if self.direction == UPWARD:
            GPIO.output(self.pin1,GPIO.HIGH)
            self.pwm.ChangeDutyCycle(self.speed)
        elif self.direction == BACKWARD:
            GPIO.output(self.pin1,GPIO.LOW)
            self.pwm.ChangeDutyCycle(self.speed)
        elif self.direction == FAST_STOP:
            GPIO.output(self.pin1,GPIO.LOW)
            self.pwm.ChangeDutyCycle(0)
        elif self.direction == SLOW_STOP:
            GPIO.output(self.pin1,GPIO.HIGH)
            self.pwm.ChangeDutyCycle(0)

    def __str__(self):
        return str({"direction":self.direction,"speed":self.speed})


class Motors(Device):
    def __init__(self,name,id,motor_type=Motor):
        super().__init__(name,id,99)
        self._data={}
        self._keys=()
        self._towrite=("speedA","speedB","directionA","directionB")
        self._motorA=motor_type()
        self._motorA.set_pwm_pin(1)
        self._motorA.set_pins(PIN0,PIN2)
        self._motorB=motor_type()
        self._motorB.set_pwm_pin(0)
        self._motorB.set_pins(PIN3,PIN1)
        self._data["speedA"]=0
        self._data["speedB"]=0
        self._data["directionA"]=FAST_STOP
        self._data["directionB"]=FAST_STOP
        self._motorA.update()
        self._motorB.update()
        self._toupdate=False

    def emergency(self):
        self._motorA.clear_pins()
        self._motorB.clear_pins()
        self._motorA.set_speed(0)
        self._motorB.set_speed(0)


    def start(self):
        try:
            self._motorA.update()
            self._motorB.update()
        except:
            raise errors.DeviceInitError(self.name(),"Cannot initialize motors")

    def download(self):
        pass

    def process(self):
        try:
            self._motorA.update()
            self._motorB.update()
        except:
            raise errors.DeviceCriticalError(self.name(),"Motors failed , stopping immediately")

    def upload(self):
        if self._toupdate:
            self._motorA.set_speed(self._data["speedA"])
            self._motorA.set_direction(self._data["directionA"])
            self._motorB.set_speed(self._data["speedB"])
            self._motorB.set_direction(self._data["directionB"])
            self._toupdate=False


    