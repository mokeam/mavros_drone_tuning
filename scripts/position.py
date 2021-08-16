#!/usr/bin/env python

import rospy
import numpy

from geometry_msgs.msg import PoseStamped

index = 0 
wps = list()
msg = PoseStamped()

def update_position():
    global index
    index = (index + 1) % len(wps)
    p = msg.pose.position
    p.x, p.y, p.z = wps[index].tolist()
    q = msg.pose.orientation
    q.w = 1


if __name__ == "__main__":
    print('Run position MavROS tuner')
    rospy.init_node("px4_position_tuning")
    pub = rospy.Publisher("/mavros/setpoint_position/local", PoseStamped, queue_size=0)
    rate = rospy.Rate(50)
    loop_duration = rospy.Duration.from_sec(10)
    stamp = rospy.Time.now() + loop_duration

    wp1 = numpy.array([0,0,1])
    wp2 = numpy.array([0,-1,1])
    wps.append(wp1)
    wps.append(wp2)

    while not rospy.is_shutdown():
        if stamp < rospy.Time.now():
            stamp += loop_duration
            update_position()
            print('Transition to new waypoint: ', msg.pose.position)
        msg.header.stamp = rospy.Time.now()
        pub.publish(msg)
        rate.sleep()

