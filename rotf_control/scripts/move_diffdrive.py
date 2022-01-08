#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from rospy.names import valid_name_validator_resolved
from std_msgs.msg import Float64
from math import *
rospy.init_node('move_diffdrive') # defining the ros node - publish_node

left_wheel_veloity=rospy.Publisher("/velocity_controller/left_wheel_controller/command",Float64,queue_size=1)
right_wheel_velocity=rospy.Publisher("/velocity_controller/right_wheel_controller/command",Float64,queue_size=1)

rate =rospy.Rate(2) # frequency at which publishing
move=Twist()
v_l=0
v_r=0
base_width=0.34
x=0
w=0
print("node started!!...")
# velocity_l=move.linear.x+omega*l/2
# velocity_r=-(move.linear.x-omega*l/2)
def callback(msg):
	global x, w
	x=msg.linear.x
	w=msg.angular.z
while not rospy.is_shutdown():
	pub = rospy.Subscriber('/cmd_vel', Twist,callback)
	v_r=x+base_width*w/2
	v_l=x-base_width*w/2
	# print(w)
	# print(v_r,"---right wheel velocity")
	# print(v_l,"left wheel veloity")
	left_wheel_veloity.publish(v_l)
	right_wheel_velocity.publish(v_r)
	rate.sleep()
