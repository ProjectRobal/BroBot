# a module to read data from microphones
from devices.Device import Device
import DeviceExceptions as errors
import pyaudio
import numpy as np

AUDIODEVICENAME=""
CHUNK=32000



class Ears(Device):
    def __init__(self,name,id):
        super().__init__(name,id,99)
        self._keys=("channel1","channel2")
        self._data["channel1"]=np.zeros(CHUNK,dtype=np.int32)
        self._data["channel2"]=np.zeros(CHUNK,dtype=np.int32)

    def callback(self,input_data, frame_count, time_info, status_flags):

        frames=np.frombuffer(input_data,dtype=np.int16)
        
        self._data["channel1"]=np.roll(self._data["channel1"],256)
        self._data["channel2"]=np.roll(self._data["channel2"],256)
        i=0

        for x in frames[0::2]:
            self._data["channel1"][i]=x
            i+=1

        i=0

        for x in frames[1::2]:
            self._data["channel2"][i]=x
            i+=1

        return (input_data, pyaudio.paContinue)
    
    def start(self):

        try:

            self.audio=pyaudio.PyAudio()
            self.stream=self.audio.open(
                format=pyaudio.paInt16,
                rate=16000,
                channels=2,
                input=True,
                frames_per_buffer=256,
                stream_callback=self.callback
            )
        except:
            raise errors.DeviceInitError(self.name(),"Cannot start audio device")
        
    def download(self):
        pass

    def process(self):
        pass
    def upload(self):
        pass

    def __del__(self):
        if hasattr(self,"stream"):
            self.stream.stop_stream()
            self.stream.close()