#! /usr/bin/python
import rospy
import math

import traceback
import sys
import simple_navigation_goals


import subprocess 


if __name__ == "__main__":
  try:
    rospy.init_node("test_scenario")
    rospy.loginfo("SimpleNavigationGoals Initialization")
    nav_goals = simple_navigation_goals.SimpleNavigationGoals()
    rospy.loginfo("Initializations done")

    # What to do if shut down (e.g. ctrl + C or failure)
    rospy.on_shutdown(nav_goals._shutdown)

    # while True:
    #   # rospy.loginfo("Go to 0.3, 0, 0 deg")
    #   # if not (nav_goals.go_to(0.3, 0, 0)):
    #   #   break
    #   rospy.loginfo("Go to 0.35, -0.2, 0 deg")
    #   if not (nav_goals.go_to(0.2, -0.5, 0)):
    #     break
    #   # rospy.loginfo("Go to -5, -5.5, 0 deg")
    #   # if not (nav_goals.go_to(0, 8, 0)):
    #   #   break
    #   # rospy.loginfo("Go to 8, 0, 180 deg")
    #   # if not (nav_goals.go_to(8, 0, 0)):
    #   #   break   

    # (nav_goals.go_to(0.3, 0, 45))
    # (nav_goals.go_to(0.6, 0, -45))


    rospy.loginfo("Go to 0.5, 0, 30 deg")
    nav_goals.go_to(0.5, -0.5, -30)
    # if (nav_goals.go_to(0.5, -0.5, -30)):
    #   subprocess.call(['python','test.py'])
    # rospy.loginfo("Go to 0.5, -0.5, -90 deg")
    # if (nav_goals.go_to(0.5, 1.0, 30)):
    #   subprocess.call(['python','test.py'])

# myQqROS

    rospy.spin()
  except rospy.ROSInterruptException:
    rospy.logerr(traceback.format_exc())

  rospy.loginfo("test terminated.")