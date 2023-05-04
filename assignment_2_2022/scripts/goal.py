#! /usr/bin/env python

import rospy
from assignment_2_2022.srv import goal_srv, goal_srvResponse
import assignment_2_2022
import assignment_2_2022.msg
import actionlib
import actionlib.msg

goals_reached = 0
goals_cancelled = 0
# Function to handle the goal service
def handle_goal_srv(request):
	global goals_reached
	global goals_cancelled
	# Get the current number of goals reached and cancelled
	goals_reached = goals_reached
	goals_cancelled = goals_cancelled
	# Print the current number of goals reached and cancelled
	print("Goals reached: {}".format(goals_reached))
	print("Goals cancelled: {}".format(goals_cancelled))
	# Create and return the response for the goal service
	response = goal_srvResponse()
	response.goals_reached = goals_reached
	response.goals_cancelled = goals_cancelled
	return response
 # Function to update the goals reached and cancelled
def update_goals_status(msg):
	global goals_reached
	global goals_cancelled
	# Get the status of the current goal from the message
	status = msg.status.status
	# Update the number of goals reached or cancelled based on the status
	if status == 3:
		goals_reached += 1
	elif status == 2:
		goals_cancelled += 1

if __name__ == '__main__':
	# Initialize the node
	rospy.init_node('goal')
	# Create a service server
	goal_srv = rospy.Service('goal', goal_srv, handle_goal_srv)
	# Create a subscriber to listen to the goal result topic
	sub_goal = rospy.Subscriber('/reaching_goal/result', assignment_2_2022.msg.PlanningActionResult, update_goals_status)
	# Keep the node running
	rospy.spin()

