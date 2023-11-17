import RPi.GPIO as GPIO
import time

# PWM not working correctly, when I use frequency of 1kHz or 2kHz and use python3 instead of python not it is working :)
# 30 % is minimum duty cycle , on lower engine stall
# and it still not works great
# aparently wirnig pi use diffrent gpio scheme
# it is not moving forward for some reason



GPIO.setmode(GPIO.BCM)


PWM_CHANNELS=(12,13)

PWM_FREQUENCY=50 #in Hz

# a module to control L298N
# I decided to use pwm channel included in RPI GPIOs

#default pins:

PIN0=5
PIN1=6

PIN2=7
PIN3=8

print(PIN0,PIN1,PIN2,PIN3)

GPIO.setup([PIN0,PIN1],GPIO.OUT)

GPIO.setup([PIN2,PIN3],GPIO.OUT)

GPIO.setup(PWM_CHANNELS[0],GPIO.OUT)

pwm=GPIO.PWM(PWM_CHANNELS[0],PWM_FREQUENCY)

GPIO.setup(PWM_CHANNELS[1],GPIO.OUT)

pwm1=GPIO.PWM(PWM_CHANNELS[1],PWM_FREQUENCY)

pwm.start(0)
pwm.ChangeDutyCycle(40)

pwm1.start(0)
pwm1.ChangeDutyCycle(0)


GPIO.output(PIN1,GPIO.HIGH)
GPIO.output(PIN0,GPIO.LOW)

GPIO.output(PIN2,GPIO.HIGH)
GPIO.output(PIN3,GPIO.LOW)

input()

pwm.ChangeDutyCycle(0)
GPIO.output(int(PIN0),GPIO.HIGH)
GPIO.output(int(PIN1),GPIO.HIGH)

pwm1.ChangeDutyCycle(0)
GPIO.output(int(PIN2),GPIO.HIGH)
GPIO.output(int(PIN3),GPIO.HIGH)

GPIO.cleanup()
