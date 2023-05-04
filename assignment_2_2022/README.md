# Assignment 2
_Massimo Carlini s4678445_
## Description of the assignment
The aim of this assignment is to develop three node starting from the package assignment_2_2022 that is provided in this ghitub repository https://github.com/CarmineD8/assignment_2_2022 that provides an implementation of an action server that moves a robot in the environment by implementing the bug0 algorithm. To reach this goal we need to implement three nodes:
1. A node that implements an action client, allowing the user to set a target (x, y) or to cancel it. The node also publishes the robot position and velocity as a custom message (x,y, vel_x, vel_z), by relying on the values published on the topic /odom.
2. A service node that, when called, prints the number of goals reached and cancelled.
3. A node that subscribes to the robot's position and velocity (using the custom message) and prints the distance of the robot from the target and the robot's average speed.

## Node implemented and pseudocode
Inside the scripts folder we can see that there are six nodes in total, three of them have been provided in the package, the remaining nodes are the nodes that I have implemented.
* `bug_as.py`: the node of the action server that makes calls to move the robot to the desired position.
* `go_to_pint_service.py`: the node that will advance the robot to the desired point.
* `wall_follow_service.py`: the node that make the robot avoid obstacles.

The following nodes are the ones I created:
* `user.py`: is the action client node where the user is asked to choose one of 3 options:
	* Enter the x,y coordinates for the robot to reach.
	* Cancel the coordinates that the robot must reach, thus interrupting its journey.
	* Quit the execution of the program.

	Then, based on the settings of the /odom topic, it publishes the robot position and velocity as a custom message on the /Position velocity subject. 

	Here is the pseudocode of this node:

	```sh
	odom_callback(odom_msg)
		- Get the x, y position and x,y linear velocity from the Odometry message
		- Create a Position_velocity message
		- Set the x, y position and x,y linear velocity in the pos_vel message
		- Publish the pos_vel message

	user()
		- Create an action client to connect to the action server
		- Wait for the action server become available
		- Repete this code until the rospy node is shut down
			- Display the main menu to the user
			- Get user choice
				- If the user choice is to reach a goal
					- Get the target coordinates from the user
					- Create a goal message with the target coordinates
					- Send the goal to the action server
				- If the user choice is to cancel the current goal
					- If there is an active goal, cancel it
					- If there is no active goal, display a message
				- If the user choice is to quit
					- Shut down the rospy node
				- If the user choice is invalid
					- Display an error message
	main()
		- Initialize the rospy node
		- Define a global publisher to publish the Position_velocity message
		- Define a subscriber which listens to the Odometry message and calls the odom_callback function
		- Call the user function
	```
* `goal.py`: node which prints the count of successful goal reached and cancelled goals.
* `print.py`: node that prints the robot's distance from its target and average speed, which it obtains by subscribing to the /Position_velocity topic with a custom message. The frequency at which the information is published can be set via a parameter in the launch file.

## How to install and run
* Install the xterm library to launch the user console and see the information that I explained before. This can be done running on terminal the following code:
	```sh 
	sudo apt-get install xterm
	```
* Now we are able to run the master:
	```sh
	roscore &
	```
* Now we can compile the module going inside the **ROS** directory and running
	```sh 
	catkin_make
	```
* Finally we are able to compile and run the application by running this line:
	```sh 
	roslunch assignment_2_2022 assignment1.launch
	```
## User guide
Once the program has run, 2 screens will appear where it is possible to see the robot and the world around it:
* **Rviz**: it is a ROS tool mainly used for debugging.
* **Gazebo**: allows the 3D view of the robot and the world including the obstacles to avoid.
Furthermore, 2 windows will open with which the user can interact with the user to make the robot move and see information about it.


## Possible improvements
Is it possible to make some improvement on this project:
* In the menu selection is possible to close all the windows, also the gazebo and rviz windows, when the userchoose to exit to the program.
