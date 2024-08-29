#!/usr/bin/env python
from math import sqrt
from numbers import Real
from turtle import pos
import cv2
import rospy
import numpy as np
from pyzbar.pyzbar import decode
from geometry_msgs.msg import Pose2D
#include <std_msgs/Int16.h>
from std_msgs.msg import Int16

# flag = 0 

#img = cv2.imread('1.png')
cap = cv2.VideoCapture(1)
# cap = cap.flip(1)

cap.set(3,640)
cap.set(4,480)

# def changeFlag(closed):
#     rospy.loginfo(closed.data)
#     if closed.data == 1:  # close on ESC key
#         rospy.loginfo(closed.data)
#         cv2.destroyAllWindows()
        


while True:

    success, img = cap.read()
    #img=cv2.flip(img0,1)
    rospy.init_node('position_node', anonymous=False)
    pub_pos= rospy.Publisher('pose',Pose2D, queue_size=10)
    # rospy.Subscriber('flag', Int16, changeFlag)
    # rospy.spin()
    for barcode in decode(img):
        myData = barcode.data.decode('utf-8')
        #print(myData)
        pts = np.array([barcode.polygon],np.int32)
        pts = pts.astype(int).reshape(-1, 2)
        x=0
        y=0
        for j in range(4):
            x=(pts[j,0]+x)
            y=(pts[j,1]+y)
        x=x/4
        y=y/4
        line1x=abs(pts[3,0]-pts[2,0])
        line2x=abs(pts[2,0]-pts[1,0])
        line1y=abs(pts[3,1]-pts[2,1])
        line2y=abs(pts[2,1]-pts[1,1])
        line1=sqrt((line1x*line1x)+(line1y*line1y))
        line2=sqrt((line2x*line2x)+(line2y*line2y))
        area=line1*line2
        position = Pose2D()
        position.x = 640-x
        position.y = y
        position.theta = area
        pub_pos.publish(position)
        print (position)
        cv2.polylines(img,[pts],True,(255,0,255),5)
        pts2 = barcode.rect
        cv2.circle(img, ((x.astype(int)),y.astype(int)), radius=0, color=(0, 0, 255), thickness=5)
        cv2.putText(img,myData,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,(255,0,255),2)
        # cv2.imshow("QRCODEscanner2", img) 

    cv2.imshow('Result',img)
    # cv2.waitKey(1)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:  # close on ESC key
        cv2.destroyAllWindows()
        break