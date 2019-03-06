#!/usr/bin/env python
# Popular Robotics Remote Control Code for course_w1
# Last edited by Lyuzhou Zhuang on 12/3/2018

"""
# This file enables the robot to be remotely controlled over Wifi from other devices.
#
# This file could also run on its own.
#
# PREREQUISITES
#	Tornado Web Server for Python
#
# Copyright
#   All rights reserved. No part of this script may be reproduced, distributed, or transmitted in any 
#   form or by any means, including photocopying, recording, or other electronic or mechanical methods, 
#   without prior written permission from Popular Robotics, except in the case of brief quotations embodied 
#   in critical reviews and certain other noncommercial uses permitted by copyright law. 
#   For permission requests, contact Popular Robotics directly.
#
# TROUBLESHOOTING:
#	  Don't use Ctrl+Z to stop the program, use Ctrl+c.
#	  If you use Ctrl+Z, it will not close the socket and you won't be able to run the program the next time.
#	  If you get the following error:
#		  "socket.error: [Errno 98] Address already in use "
#	  Run this on the terminal:
#		  "sudo netstat -ap |grep :9093"
#	  Note down the PID of the process running it
#	  And kill that process using:
#		  "kill pid"
#	  If it does not work use:
#		  "kill -9 pid"
#	  If the error does not go away, try changin the port number '9093' both in the client and server code
#
"""

import time,sys,json

# Import the ArmRobot.py file (must be in the same directory as this file!).
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


def t_up(speed, t_time):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(AIN2, False)    # AIN2
    GPIO.output(AIN1, True)     # AIN1

    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN2, False)    # BIN2
    GPIO.output(BIN1, True)     # BIN1
    time.sleep(t_time)


def t_stop(t_time):
    L_Motor.ChangeDutyCycle(0)
    GPIO.output(AIN2, False)    # AIN2
    GPIO.output(AIN1, False)    # AIN1

    R_Motor.ChangeDutyCycle(0)
    GPIO.output(BIN2, False)    # BIN2
    GPIO.output(BIN1, False)    # BIN1
    time.sleep(t_time)


def t_down(speed, t_time):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(AIN2, True)     # AIN2
    GPIO.output(AIN1, False)    # AIN1

    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN2, True)     # BIN2
    GPIO.output(BIN1, False)    # BIN1
    time.sleep(t_time)


def t_left(speed, t_time):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(AIN2, True)     # AIN2
    GPIO.output(AIN1, False)    # AIN1

    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN2, False)    # BIN2
    GPIO.output(BIN1, True)     # BIN1
    time.sleep(t_time)


def t_right(speed, t_time):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(AIN2, False)    # AIN2
    GPIO.output(AIN1, True)     # AIN1

    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN2, True)     # BIN2
    GPIO.output(BIN1, False)    # BIN1
    time.sleep(t_time)


def setServoPulse(channel, pulse):
    pulseLength = 1000000.0             # 1,000,000 us per second
    pulseLength /= 50.0                       # 60 Hz
    # print "%d us per period" % pulseLength
    pulseLength /= 4096.0                  # 12 bits of resolution
    # print "%d us per bit" % pulseLength
    pulse *= 1000.0
    pulse /= (pulseLength*1.0)
    # pwmV=int(pulse)
    print "pulse: %f  " % pulse
    pwm.setPWM(channel, 0, int(pulse))


# Angle to PWM
def write(servonum, x):
    y = x/90.0+0.5
    y = max(y, 0.5)
    y = min(y, 2.5)
    setServoPulse(servonum, y)


c = 0


# Initialize Tornado to use 'GET' and load index.html
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        loader = tornado.template.Loader(".")
        self.write(loader.load("index.html").generate())


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
            t_up(50, 0)
        elif c == 2:
            print "Running Reverse"
            t_down(50, 0)
        elif c == 4:
            print "Turning Right"
            t_right(50, 0)
        elif c == 6:
            print "Turning Left"
            t_left(50, 0)
        elif c == 5:
            print "Stopped"
            t_stop(0)    # Stop the robot from moving.
        elif c == 1:
            print "Arm Claw:", v
            write(0, v)
        elif c == 3:
            print "Arm Waist:", v
            write(1, v)
        elif c == 7:
            print "Arm Left:",v
            write(2, v)
        elif c == 9:
            print "Arm Rigth:",v
            write(3, v)
        print "Values Updated"

    def on_close(self):
        # robot.stop()  # Stop the robot from moving.
        print 'connection closed...'


application = tornado.web.Application([
    (r'/ws', WSHandler),
    (r'/', MainHandler),
    (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./resources"}),
])


class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print "Ready"
        while running:
            time.sleep(.2)  # sleep for 200 ms


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # Numbers GPIOs by physical location
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
  
pwm.setPWMFreq(50)  # Set frequency to 60 Hz
running = True
thread1 = myThread(1, "Thread-1", 1)
thread1.setDaemon(True)
thread1.start()
application.listen(9093)    # starts the websockets connection
tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    c = 0
