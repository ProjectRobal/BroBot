from DeviceManager import DeviceManager
from devices.Gyroscope import Gyroscope
from timeit import default_timer as timer
import time

manager = DeviceManager()

gyro= Gyroscope("Gyroscope",0,2)

manager.addDevice(gyro)

manager.SelectPort(2)

while True:
    manager.loop()

    print("Angel: ",manager.getParamsList("Gyroscope")["gyroscope"])
    print("Accel: ",manager.getParamsList("Gyroscope")["acceleration"])

    time.sleep(0.2)