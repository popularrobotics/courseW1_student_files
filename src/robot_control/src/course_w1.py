#!/usr/bin/env python
# Popular Robotics CourseW1 Template
# Last edited by Lyuzhou Zhuang on 2/19/2019

"""
# Copyright
#   All rights reserved. No part of this script may be reproduced, distributed, or transmitted in any 
#   form or by any means, including photocopying, recording, or other electronic or mechanical methods, 
#   without prior written permission from Popular Robotics, except in the case of brief quotations embodied 
#   in critical reviews and certain other noncommercial uses permitted by copyright law. 
#   For permission requests, contact Popular Robotics directly.
"""

# The below commands imports other python files (modules) to be used in this script.
import Basic_Motor_Control_Code as Motor


# ----- example functions below -----

def test_wheel_motors():
    # test to see if wheel motors function properly
    Motor.vehicle_move_forward(50, 0.5) # arguments: speed (between 0 and 100), duration (seconds)
    Motor.vehicle_stop_moving_for(.2)   # argument: duration (seconds)
    Motor.vehicle_move_backward(50, 0.5)
    Motor.vehicle_stop_moving_for(.2)
    Motor.vehicle_turn_left(50, 0.5)
    Motor.vehicle_stop_moving_for(.2)
    Motor.vehicle_turn_right(50, 0.5)
    Motor.vehicle_stop_moving_for(.2)

# ----- example functions above -----


# ***** student edits start *****
# students define their own functions here.

def student_function():
    test_wheel_motors()  # You could comment this out if the wheel motors function properly
    Motor.vehicle_move_forward(50, 0.5)
    Motor.vehicle_stop_moving_for(0)
    pass

# ***** student edits end *****


# ----- main function below -----

if __name__ == "__main__":  # call any function below
    student_function()

# ----- main function above -----
