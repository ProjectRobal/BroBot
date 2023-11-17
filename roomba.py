from DeviceManager import DeviceManager
from devices.Gyroscope import Gyroscope
from devices.DistanceSensor import DistanceSensor
from devices.Servos import Servos
from devices.Motors import Motors,UPWARD,FAST_STOP
from devices.Ears import Ears
import RPi.GPIO as GPIO
import time


manager = DeviceManager()


distance_front_1 = DistanceSensor("front1",2,4)
distance_front_2 = DistanceSensor("front2",2,5)
servos= Servos("Servos",1,3)
motor= Motors("Motors",4)

manager.addDevice(distance_front_1)
manager.addDevice(distance_front_2)
manager.addDevice(motor)
manager.addDevice(servos)

print("Everything up and running!")

speed=30

try:

    while True:

        manager.loop()

        distance1=manager.getParamsList("front1")['distance']
        distance2=manager.getParamsList("front2")['distance']

        print("Front1: ",distance1)
        print("Front2: ",distance2)

        
        if distance1<=400 or distance2<=400:
            manager.UpdateParams("Motors",{"directionA":0, "directionB":0,"speedA":0,"speedB":speed})
            manager.UpdateParams("Servos",{"pwm2":90,"pwm3":0})
            print("Left")
        else:
            manager.UpdateParams("Motors",{"directionA":0, "directionB":0,"speedA":speed,"speedB":speed})
            manager.UpdateParams("Servos",{"pwm2":90,"pwm3":90})


except Exception as e:
    print("Exeption occured: ",e)

finally:
    manager.clear()
    GPIO.cleanup()