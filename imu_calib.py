from DeviceManager import DeviceManager
from devices.Gyroscope import Gyroscope


manager = DeviceManager()

gyro= Gyroscope("Gyroscope",0,2)

manager.addDevice(gyro)

manager.SelectPort(2)

print(gyro.calibrate(200))