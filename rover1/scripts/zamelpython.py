#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import Int16
from geometry_msgs.msg import Pose2D
import cv2
import numpy as np
cap = cv2.VideoCapture(0)
Trackbars = True
# open usb camera , use 0 for builtin camera
# make it "True" to show sliders for testing
flag = True # the flag is to create the trackbars only once in the loop
#-----------------------------Tennis ball values-----------------------
LHue = 30
UHue = 51
LSat = 105
USat = 255
LVal = 63
UVal = 255
lThresh = 100 # for canny filter
uThresh = 200 # for canny filter
#---------------------------------------------------------------------------
# each callback change its related value, getTrackbarPos: get te new value from the trackbar
def callback1(Val):
    global LHue
    LHue = cv2.getTrackbarPos('LHue','frame')
def callback2(Val1):
    global UHue
    UHue = cv2.getTrackbarPos('UHue','frame')
    UHue = Val1
def callback3(Val):
    global LSat
    LSat = cv2.getTrackbarPos('LSat','frame')
def callback4(Val):
    global USat
    USat = cv2.getTrackbarPos('USat','frame')
def callback5(Val):
    global LVal
    LVal = cv2.getTrackbarPos('LVal','frame')
def callback6(Val):
        global UVal
        UVal = cv2.getTrackbarPos('UVal','frame')
# ------------------------ create the trackbars
def find_object():
    if (flag):
        cv2.createTrackbar( 'LHue', 'frame', 0,360,callback1)
        cv2.createTrackbar(' UHue', 'frame', 0,360,callback2)
        cv2.createTrackbar( 'LSat', 'frame', 0,255,callback3)
        cv2.createTrackbar( 'USat', 'frame', 0,255,callback4)
        cv2.createTrackbar( 'LVal', 'frame', 0,255,callback5)
        cv2.createTrackbar( 'UVal', 'frame', 0,255,callback6)
        global flag
        flag = False
    else:
        return

#-------------------------Centroid---------------------------------
def get_contour_center(contour):
    M = cv2.moments(contour)
    centroid_x = -1
    centroid_y = -1
    if (M['m00']!=0):
        centroid_x = int(M['m10']/M['m00'])
        centroid_y = int(M['m01']/M['m00'])
    return centroid_x,centroid_y
    
def initiate():
#---------------initiate publisher node named "position_node" to publish int values
    pub_pos= rospy.Publisher('pose',Pose2D, queue_size=10)
    rospy.init_node('position_node', anonymous=False) #False = cant open more than one
    rate = rospy.Rate(10) #10hz
    print("Object Position")
#------------------------------------------------------------------------

    while not rospy.is_shutdown():
#-------------- read from camera and save in variable "frame"--------

        _, frame = cap.read() # "-" means I dont need first variable so it defined as "dash"
        frame = cv2.flip(frame, 1)
        if cv2.waitKey(1) & 0xFF == 27:
        # press "ESC" to quit the program
            cap.release()
            cv2.destroyAllWindows()
#-------------------------------------------------------------------

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
# convert image to hsv
        hsv = cv2.GaussianBlur(hsv, (15,15), cv2.BORDER_DEFAULT)
# and removing noise
        LowerBound = np.array([LHue, LSat, LVal])
        UpperBound = np.array([UHue, USat, UVal])
        mask = cv2.inRange(hsv, LowerBound, UpperBound)
# applying the mask on hsv image (converted frame)
        kernel = np.ones((15,15),np.uint8)
#15 x15 kernal
        openMask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
# openning followed b dilation
        cv2.imshow('mask',openMask)
#
#filtering
#
# create
        _, contours, hierarchy = cv2.findContours(openMask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# find countors and store them in list called "contours", simpple approximation means store corner points only
#RETR_TREE is retrical modes that returns all conturs information about parants, siblings, children, etc
# and store these relationships in variable "hierarchy"
        cv2.drawContours(frame, contours, -1, (0,255,0), 3)
#draw contours over the image variable "frame" ,-1 means draw all
# contours in "contours" list, color (0,255,0)=(B,G,R), 3 is thickness
        black = np.zeros([frame.shape[0], frame.shape[1], 3], 'uint8') #
# create black image with same size of original frame
        maxLength = 5
        minArea = 3500
        centroid_x = 0
        centroid_y = 0
        for c in contours: #go through each contour in the list, one by one and call it the variable c
            area = cv2.contourArea(c)
            if area > minArea:
# check area of each contour, if it is less than minArea then ignore it
                areaRatio = area/minArea
# to check how big the contour area in comparison to min area
                perimeter = cv2.arcLength(c, True)
                ((x,y),radius) = cv2.minEnclosingCircle(c) #find x and y
                cv2.drawContours(frame, [c], -1, (150,250,150), 1) # draw the contour
                x = (int)(x)
                y = (int)(y)
                centroid_x,centroid_y = get_contour_center(c) #f ind centroid
                cv2.circle(frame, (x,y), (int)(radius), (0,0,255), 3) # draw circle
# next 2 lines draw the plus sign
                cv2.line(black, (x,(int)(y-(maxLength*areaRatio))),(x,(int)(y+(maxLength*areaRatio))), (0, 255, 0), 1)
                cv2.line(black, ((int)(x-(maxLength*areaRatio)),y),((int)(x+(maxLength*areaRatio)),y), (0, 255, 0), 1)
        canny = cv2.Canny(openMask, lThresh, uThresh)
# applying canny edge detection on openmask frame
        message = "Tennis Ball"
        cv2.putText(frame, message, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(64,187,179),2)
# -----------showing the frames-----------
        cv2.imshow('frame',frame)
        cv2.imshow("center", black)
        cv2.imshow("Canny", canny)
        if (Trackbars): # if Trackbars True it will generate the trackbars
            find_object()
#----------------prepare the messge to be published------------------
        position = Pose2D()
        position.x = centroid_x
        position.y = centroid_y
        position.theta = 0
# because it is not used
# ----------- Printing on the terminal x and y

        x_message = " x position = %.1f" %centroid_x
        print (x_message)
        y_message = " y position = %.1f" %centroid_y
        print (y_message)
# ----------------- Publishing
        pub_pos.publish(position)
if __name__=='__main__':
    initiate()