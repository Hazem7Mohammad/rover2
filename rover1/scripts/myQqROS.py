#import libraries
import cv2
from pyzbar import pyzbar

import rospy
import numpy as np
from geometry_msgs.msg import Pose2D
from std_msgs.msg import Int16


#---------- Set Topics and Node names ------------------------
publish_topic1 = 'pose'
subscribe_topic1 = 'flag'
node1 = 'QR_node'
Flag = False



#------------- Initiate the node and set the publisher--------------------------
rospy.init_node(node1, anonymous=False) # Initiate a node named in the parameter "node1"
pub_pos= rospy.Publisher(publish_topic1 ,Pose2D, queue_size=10) 
# set "pub_pose" as publisher to the topic saved in parameter "publish_topic1"

#------------------- Flag used to exit the code as "ESC"-------------------
def changeFlag(status):
    if (status.data == 1) or (status.data == 2):  # close on ESC key
        global Flag # global : to access the global variable "Flag"
        Flag = True
        rospy.loginfo(Flag) # Print the Flag
        
#----------------------------------------------------------------------

r = rospy.Rate(10)


def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:

        #------------- Extract center, dimension,area and bounding polygon-----------
        x, y , w, h = barcode.rect #extracting the satarting point, width & hight
        Cx = x + (w/2) # Calculate center in x axis
        Cy = y + (h/2) # Calculate center in y axis
        area = w*h # Calculate the area
        pts = np.array([barcode.polygon],np.int32) # extract the polygon and save it as array
        pts = pts.reshape ((4,1,2)) # reshape it in a way acceptable by "polylines"
        #------------------------------------------------------------------------


        # ---- Decode the information from the QR code and draw a rectangle around it----
        barcode_info = barcode.data.decode('utf-8') #extract the text
        cv2.circle(frame, (Cx,Cy), radius=0, color=(0, 0, 255), thickness=5)
        # "rectangle" doesnt draw tilted rectangle so we us "polylines" instead
        cv2.polylines(frame,[pts],True,(255,0,255),5)
        #------------------------------------------------------------------------


        # ------Add the decoded information as a text on top of the rectangle-------
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 0.9, (0, 0, 255), 2)
        #--------------------------------------------------------------------------
        

        # -----------Save the extracted information into a text document----------
        # with open("barcode_result.txt", mode ='w') as file:
        #     file.write("Recognized Barcode:" + barcode_info)
        #----------------------------------------------------------------------------
                
                
        # ---------------------------- Publish data-------------------------------
        position = Pose2D()
        position.x = Cx
        position.y = Cy
        position.theta = area #use theta index in Pose2D message to send the area
        pub_pos.publish(position) # publish the message "position"
        print (position)
        #----------------------------------------------------------------------------
        rospy.Subscriber(subscribe_topic1, Int16, changeFlag)
        r.sleep()
        # rospy.spin()
	    #keeps your node from exiting until the node has been shutdown

    return frame  


def main():
    # ---------- Turn the camera on (0: built in camera/ 1: usb camera)-------------
    camera = cv2.VideoCapture(1)
    camera.set(3,640) # Set the camera to 640x480 bcause the threshold values set based->
    camera.set(4,480) # <- on that and if the camera changed, it may has other resolution
    ret, frame = camera.read() #ret: true if the frame is available /frame: image array
    #-------------------------------------------------------------------------------
   

    # -------- Keep running the decoding function until "ESC" is pressed-----------
    while ret:
        ret, frame = camera.read()
        frame = read_barcodes(frame)
        cv2.imshow('Barcode/QR code reader', frame)
        if (cv2.waitKey(1) & 0xFF == 27) or Flag :
            break
    #---------------------------------------------------------------------------------


    # ------------- Close the camera and all windows -------------------------------
    camera.release()
    cv2.destroyAllWindows()
    #----------------------------------------------------------------------------------

if __name__ == '__main__':
    main()