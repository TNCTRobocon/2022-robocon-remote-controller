#!/usr/bin/env python3

from copy import copy
import queue
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
	msg.data = [0, 0]


	pre_state = queue.Queue(2)
	pre_state.put([0, 0])
	# write code=================================
	cp22 = lib.CommunicationProtocol22()
	rj = lib.ReadJoyController()
	# end write data=============================

	while(not rospy.is_shutdown()):
		msg.data[0] = 0
		msg.data[1] = 0
		# write code=============================
		if rj.check_event():
			joystick_data, button_data = rj.get_joystick_data()
			tmp = cp22.encode(joystick_data, button_data)
		# end write code=========================
			pre_state.put(copy(tmp))
			pre_val = pre_state.get()
			tmp[0] = (tmp[0] & (pre_val[0] ^ tmp[0]))
			tmp[1] = tmp[1] & (pre_val[1] ^ tmp[1])
			msg.data = copy(tmp)
			if msg.data[3] == 0:
				msg.data[3] = 255
			else :
				msg.data[3] -= 1
			if msg.data[5] == 0:
				msg.data[5] = 255
			else :
				msg.data[5] -= 1

		rospy.loginfo(msg.data)
		pub.publish(msg)
		rate.sleep()


main()