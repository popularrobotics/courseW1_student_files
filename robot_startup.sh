#!/bin/bash

workspace_path=/home/ubuntu/courseW1_ws 

sudo chmod 777 /dev/tty*

source $workspace_path/devel/setup.bash
#chmod +x $workspace_path/script/*

gnome-terminal -x bash -c "roscore" 

gnome-terminal -x bash -c "sleep 2 && cd /home/ubuntu/robociti-robot/robociti-connect && npm start && exec bash" 

#gnome-terminal -x bash -c "sleep 2 && ./ngrok tcp 22 --region=ap --remote-addr 1.tcp.ap.ngrok.io:20320 && exec bash" 

gnome-terminal -x bash -c "sleep 2 && cd /home/ubuntu/courseW1_ws/src/robot_control/src && rosrun robot_control course_w1_remote_control.py" &

#gnome-terminal -x bash -c "sleep 2 && cd /home/ubuntu/courseW1_ws/src/robot_control/src && rosrun robot_control course_w1_cheatsheet.py" &

