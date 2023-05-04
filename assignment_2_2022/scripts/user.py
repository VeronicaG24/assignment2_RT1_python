#! /usr/bin/env python

import rospy
import actionlib
import actionlib.msg
import assignment_2_2022.msg
from std_srvs.srv import *
import sys
import select
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Twist
from assignment_2_2022.msg import Position_velocity


def odom_callback(odom_msg):
	
	global pub
	# Get the x, y position and x,y linear velocity
	x = odom_msg.pose.pose.position.x
	y = odom_msg.pose.pose.position.y
	vel_x = odom_msg.twist.twist.linear.x
	vel_y = odom_msg.twist.twist.linear.y
	# Create a Position_velocity message
	pos_vel = Position_velocity()
	# Set the x, y position and x,y linear velocity in the pos_vel message
	pos_vel.x = x
	pos_vel.y = y
	pos_vel.v_x = vel_x
	pos_vel.v_y = vel_y
	# Publish the message already created
	pub.publish(pos_vel)
    
    
def user():
	# Create an action client to connect to the action server
	user = actionlib.SimpleActionClient('/reaching_goal', assignment_2_2022.msg.PlanningAction)
	# Wait for the action server become available
	user.wait_for_server()
	# Repete this code until the rospy node is shut down
	while not rospy.is_shutdown():
		# Display the main menu to the user
		print("Welcome to the Main Menu")
		print("1. Reach a goal")
		print("2. Cancel current goal")
		print("3. Exit")
		# Get user choice
		choice = input("Enter your choiche: ")
		# First case, the user select to reach a goal
		if choice == '1':
			# Get the target coordinates from the user
			pos_x = float(input("Enter target coordinates x: "))
			pos_y = float(input("Enter target coordinates y: "))
        		# Create a goal message with the target coordinates
			goal = assignment_2_2022.msg.PlanningGoal()
			goal.target_pose.pose.position.x = pos_x
			goal.target_pose.pose.position.y = pos_y
			# Send the goal to the action server
			user.send_goal(goal)
		# Second case, the user select to cancel the current goal
		elif choice == '2':
			# If there is an active goal, cancel it
			if user.get_state() == actionlib.GoalStatus.ACTIVE:
				user.cancel_goal()
				print("Goal cancelled!")
			else:
			# If there is no active goal, display a message
				print("No active goal to cancel")
		# Third case, the user want to quit
		elif choice == '3':
			# Shut down the rospy node
			rospy.signal_shutdown("Exiting")
		# If the user choice is invalid, display an error message
		else:
			print("Invalid selection")
            
def main():
	# Initialize the rospy node
	rospy.init_node('user')
	# Define a global publisher to publish the Position_velocity message
	global pub
	pub = rospy.Publisher("/position_velocity", Position_velocity, queue_size = 1)
	# Define a subscriber which listens to the Odometry message and calls the odom_callback function
	sub = rospy.Subscriber('/odom', Odometry, odom_callback)
	# Call the user function
	user()  	


if __name__ == '__main__':
    main()
