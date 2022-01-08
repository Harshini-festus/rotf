#!/usr/bin/env python

from logging import error
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Twist
import math

x =0.0
y = 0.0
v_x = 0.0 
v_y = 0.0
w_z = 0
err = 0.0

tim = 0.0
kp_x , kp_y ,kp_z = 2 , 1.0 , 1.0 
prev_time = 0.0 
dt = 0.0 



def cal_pos(msg):
    global x
    global y
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    # print(x)

    
def cal_vel(msg):
    global v_x
    global v_y
    global w_z
    v_x = msg.twist.twist.linear.x
    v_y = msg.twist.twist.linear.y
    w_z =  msg.twist.twist.angular.z
  
    

def pid(v_x,v_y,w_z):
   global err_x
   global err_y
   global err_z
   corr_x = 0.0
   corr_y=0.0
   corr_z=0.0
   global tim
   tim = rospy.Time.now()
   err_x = v_x - 0.1
   err_y=v_y
   err_z=w_z
   
   prev_error_x =0.0
   prev_error_y=0.0
   prev_error_z=0.0
   #d_error_x = err_x - prev_error_x
   #d_error_y=err_y-prev_error_y
   #d_error_z=err_z-prev_error_z
  
   corr_x = kp_x*(err_x) 
   corr_y=kp_y*(err_y)
   corr_z=kp_z*(err_z)
   correction=[corr_x,corr_y,corr_z]
   prev_error_x= err_x
   prev_error_y=err_y
   prev_error_z=err_z
   return (correction)


rospy.init_node('pos_diffdrive')
sub1 = rospy.Subscriber('/odom',Odometry,cal_pos)
sub2 = rospy.Subscriber('/odom',Odometry,cal_vel)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
rate =rospy.Rate(2)

move = Twist()

v =0.5
d =5




while not rospy.is_shutdown():
    x_goal=d
    if x_goal-x <= 0:
        
        move.linear.x = 0
        move.linear.y =0 
        move.angular.z = 0
        print("stopped")
        
    else:
        # move.linear.x =(x_goal-x)
        # move.linear.y = 0
        corr = pid(v_x,v_y,w_z)
        move.linear.x =corr[0]*(-10)
        move.linear.y=corr[1]*(-10)
        move.angular.z=corr[2]*(0.01)
        move.linear.y =0.0
        print(move.linear.x)

        
    pub.publish(move)
    rate.sleep()


    