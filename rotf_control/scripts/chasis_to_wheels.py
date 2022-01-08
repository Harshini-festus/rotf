import time
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
rospy.init_node("chasis_to_wheel",anonymous="false")
vel_l=0
vel_r=0
x=0.0
y=0.0
r=0.0
base_width=0.34
rate =rospy.Rate(2)
left_wheel_veloity=rospy.Publisher("/velocity_controller/left_wheel_controller/command",Float64,queue_size=1)
right_wheel_velocity=rospy.Publisher("/velocity_controller/right_wheel_controller/command",Float64,queue_size=1)
def twistCallback(msg):
    x = msg.linear.x
    r = msg.angular.z
    return x,r
cmd_vel=rospy.Subscriber("/cmd_vel",Twist, twistCallback)
chasis_v=twistCallback(cmd_vel)
chasis_velocity=list(chasis_v)

vel_r = chasis_velocity[0] + chasis_velocity[1]* base_width / 2 
vel_l = chasis_velocity[0] - chasis_velocity[1]* base_width / 2 

while not rospy.is_shutdown():
    left_wheel_velocity.publish(vel_l)
    right_wheel_velocity.publish(vel_r)
    rate.sleep()

# import time
# import numpy as np
# from sensor_msgs.msg import Joy
# # !/usr/bin/env python
# import rospy
# from geometry_msgs.msg import Twist
# from std_msgs.msg import Float64

# rospy.init_node('cmd_vel_listener_rpm_publisher')
# left_wheel_veloity=rospy.Publisher("/velocity_controller/left_wheel_controller/command",Float64,queue_size=1)
# right_wheel_velocity=rospy.Publisher("/velocity_controller/right_wheel_controller/command",Float64,queue_size=1)
# rate = rospy.Rate(25.0)
# rpm_left=0
# rpm_right=0
# wheel_diameter = 0.2
# track_width = 0.34
# factor_linearX = 1.0
# factor_angularZ = 1.0
# resolution_vitesse = 0.25
# x = 0.0
# z = 0.0

# def callback(msg):
#     x = msg.linear.x
#     z = msg.angular.z
#     rpm_left = (x*60.0*factor_linearX/(3.14*wheel_diameter)-z*factor_angularZ*track_width*60.0/(wheel_diameter*3.14*2.0))*resolution_vitesse
#     rpm_right = (x*60.0*factor_linearX/(3.14*wheel_diameter)+z*factor_angularZ*track_width*60.0/(wheel_diameter*3.14*2.0))*resolution_vitesse
	
#     #print(x,z)
#     #perimeter=3.14*wheel_diameter
#     #track_width=wheel_seperation
#     #rate.sleep()

# print("right_rpm",rpm_right,"left_rpm",rpm_left)

# def listener_and_pub():
# 	rospy.Subscriber("/cmd_vel", Twist, callback) #/cmd_vel /key_vel /ps3_vel /joy
# 	rospy.spin()
# 	left_wheel_veloity.publish(rpm_left)
#       right_wheel_velocity.publish(rpm_right)
# if __name__ == '__main__':
# 	try:
# 		listener_and_pub()
# 	except rospy.ROSInterruptException:
# 		pass
