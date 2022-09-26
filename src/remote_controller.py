#!/usr/bin/env python3

import rospy
from std_msgs.msg import UInt8MultiArray

import lib

def main():
    # init config
    rospy.init_node("remote_controller", anonymous=True)

    rate = rospy.Rate(100)
    pub = rospy.Publisher("control_data", UInt8MultiArray, queue_size=10)

    # send message
    ## if you want to assignment,
    ## msg.data = [1, 2, 3] //write any vals
    msg = UInt8MultiArray()

    # write code=================================
    cp22 = lib.CommunicationProtocol22()
    rj = lib.ReadJoyController()
    # end write data=============================

    while(not rospy.is_shutdown):

        # write code=============================
        if rj.check_event():
            joystick_data, button_data = rj.get_joystick_data()
            msg = cp22.encode(joystick_data, button_data)
        # end write code=========================

        pub.publish(msg)
        rate.sleep()


if __name__ == "main":
    main()