from devices.Device import Device
from libs.mpu6050 import mpu6050
import DeviceExceptions as errors

import os
import json
import numpy as np
import time
from timeit import default_timer as clock
import config

class Gyroscope(Device):
    def __init__(self,name,id,port):
        super().__init__(name,id,port)
        self._data={}
        self._keys=("acceleration","gyroscope","temperature")
        self._towrite=("accel_range","gyro_range","lowpass_filter")
        self.gyro_off=np.zeros(3,dtype=np.float32)
        self.accel_off=np.zeros(3,dtype=np.float32)
        self.last_time=0.0
        self.sample_time=0.0
    
    def get_angels(self,gyroscope,acceleration):
        '''
            Get data from IMU to calculate pitch,roll and yaw
        '''
        angels=np.zeros(3,dtype=np.float32)

        index=np.argmax(acceleration)

        if index == 0:
            angels[2]=np.arctan2(acceleration[1],acceleration[0])
            angels[1]=np.arctan2(acceleration[0],acceleration[2])
        elif index == 1:
            angels[2]=np.arctan2(acceleration[1],acceleration[0])
            angels[1]=np.arctan2(acceleration[1],acceleration[2])
        else:
            angels[0]=np.arctan2(acceleration[1],acceleration[2])
            angels[1]=np.arctan2(acceleration[0],acceleration[1])

        return (angels*(180.0/np.pi))-np.array([0,90.0,1.0],np.float32)

    def calibration_data(self):
        '''
            Read calibration data from environment        
        '''
        try:
            with open(config.IMU_CALIB_FILE,"r") as f:
                calib:dict=json.load(f)

                if "calibration" in calib.keys():
                    self.gyro_off=calib["calibration"][0]
                    self.accel_off=calib["calibration"][1]
        except:
            print("Cannot open config file: "+config.IMU_CALIB_FILE)

    def calibrate(self,N,accel_def=config.DEFAULT_ACCELERAION):
        '''
            Return calibration data that will stored
            N - number of samples
            calib[0] - data from gyroscope
            calib[1] - data from accelerometer
        '''

        calib=np.zeros((2,3),dtype=np.float64)

        for n in range(N):
            calib[0]=calib[0]+np.array(list(self._mpu.get_gyro_data().values()),dtype=np.float32)
            calib[1]=calib[1]+np.array(list(self._mpu.get_accel_data().values()),dtype=np.float32)
            # about 250 Hz
            time.sleep(0.004)

        calib=calib/N

        calib[1]=calib[1]-accel_def

        # save calibration data

        with open(config.IMU_CALIB_FILE,"w") as f:
            json.dump({
                "calibration":calib.tolist()
            },f)

        return calib

    def start(self):
        try:
            self._mpu=mpu6050(0x68)
            self._mpu.set_accel_range(mpu6050.ACCEL_RANGE_2G)
            self._mpu.set_gyro_range(mpu6050.GYRO_RANGE_500DEG)
            self._data["accel_range"]=self._mpu.read_accel_range()
            self._data["gyro_range"]=self._mpu.read_gyro_range()
            self.calibration_data()
        except Exception as e:
            print(str(e))
            raise errors.DeviceInitError(self.name(),"Cannot connect to i2c")

    def download(self):
        try:
            self.sample_time=clock()-self.last_time

            if self.sample_time>0:
                accel=np.array(list(self._mpu.get_accel_data().values()),dtype=np.float32)-self.accel_off
                gyro=np.array(list(self._mpu.get_gyro_data().values()),dtype=np.float32)-self.gyro_off

                angels=self.get_angels(gyro,accel)

                self._data[self._keys[0]]=accel
                self._data[self._keys[1]]=angels
                self._data[self._keys[2]]=self._mpu.get_temp()
            
            self.last_time=clock()

        except:
            self._data[self._keys[0]]=[float('nan'),float('nan'),float('nan')]
            self._data[self._keys[1]]=[float('nan'),float('nan'),float('nan')]
            self._data[self._keys[2]]=float('nan')
            raise errors.DeviceGeneralFault(self.name(),"Cannot read gyroscope data")

    def upload(self):
        try:
            if self._toupdate:
                self._mpu.set_accel_range(self._data[self._towrite[0]])
                self._mpu.set_gyro_range(self._data[self._towrite[1]])
                self._mpu.set_filter_range(self._data[self._towrite[2]])
                self._toupdate=False
        except:
            self._toupdate=False
            raise errors.DeviceGeneralFault(self.name(),"Cannot update gyroscope parameters")

    def process(self):
        pass
