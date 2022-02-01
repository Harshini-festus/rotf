#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
rospy.init_node("laser_data_publisher")
scan=LaserScan()
def callback(msg):
    scan.header=msg.header
    scan.intensities=msg.intensities
    scan.range_max=msg.range_max
    scan.range_min=msg.range_min
    scan.angle_increment=msg.angle_increment
    scan.angle_max=msg.angle_max
    scan.angle_min=msg.angle_min
    scan.time_increment=msg.time_increment
    
rate=rospy.Rate(100)
while not rospy.is_shutdown():
    scan_received=rospy.Subscriber("/diff_bot/laser/scan", callback)
    scan_sent=rospy.Publisher("/scan", LaserScan, queue_size=1)
    scan_sent(scan)
    rate.sleep()