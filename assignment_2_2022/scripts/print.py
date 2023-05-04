#! /usr/bin/env python

import rospy
import math
import time
from assignment_2_2022.msg import Position_velocity

frequency = 1.0
last_print = 0
# Function that process position and velocity information
def info(data):
	global frequency, last_print
	# Get the current time in milliseconds
	c_time = time.time() * 1000
	# Check if the time since the last print is greater than the desired frequency 
	if (c_time - last_print) > (1000/frequency):
		# Get the desired x and t position from the ROS parameter server
		d_x = rospy.get_param('des_pos_x')
		d_y = rospy.get_param('des_pos_y')
		# Calculate the distance between the current and desired position		
		distance = math.sqrt((d_x - data.x)**2 + (d_y - data.y)**2)
		# Calculate the velocity
		vel = math.sqrt(data.v_x**2 + data.v_y**2)
		# Print the distance and velocity 
		rospy.loginfo("Distance to goal: {}, Average speed: {}".format(distance, vel))
		# Update the last print time to the current time
		last_print = c_time
	
	

def main():
	global frequency
	# Initialize the node
	rospy.init_node('print')
	# Get the frequency parameter from the ROS parameter server
	frequency = rospy.get_param("freq")
	# Subscribe to the position_velocity topic and pass the info info callback function
	info_pos = rospy.Subscriber("/position_velocity", Position_velocity, info)
	# Spin the node to keep it running
	rospy.spin()

if __name__ == '__main__':
	main()


