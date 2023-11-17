from microphone import Microphone
import numpy as np
np.set_printoptions(threshold=np.inf)

mic=Microphone()

print(mic.record(10))