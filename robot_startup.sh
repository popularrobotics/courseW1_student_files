#!/bin/bash

workspace_path=/home/ubuntu/courseW1_ws 

sudo chmod 777 /dev/tty*

source $workspace_path/devel/setup.bash
#chmod +x $workspace_path/script/*

gnome-terminal -x bash -c "roscore" 

gnome-terminal -x bash -c "sleep 2 && cd /home/ubuntu/courseW1_ws/src/robot_control/src && rosrun robot_control course_w1_remote_control.py" &
