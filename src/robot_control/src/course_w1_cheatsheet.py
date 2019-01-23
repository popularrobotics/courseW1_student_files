#!/usr/bin/env python
# Popular Robotics CourseW1 Template
# Last edited by Lyuzhou Zhuang on 12/3/2018

"""
# This file acts as a cheatsheet, which contains some reference
# functions/answers to student challenges, especially the autonomous
# driving challenge.
# Students should try to tackle the challenges on their own before checking this file.
#
# This file could also run on its own.
#
# Copyright
#   All rights reserved. No part of this script may be reproduced, distributed, or transmitted in any 
#   form or by any means, including photocopying, recording, or other electronic or mechanical methods, 
#   without prior written permission from Popular Robotics, except in the case of brief quotations embodied 
#   in critical reviews and certain other noncommercial uses permitted by copyright law. 
#   For permission requests, contact Popular Robotics directly.
#
"""

import Basic_Motor_Control_Code as Motor
import Three_Ultrasonic_Sensors as Ultrasonic
import time


def test_wheel_motors():    # test to see if wheel motors function properly
    Motor.vehicle_move_forward(50, 0.5)  # arguments: speed, duration (seconds)
    Motor.vehicle_stop_moving_for(.2)  # argument: duration (seconds)
    Motor.vehicle_move_backward(50, 0.5)
    Motor.vehicle_stop_moving_for(.2)
    Motor.vehicle_turn_left(50, 0.5)
    Motor.vehicle_stop_moving_for(.2)
    Motor.vehicle_turn_right(50, 0.5)
    Motor.vehicle_stop_moving_for(.2)


def test_arm_motors():  # test to see if arm motors function properly
    Motor.arm_motor_position(0, 10)   # 0 for Claw, 0-45 degrees
    Motor.arm_motor_position(1, 90)   # 1 for Waist, upperarm, up or down, 90-180 degrees
    Motor.arm_motor_position(2, 60)   # 2 for Arm Left, forearm, stretch in or out, 60-120 degrees
    Motor.arm_motor_position(3, 20)   # 3 for Arm orientation, left or right, 10-170 degrees
    time.sleep(1)
    Motor.arm_motor_position(0, 40)   # 0 for Claw, 0-45 degrees
    Motor.arm_motor_position(1, 120)  # 1 for Waist, upperarm, up or down, 90-180 degrees
    Motor.arm_motor_position(2, 110)  # 2 for Arm Left, forearm, stretch in or out, 60-120 degrees
    Motor.arm_motor_position(3, 80)  # 3 for Arm orientation, left or right, 10-170 degrees
    time.sleep(1)


def test_ultrasonic_sensors():  # test to see if the ultrasonic sensors function properly
    # Mind the GPIO mode conflict!!!
    try:
        Ultrasonic.loop_read_distance()
    except KeyboardInterrupt:
        Ultrasonic.destroy()


def cal_average(lst):   # calculate the mean of a list of numbers
    return sum(lst)/len(lst)


def cal_variance(lst):
    # The purpose of this function is to calculate
    # the variance of a list of numbers
    ave = cal_average(lst)
    total = 0
    for i in lst:
        total += (i-ave)**2
    return total/len(lst)


def is_it_a_ramp(lst_front, lst_left, lst_right):
    # The purpose of this function is to test if there's
    # a ramp ahead of the vehicle
    """
    var_f = cal_variance(lst_front)
    var_l = cal_variance(lst_left)
    var_r = cal_variance(lst_right)
    var_lst = [var_f, var_l, var_r]
    var_lst.sort()
    print var_lst
    if (var_lst[0] < 50) and (var_lst[1] < 1700):
        return True
    else:
        return False
    """
    return False


