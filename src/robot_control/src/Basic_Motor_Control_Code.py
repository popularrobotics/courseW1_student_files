#!/usr/bin/env python
# Popular Robotics Course Template
# Last edited by Lyuzhou Zhuang on 10/30/2018

"""
# This file contains all the necessary code to drive the motor part of
# the robot for course_W1.
#
# This file could also run on its own
#
# PREREQUISITES
#   Tornado Web Server for Python
#
# Copyright
#   All rights reserved. No part of this script may be reproduced, distributed, or transmitted in any 
#   form or by any means, including photocopying, recording, or other electronic or mechanical methods, 
#   without prior written permission from Popular Robotics, except in the case of brief quotations embodied 
#   in critical reviews and certain other noncommercial uses permitted by copyright law. 
#   For permission requests, contact Popular Robotics directly.
#
# TROUBLESHOOTING:
#   Don't use Ctrl+Z to stop the program, use Ctrl+c.
#	If you use Ctrl+Z, it will not close the socket and you won't be able to run the program the next time.
#	If you get the following error:
#		"socket.error: [Errno 98] Address already in use "
#	Run this on the terminal:
#		"sudo netstat -ap |grep:9093"
#	Note down the PID of the process running it
#	And kill that process using:
#		"kill pid"
#	If it does not work use:
#		"kill -9 pid"
#	If the error does not go away, try changin the port number '9093' both in the client and server code
"""


# import rospy
# from std_msgs.msg import String
import time, json

# Import the Adafruit_PWM_Servo_Driver.py file (must be in the same directory as this file!).
from Adafruit_PWM_Servo_Driver import PWM
import RPi.GPIO as GPIO  
import threading
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import tornado.escape

# Initialise the PWM device using the default address
pwm = PWM(0x40)
servoMin = 150  # Min pulse length out of 4096  #150
servoMax = 600  # Max pulse length out of 4096 #600

PWMA = 18
AIN1 = 22
AIN2 = 27

PWMB = 23
BIN1 = 25
BIN2 = 24


def vehicle_move_forward(speed, duration):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(AIN2, False)    # AIN2
    GPIO.output(AIN1, True)     # AIN1

    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN2, False)    # BIN2
    GPIO.output(BIN1, True)     # BIN1
    time.sleep(duration)


def vehicle_stop_moving_for(duration):
    L_Motor.ChangeDutyCycle(0)
    GPIO.output(AIN2, False)    # AIN2
    GPIO.output(AIN1, False)    # AIN1

    R_Motor.ChangeDutyCycle(0)
    GPIO.output(BIN2, False)    # BIN2
    GPIO.output(BIN1, False)    # BIN1
    time.sleep(duration)


def vehicle_move_backward(speed, duration):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(AIN2, True)     # AIN2
    GPIO.output(AIN1, False)    # AIN1

    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN2, True)     # BIN2
    GPIO.output(BIN1, False)    # BIN1
    time.sleep(duration)


def vehicle_turn_left(speed, duration):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(AIN2, True)     # AIN2
    GPIO.output(AIN1, False)    # AIN1

    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN2, False)    # BIN2
    GPIO.output(BIN1, True)     # BIN1
    time.sleep(duration)


def vehicle_turn_right(speed, duration):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(AIN2, False)    # AIN2
    GPIO.output(AIN1, True)     # AIN1

    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN2, True)     # BIN2
    GPIO.output(BIN1, False)    # BIN1
    time.sleep(duration)


def set_servo_pulse(channel, pulse):
    pulse_length = 1000000.0    # 1, 000, 000 us per second
    pulse_length /= 50.0        # 60 Hz
    # print "%d us per period" % pulse_length
    pulse_length /= 4096.0      # 12 bits of resolution
    # print "%d us per bit" % pulse_length
    pulse *= 1000.0
    pulse /= (pulse_length*1.0)
    # pwmV=int(pulse)
    # print "pulse: %f  " % pulse
    pwm.setPWM(channel, 0, int(pulse))


# Angle to PWM
def arm_motor_position(servo_num, x):
    y = x/90.0+0.5
    y = max(y, 0.5)
    y = min(y, 2.5)
    set_servo_pulse(servo_num, y)


def destroy():
    GPIO.cleanup()


c = 0


