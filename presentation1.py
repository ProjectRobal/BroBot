from DeviceManager import DeviceManager
from devices.Gyroscope import Gyroscope
from devices.DistanceSensor import DistanceSensor
from devices.Servos import Servos
from devices.Motors import Motors,UPWARD,FAST_STOP
from devices.Ears import Ears
import RPi.GPIO as GPIO
import time



manager = DeviceManager()

gyro= Gyroscope("Gyroscope",0,0)

servos= Servos("Servos",1,1)

motor= Motors("Motors",4)

#ears= Ears("Ears",5)

servos.write({"pwm0":0})
servos.write({"pwm1":-45})
servos.write({"offset1":180.0})




distance_front = DistanceSensor("Distance_Front",2,2)

distance_floor = DistanceSensor("Distance_Floor",3,3)


manager.addDevice(distance_front)
#manager.addDevice(distance_floor)
manager.addDevice(gyro)
manager.addDevice(servos)
manager.addDevice(motor)
#manager.addDevice(ears)

#motor.write({"directionA":UPWARD, "directionB":UPWARD,"speedA":35,"speedB":35})

try:

    distance=0

    while True:
        manager.loop()

        #time.sleep(1)
        #motor.write({"directionA":FAST_STOP, "directionB":FAST_STOP,"speedA":0,"speedB":0})

        distance=manager.getParamsList("Distance_Front")["distance"]

        print(distance)

        if distance < 1800:
            manager.UpdateParams("Servos",{"pwm0":180,"pwm1":-180})
        elif distance >= 1800:
            manager.UpdateParams("Servos",{"pwm0":0,"pwm1":0})

        time.sleep(0.1)

except Exception as e:
    print("Exeption occured: ",e)

finally:
    manager.clear()
    GPIO.cleanup()