def autonomous_driving():
    # This function reads data from the 3 ultrasonic sensors and enables
    # the wheel robot to go towards one direction while avoiding obstacles
    # automatically

    # Initialization
    angle_turned_right = 0  # To record the angle the robot turned.
    time_moving_forward_start = time.time()
    lst_f = [10]*2
    lst_l = [10]*2
    lst_r = [10]*2
    just_to_activate_the_sensor = Ultrasonic.read_distance(0)
    print 'Front', just_to_activate_the_sensor, 'cm'
    just_to_activate_the_sensor = Ultrasonic.read_distance(1)
    print 'Right', just_to_activate_the_sensor, 'cm'
    just_to_activate_the_sensor = Ultrasonic.read_distance(2)
    print 'Left', just_to_activate_the_sensor, 'cm'
    print '\nUltrasonic sensors initialization completed.\n'
    turn_speed = 50  # between 0 and 100, preferably 50
    # Initialization done

    while True:
        time.sleep(0.2)  # Let the sensors cool down a bit
        front_distance = Ultrasonic.read_distance(0)
        lst_f.pop(0)
        lst_f.append(front_distance)
        right_distance = Ultrasonic.read_distance(1)
        lst_r.pop(0)
        lst_r.append(right_distance)
        left_distance = Ultrasonic.read_distance(2)
        lst_l.pop(0)
        lst_l.append(left_distance)
        print 'Front', front_distance, 'cm'
        print 'Right', right_distance, 'cm'
        print 'Left', left_distance, 'cm'

        if left_distance < 9:
            Motor.vehicle_stop_moving_for(0)
            if is_it_a_ramp(lst_f, lst_l, lst_r):
                print 'Encounter slope < on left !!!\n'
                time_turn_start = time.time()
                Motor.vehicle_turn_left(turn_speed, 0.5)
                time_elapsed = time.time() - time_turn_start
                angle_turned_right -= turn_speed * time_elapsed
                Motor.vehicle_move_backward(50, 1)
            else:
                print 'Encounter obstacle O on left !!!!!!!!!!!!!!!!!!!!!!\n'
                print 'Moving backward...'
                Motor.vehicle_move_backward(50, 0.2)
                print 'Turning right...\n'
                time_turn_start = time.time()
                Motor.vehicle_turn_right(turn_speed, 0.5)
                time_elapsed = time.time() - time_turn_start
                angle_turned_right += turn_speed * time_elapsed
            time_moving_forward_start = time.time()
            continue

        if right_distance < 9:
            Motor.vehicle_stop_moving_for(0)
            if is_it_a_ramp(lst_f, lst_l, lst_r):
                print 'Encounter slope < on right !!!\n'
                time_turn_start = time.time()
                Motor.vehicle_turn_right(turn_speed, 0.5)
                time_elapsed = time.time() - time_turn_start
                angle_turned_right += turn_speed * time_elapsed
                Motor.vehicle_move_backward(50, 1)
            else:
                print 'Encounter obstacle O on right !!!!!!!!!!!!!!!!!!!!!!\n'
                print 'Moving backward...'
                Motor.vehicle_move_backward(50, 0.2)
                print 'Turning left...\n'
                time_turn_start = time.time()
                Motor.vehicle_turn_left(turn_speed, 0.5)
                time_elapsed = time.time() - time_turn_start
                angle_turned_right -= turn_speed * time_elapsed
            time_moving_forward_start = time.time()
            continue

        if front_distance < 10:
            Motor.vehicle_stop_moving_for(0)
            if is_it_a_ramp(lst_f, lst_l, lst_r):
                print 'Encounter slope < on front !!!\n'
                Motor.vehicle_move_forward(80, 0.5)
            else:
                print 'Encounter obstacle O on front !!!!!!!!!!!!!!!!!!!!!!\n'
                print 'Moving backward...'
                Motor.vehicle_move_backward(50, 0.5)
                print 'Turning right...\n'
                time_turn_start = time.time()
                Motor.vehicle_turn_right(turn_speed, 0.5)
                time_elapsed = time.time() - time_turn_start
                angle_turned_right += turn_speed * time_elapsed
            time_moving_forward_start = time.time()
            continue

        if time.time() - time_moving_forward_start > 1.5:
            if angle_turned_right > 0:
                print '\nTurning back to original direction...\n'
                Motor.vehicle_turn_left(turn_speed, angle_turned_right / turn_speed * 1.6)
                angle_turned_right = 0
            elif angle_turned_right < 0:
                print '\nTurning back to original direction...\n'
                Motor.vehicle_turn_right(turn_speed, -angle_turned_right / turn_speed)
                angle_turned_right = 0
            time_moving_forward_start = time.time()

        Motor.vehicle_move_forward(90, 0)
        print "\nSafe. Moving forward...\n"


if __name__ == "__main__":  # call any function below
    autonomous_driving()
