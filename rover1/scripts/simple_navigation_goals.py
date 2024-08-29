#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import numpy as np
from tf.transformations import quaternion_from_euler

class SimpleNavigationGoals:

    def __init__(self):
        pass

    def go_to(self, x, y, yaw):
        client = None
        client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
        client.wait_for_server()

        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()

        roll=0
        pitch=0
        yaw = (yaw*3.14)/180 # convert from degree to radian
        
        quat = quaternion_from_euler (roll, pitch, yaw)

        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y
        goal.target_pose.pose.position.z = 0
        goal.target_pose.pose.orientation.x = quat[0]
        goal.target_pose.pose.orientation.y = quat[1]
        goal.target_pose.pose.orientation.z = quat[2]
        goal.target_pose.pose.orientation.w = quat[3]

        client.send_goal(goal)
        wait = client.wait_for_result()

        if not wait:
            rospy.logerr("Action server not available!")
            rospy.signal_shutdown("Action server not available!")
        else:
            rospy.loginfo("Done")
            return client.get_result()




    def _shutdown(self):
        rospy.signal_shutdown("Shutdown!")