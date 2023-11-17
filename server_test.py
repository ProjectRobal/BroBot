import network.server as server
from DeviceManager import DeviceManager
from devices.Gyroscope import Gyroscope
from devices.DistanceSensor import DistanceSensor
from devices.Servos import Servos
from devices.Motors import Motors,UPWARD,FAST_STOP
from devices.Ears import Ears



manager = DeviceManager()

gyro= Gyroscope("Gyroscope",0,2)

servos= Servos("Servos",1,3)

motor= Motors("Motors",4)

ears= Ears("Ears",5)

servos.write({"pwm0":0})
servos.write({"pwm1":0})
servos.write({"offset1":-180.0})


distance_front_1 = DistanceSensor("Distance_Front1",2,4)
distance_front_2 = DistanceSensor("Distance_Front",2,5)


#distance_front = DistanceSensor("Distance_Front",2,2)

#distance_floor = DistanceSensor("Distance_Floor",3,3)


manager.addDevice(distance_front_1)
manager.addDevice(distance_front_2)
manager.addDevice(gyro)
manager.addDevice(servos)
manager.addDevice(motor)
#manager.addDevice(ears)

input("Press any key to continue")

server.run(manager,'192.168.2.202:5051')

motor.emergency()