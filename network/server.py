from concurrent import futures
import grpc
import _grpc.rc_service_pb2 as rc_service_pb2
from _grpc.rc_service_pb2 import Message,_None,Gyroscope,DistanceSensor,AudioChunk
import _grpc.rc_service_pb2_grpc as rc_service_pb2_grpc
from DeviceManager import DeviceManager
import DeviceExceptions as errors
import numpy as np

class RCRobotServicer(rc_service_pb2_grpc.RCRobotServicer):
    def __init__(self,manager):
        self._manager = manager
        self._status=0
        self._message=""

    
    def UpdateParams(self,params):
        try:
            self._manager.UpdateParams("Motors",{"speedA":params.mA.speed,"directionA":params.mA.direction,"speedB":params.mB.speed,"directionB":params.mB.direction})
        except errors.GeneralDeviceError as e:
            self._message=str(e)
            self._code=e.code

        try:
            self._manager.UpdateParams("Servos",{"pwm0":params.ear1.angle,"pwm1":params.ear2.angle})
        except errors.GeneralDeviceError as e:
            self._message=str(e)
            self._code=e.code        

    def PackageData(self):
        self._message=""
        data=self._manager.getParamsList("Gyroscope")
        gyro=Gyroscope()
        try:
            gyro=Gyroscope()
            gyro.acceleration[:]=np.array(data["acceleration"],dtype=np.float32)
            gyro.gyroscope[:]=np.array(data["gyroscope"],dtype=np.float32)
            gyro.accel_range=int(data["accel_range"])
            gyro.gyro_range=int(data["gyro_range"])
        except Exception as e:
            self._status=-1
            self._message+=" No device Gyroscope"   
            gyro.acceleration[:]=np.zeros(3,dtype=np.float32)
            gyro.gyroscope[:]=np.zeros(3,dtype=np.float32)
            gyro.accel_range=0
            gyro.gyro_range=0

        data=self._manager.getParamsList("Distance_Front")
        front=DistanceSensor()

        try:
            front=DistanceSensor(distance=data["distance"])
        except Exception as e:
            self._status=-1
            self._message+=" No front Sensor"  
            front=DistanceSensor(distance=65535)

        data=self._manager.getParamsList("Distance_Front1")
        front1=DistanceSensor()

        try:
            front1=DistanceSensor(distance=data["distance"])
        except Exception as e:
            self._status=-1
            self._message+=" No front Sensor"  
            front1=DistanceSensor(distance=65535)

        data=self._manager.getParamsList("Distance_Floor")

        floor=DistanceSensor()

        try:
                floor=DistanceSensor(distance=data["distance"])
        except Exception as e:
            self._status=-1
            self._message+=" No floor Sensor"  
            floor=DistanceSensor(distance=0)
        
        data=self._manager.getParamsList("Ears")
        left=AudioChunk()
        right=AudioChunk()

        try:
            left=AudioChunk()
            left.data[:]=np.array(data["channel1"],np.int32)
            right=AudioChunk()
            right.data[:]=np.array(data["channel2"],np.int32)
        except Exception as e:
            self._status=-1
            self._message+=" No audio device"
            left.data[:]=np.zeros(32000,np.int32)
            right.data[:]=np.zeros(32000,np.int32)
        
        msg=Message(front=front,front1=front1,floor=floor, left=left, right=right,gyroscope=gyro,status=self._status,message=self._message)

        return msg


    def Process(self,request, context):
        self._message=""
        try:

            self.UpdateParams(request)

            self._manager.loop()

        except errors.DeviceCriticalError as e:
            print(e)
            self._message=str(e)
            self._code=e.code
            self._manager.EmergencyDetach(e.name)
        except errors.GeneralDeviceError as e:
            print(e)
            self._message=str(e)
            self._code=e.code
        except Exception as e:
            self._message=e
            self._code=-98
        except:
            self._message="Some errors"
            self._code=-99
        finally:

            return self.PackageData()



    def SendCommand(self,request,context):
        try:
        
            self.UpdateParams(request)

            self._manager.loop()
        except errors.DeviceCriticalError as e:
            print(e)
            self._message=e
            self._code=e.code
            self._manager.EmergencyDetach(e.name)
        except errors.GeneralDeviceError as e:
            print(e)
            self._message=e
            self._code=e.code
        except Exception as e:
            self._message=e
            self._code=-98
        except:
            self._message="Some errors"
            self._code=-99

        return _None()
    
    def ReadData(self, request, context):

        self._manager.loop()

        return self.PackageData()



def run(manager,addr):
    server= grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    rc_service_pb2_grpc.add_RCRobotServicer_to_server(
        RCRobotServicer(manager),server
    )
    server.add_insecure_port(addr)
    server.start()
    server.wait_for_termination()