# Initialize Tornado to use 'GET' and load index.html
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        loader = tornado.template.Loader(".")
        self.arm_motor_position(loader.load("index.html").generate())


# Code for handling the data sent from the webpage
class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'connection opened...'

    def on_message(self, message):      # receives the data from the webpage and is stored in the variable message
        global c
        print 'received:', message        # prints the revived from the webpage
        decodejson = json.loads(message)
        c = decodejson['eventType']
        v = decodejson['eventValue']
        print 'eventType:', c
        if c == 8:
            print "Running Forward"
            vehicle_move_forward(50, 0)
        elif c == 2:
            print "Running Reverse"
            vehicle_move_backward(50, 0)
        elif c == 4:
            print "Turning Right"
            vehicle_turn_right(50, 0)
        elif c == 6:
            print "Turning Left"
            vehicle_turn_left(50, 0)
        elif c == 5:
            print "Stopped"
            vehicle_stop_moving_for(0)    # Stop the robot from moving.
        elif c == 1:
            print "Arm Claw:", v
            arm_motor_position(0, v)
        elif c == 3:
            print "Arm Waist:", v
            arm_motor_position(1, v)
        elif c == 7:
            print "Arm Left:", v
            arm_motor_position(2, v)
        elif c == 9:
            print "Arm Right:", v
            arm_motor_position(3, v)
        print "Values Updated"

    def on_close(self):
        # robot.stop()  # Stop the robot from moving.
        print 'connection closed...'


application = tornado.web.Application([
    (r'/ws', WSHandler),
    (r'/', MainHandler),
    (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./resources"}),
])


class MyThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print "Ready"
        while running:
            time.sleep(.2)              # sleep for 200 ms


###############################


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)

GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)

L_Motor = GPIO.PWM(PWMA, 100)
L_Motor.start(0)
R_Motor = GPIO.PWM(PWMB, 100)
R_Motor.start(0)

pwm.setPWMFreq(50)                        # Set frequency to 60 Hz
running = True

""" following scripts are for controlling the robot over the internet
thread1 = MyThread(1, "Thread-1", 1)
thread1.setDaemon(True)
thread1.start()
application.listen(9093)          	#starts the websockets connection
tornado.ioloop.IOLoop.instance().start()
"""


def test_wheel_motors():    # test to see if wheel motors function properly
    vehicle_move_forward(50, 1)  # arguments: speed, duration (seconds)
    vehicle_stop_moving_for(.2)  # argument: duration (seconds)
    vehicle_move_backward(50, 1)
    vehicle_stop_moving_for(.2)
    vehicle_turn_left(50, 1)
    vehicle_stop_moving_for(.2)
    vehicle_turn_right(50, 1)
    vehicle_stop_moving_for(.2)


def test_arm_motors():  # test to see if arm motors function properly
    # print "arm position 1"
    arm_motor_position(0, 80)  # 0 for Claw, 0-45 degrees
    print "claw open"
    time.sleep(3)
    arm_motor_position(1, 160)  # 1 for Waist, upperarm, up or down, 90-180 degrees
    print "waist(right) down"
    time.sleep(3)
    arm_motor_position(2, 80)  # 2 for Arm Left, forearm, stretch in or out, 60-120 degrees
    print "arm(left) in"
    time.sleep(3)
    arm_motor_position(3, 20)  # 3 for Arm orientation, left or right, 10-170 degrees
    print "base turn right"
    time.sleep(3)
    # print "arm position 2"
    arm_motor_position(0, 30)  # 0 for Claw, 0-45 degrees
    print "claw close"
    time.sleep(3)
    arm_motor_position(1, 100)  # 1 for Waist, upperarm, up or down, 90-180 degrees
    print "waist(right) up"
    time.sleep(3)
    arm_motor_position(2, 110)  # 2 for Arm Left, forearm, stretch in or out, 60-120 degrees
    print "arm(left) out"
    time.sleep(3)
    arm_motor_position(3, 80)  # 3 for Arm orientation, left or right, 10-170 degrees
    print "base center"
    #time.sleep(3)
    print "arm test complete"
    time.sleep(3)


# -------------------------

if __name__ == "__main__":
    try:
        test_wheel_motors()
        #test_arm_motors()
    except KeyboardInterrupt:
        destroy()
