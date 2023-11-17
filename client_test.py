import network.client as client
import pyaudio

data = {
    "Motors":
    {
        "speedA":0,
        "directionA":1,
        "speedB":0,
        "directionB":1
    },
    "Servos":
    {
        "pwm1":45,
        "pwm2":135,
    }
}

with client.connect('192.168.50.42:5051') as channels:
    stub=client.get_stub(channels)
    print("Send Command!")
    msg=client.process_data(stub,data)
    print(msg)

