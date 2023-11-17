import grpc
import _grpc.rc_service_pb2_grpc as pb2_grpc
from _grpc.rc_service_pb2 import _None,Motor,DistanceSensor,Gyroscope,Servo,AudioChunk,Command,Message


def send_message(stub,speedA,directionA,speedB,directionB,angel1,angel2):

    msg=Command(mA=Motor(direction=directionA,speed=speedA),mB=Motor(direction=directionB,speed=speedB),ear1=Servo(angle=angel1),ear2=Servo(angle=angel2))

    return stub.SendCommand(msg)    

def send_message_data(stub,data):

    return send_message(stub=stub,speedA=data["Motors"]["speedA"],directionA=data["Motors"]["directionA"],speedB=data["Motors"]["speedB"],directionB=data["Motors"]["directionB"],angel1=data["Servos"]["pwm1"],angel2=data["Servos"]["pwm2"])

def process(stub,speedA,directionA,speedB,directionB,angel1,angel2):

    msg=Command(mA=Motor(direction=directionA,speed=speedA),mB=Motor(direction=directionB,speed=speedB),ear1=Servo(angle=angel1),ear2=Servo(angle=angel2))

    return stub.Process(msg)

def process_data(stub,data):

    return process(stub,speedA=data["Motors"]["speedA"],directionA=data["Motors"]["directionA"],speedB=data["Motors"]["speedB"],directionB=data["Motors"]["directionB"],angel1=data["Servos"]["pwm1"],angel2=data["Servos"]["pwm2"])


def get_stub(channel):
    return pb2_grpc.RCRobotStub(channel)

def connect(address):
    return grpc.insecure_channel(address)