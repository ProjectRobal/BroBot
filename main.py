from DeviceManager import DeviceManager
from devices.Gyroscope import Gyroscope
from devices.DistanceSensor import DistanceSensor
from devices.Servos import Servos
from devices.Motors import Motors,UPWARD,FAST_STOP
from devices.Ears import Ears
import RPi.GPIO as GPIO
import time



manager = DeviceManager()

gyro= Gyroscope("Gyroscope",0,2)

servos= Servos("Servos",1,3)

motor= Motors("Motors",4)

ears= Ears("Ears",5)

servos.write({"pwm0":0})
servos.write({"pwm1":0})
servos.write({"offset1":-180.0})


distance_front_1 = DistanceSensor("Distance_Front1",2,4)
distance_front_2 = DistanceSensor("Distance_Front2",2,5)

#distance_floor = DistanceSensor("Distance_Floor",3,3)


#manager.addDevice(distance_front_1)
#manager.addDevice(distance_front_2)
#manager.addDevice(distance_floor)
manager.addDevice(servos)
manager.addDevice(gyro)
manager.addDevice(motor)
#manager.addDevice(ears)

#motor.write({"directionA":UPWARD, "directionB":UPWARD,"speedA":35,"speedB":35})

print("Everything up and running!")
print("I am awaiting your command")

try:

    opt='h'

    while True:
        manager.loop()

        #time.sleep(1)
        #motor.write({"directionA":FAST_STOP, "directionB":FAST_STOP,"speedA":0,"speedB":0})
        
        opt=input()


        if opt == 'd':

            print(manager.getAllParamsList())

        elif opt == 'm':

            print("Set motor speed A:")

            mA=int(input())

            print("Set motor direction A:")

            dirA=int(input())

            print("Set motor speed B:")

            mB=int(input())

            print("Set motor direction B:")

            dirB=int(input())

            manager.UpdateParams("Motors",{"directionA":dirA, "directionB":dirB,"speedA":mA,"speedB":mB})

        elif opt== 's':
            
            print("Stopping the engines")

            manager.UpdateParams("Motors",{"directionA":FAST_STOP, "directionB":FAST_STOP,"speedA":0,"speedB":0}) 

        elif opt == 'e':
            print("Set ear A: ")
            e1=input()

            print("Set ear B: ")

            e2=input()

            manager.UpdateParams("Servos",{"pwm0":int(e1),"pwm1":int(e2)})
        elif opt == 'h':
            print("d - list all sensors reading")
            print("m - override motors control")
            print("s - stop motors immediately")
            print("e- move ears")



except Exception as e:
    print("Exeption occured: ",e)

finally:
    manager.clear()
    GPIO.cleanup()
