#!/usr/bin/env python
import imghdr
import rospy 
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import sys
from math import sqrt
from numbers import Real
import numpy as np
from pyzbar.pyzbar import decode
from geometry_msgs.msg import Pose2D

bridge=CvBridge()
cap = cv2.VideoCapture(0)
def image(image_sub):
    while True:
        success, img = cap.read()
        image_sub.publish(bridge.cv2_to_imgmsg(img, "bgr8"))
        k = cv2.waitKey(1) & 0xFF
        if k == 27:  # close on ESC key
            cv2.destroyAllWindows()
            break



def main(args):
    rospy.init_node('image_converter', anonymous=True)
    image_sub=rospy.Publisher("/usb_cam/image_raw", Image, queue_size=10)
    image(image_sub)

if __name__=='__main__':
    main(sys.argv)