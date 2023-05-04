/**
*\file subscriber.cpp
*\brief ROS node for counting goals reached and deleted
*\author Veronica Gavagna
*\version 0.1
*\date 26/01/2023
**/

#include <ros/ros.h>
#include <unistd.h>
#include <sstream>
#include <iostream>
#include <cmath>
#include "follow_goal/pos_vel.h"
#include <follow_goal/PlanningActionGoal.h>

using namespace std;

// global variables for position and velocity of the robot, coordinates of the goal
float x_pos, y_pos, x_vel, y_vel, x_goal, y_goal;
// global variables for distance from the goal and average speed
float dist_goal, average_vel;
// global variable for frequency rate
double frequency;
// Subscribers
ros::Subscriber sub1;
ros::Subscriber sub2;


/*#############################################
# 
# Get position and velocity of the robot
# from custom topic pos_vel
# 
##############################################*/
void pos_vel_callback(const follow_goal::pos_vel::ConstPtr& msg) {

	x_pos = msg->x_pos;
	y_pos = msg->y_pos;
	x_vel = msg->x_vel;
	y_vel = msg->y_vel;
	
}


/*#############################################
# 
# Get coordinates of the goal 
# 
##############################################*/
void goal_callback(const follow_goal::PlanningActionGoal::ConstPtr& msg) {	
	
	x_goal = msg->goal.target_pose.pose.position.x;
	y_goal = msg->goal.target_pose.pose.position.y;
	
}


/*#############################################
# 
# Compute distance from the goal and average
# speed of the robot
# Print the results 
# 
##############################################*/
void get_dist_vel_from_goal() {

	dist_goal = sqrt(((x_goal - x_pos)*(x_goal - x_pos)) + ((y_goal - y_pos)*(y_goal - y_pos)));
	average_vel = sqrt((x_vel*x_vel) + (y_vel*y_vel));
	
	
	cout << "Distance from goal: " << dist_goal << "\t\tAverage speed: " << average_vel << "\n";
	
}


/*###############################################
# 
# Manage ROS init, NodeHandle, rate frequency,
# subscriber for position and velocity,
# subscriber for goal coordinates, and calculation
# of distance from the goal and average speed
# 
################################################*/
int main(int argc, char **argv) {
	
	//init
	ros::init(argc, argv, "subscriber_robot");
	
	//NodeHandle for main access point to communications with ROS system
	ros::NodeHandle n;
	
	// set rate frequency
	ros::param::get("frequency", frequency);
	ros::Rate rate(frequency);
	
	while(ros::ok()) {
		// Subscriber for position and velocity
		sub1 = n.subscribe("/robot_info", 1, pos_vel_callback);
		
		// Subscriber for goal coordinates
		sub2 = n.subscribe("/reaching_goal/goal", 1, goal_callback);
		
		// calculation of distance from the goal and average speed
		get_dist_vel_from_goal();
		
		rate.sleep();
		ros::spinOnce();
	}
	
	return 0;
}
