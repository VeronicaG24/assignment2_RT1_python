/**
*\file publisher.cpp
*\brief ROS node for counting goals reached and deleted
*\author Veronica Gavagna
*\version 0.1
*\date 26/01/2023
**/

#include <ros/ros.h>
#include <unistd.h>
#include <sstream>
#include <iostream>
#include "nav_msgs/Odometry.h"
#include "follow_goal/pos_vel.h"


// global variables for position and velocity of the robot
float x_pos, y_pos, x_vel, y_vel;

// publisher 
ros::Publisher pub;


/*###############################################
# 
# Get position and velocity of the robot
# from topic odom
# Public them to custom topic pos_vel
# 
################################################*/
void pos_vel_callback(const nav_msgs::Odometry::ConstPtr& msg) {
	ROS_INFO("\nRobot subscriber@[%f, %f, %f, %f]\n", msg->pose.pose.position.x, msg->pose.pose.position.y, msg->twist.twist.linear.x, msg->twist.twist.linear.y);	
	
	//Subscribe position and velocity from topic odom
	x_pos = msg->pose.pose.position.x;
	y_pos = msg->pose.pose.position.y;
	x_vel = msg->twist.twist.linear.x;
	y_vel = msg->twist.twist.linear.y;
	
	//public position and velocity to custom topic
	follow_goal::pos_vel pos_vel;
	pos_vel.x_pos = x_pos;
	pos_vel.y_pos = y_pos;
	pos_vel.x_vel = x_vel;
	pos_vel.y_vel = y_vel;
	
	pub.publish(pos_vel);
}


/*###############################################
# 
# Manage ROS init, NodeHandle, subscriber,
# and publisher
# 
################################################*/
int main(int argc, char **argv) {
	
	//init
	ros::init(argc, argv, "publisher_robot");
	
	//NodeHandle for main access point to communications with ROS system
	ros::NodeHandle n;
	
	// Subscriber
	ros::Subscriber sub = n.subscribe("/odom", 1, pos_vel_callback);
	
	// Publisher
	pub = n.advertise<follow_goal::pos_vel>("/robot_info", 10);
	
	sleep(1);
	ros::spin();
	
	return 0;
	
}
