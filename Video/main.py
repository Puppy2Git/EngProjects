import cv2  # Image library
import numpy  # Number Library
import os #File Library
import random #Random Library
import math# meth
import time#Za warldo

# define names of each possible ArUco tag OpenCV supports
ARUCO_DICT = {
	"DICT_4X4_50": cv2.aruco.DICT_4X4_50,
	"DICT_4X4_100": cv2.aruco.DICT_4X4_100,
	"DICT_4X4_250": cv2.aruco.DICT_4X4_250,
	"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
	"DICT_5X5_50": cv2.aruco.DICT_5X5_50,
	"DICT_5X5_100": cv2.aruco.DICT_5X5_100,
	"DICT_5X5_250": cv2.aruco.DICT_5X5_250,
	"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
	"DICT_6X6_50": cv2.aruco.DICT_6X6_50,
	"DICT_6X6_100": cv2.aruco.DICT_6X6_100,
	"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
	"DICT_7X7_50": cv2.aruco.DICT_7X7_50,
	"DICT_7X7_100": cv2.aruco.DICT_7X7_100,
	"DICT_7X7_250": cv2.aruco.DICT_7X7_250,
	"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
	"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
	"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
	"DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
	"DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
	"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}
#The elbow's connected to the w h a t bone
Markers_names = {
    1 : "Elbow",
    2 : "Joint",
    3 : "forearm",
    69 : "nice"
    }
vid = cv2.VideoCapture(0)#Grabs the camera
ret, frame = vid.read()#Grabs the ret and the frame (ret is useless)
    
markers = []
#Does that marker thing class to store values with ease
class marker:
    def __init__(self,mID,posX,posY):#When being created
        self.mID = mID#Id
        self.posX = posX#Center X pos
        self.posY = posY#Center Y pos
        self.timer = time.time()# time when created
        self.name = "w h a t"#if it is an invalid marker #
        if (mID in Markers_names.keys()):#if it is in the markers
            self.name = Markers_names[mID]#YES YES YES YES YES
        
    #Updates timer
    def updatetimer(self):
        self.timer = time.time()
    #update position
    def updatepos(self,iX,iY):
        self.posX = iX
        self.posY = iY

#Used to determin if marker is already in array
def in_markers(minput):
    isin = None#not in the list
    for i in range(len(markers)):#Fine I'll check again
        if (markers[i].mID == minput):#I doubt it's going to be in
            isin = i#Oh S**t it is 
    return isin#final answers


#scraps the dead markers off of the code
def cleanup_deadmarkers():
    global markers#Getting markers
    delay = 1#Delay to kill markers
    markerstoKill = []#List of markers to kill
    for i in range(len(markers)):#through all markers
        if(time.time() - markers[i].timer >= delay):#if they are too small
            markerstoKill.append(i)#add to the death note
    for tha in markerstoKill:#light
        try:#do
            del markers[tha]#I'll take a potato chip, AND EAT IT
        except:#Light got shot
            None#lmao

#Draws funny lines lamo
def drawfunnylineslmao():
    global markers#Getting markers
    global frame#Getting frame to draw to
    for make in markers:
        cv2.circle(frame, (make.posX, make.posY), 4, (0, 0, 255), -1)
    if (len(markers) == 1 or len(markers) == 0):#If there is not enough for a line
        None#Nothing
    elif (len(markers) == 2):#If there is only 2 markers
        cv2.line(frame,(markers[0].posX,markers[0].posY),(markers[1].posX,markers[1].posY),(0,255,255))
    else:#Otherwise if there are 2+
        for i in range(len(markers)):#Through all markers
            if (i == len(markers)-1):#If it is the last marker
                cv2.line(frame,(markers[i].posX,markers[i].posY),(markers[0].posX,markers[0].posY),(0,255,255))
            elif (i != 0):#if it is not the first marker
                cv2.line(frame,(markers[i].posX,markers[i].posY),(markers[i+1].posX,markers[i+1].posY),(0,255,255))
            else:#If it is the first marker
                cv2.line(frame,(markers[i].posX,markers[i].posY),(markers[1].posX,markers[1].posY),(0,255,255))

#Draws the names lmao
def lmaonameslmao():
    global markers#Markers again
    for thang in markers:#Get things in thing
        cv2.putText(frame, "Name: {0}  Pos: ({1},{2})".format(thang.name,thang.posX,thang.posY),( thang.posX, thang.posY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)


while True:# yes.
    #Choosing which marker to look for
    arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT["DICT_4X4_100"])
    #Def perameters
    arucoParams = cv2.aruco.DetectorParameters_create()
    #Looking for all markers
    (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)
    # was marker found
    if len(corners) > 0:
        # flatten the ArUco IDs list
        ids = ids.flatten()
        #loop over the detected ArUCo corners
        for (markerCorner, markerID) in zip(corners, ids):
            # extract the marker corners (which are always returned in
            #top-left, top-right, bottom-right, and bottom-left order)
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners#Grabbing corners from list
            #convert each of the (x, y)-coordinate pairs to integers
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))
            # draw the bounding box of the marker
            '''
            cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
            cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
            cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
            cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)
            '''
            # compute and draw the center (x, y)-coordinates of the ArUco
            
            cX = int((topLeft[0] + bottomRight[0]) / 2.0)#Center point X
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)#Center point Y
            #Looking to see if there are in markers
            mak = in_markers(markerID)
            if (mak != None):#If they are
                markers[mak].updatetimer()#update the timer
                markers[mak].updatepos(cX,cY)#Update the pos
            else:#Otherwise
                if (markerID in Markers_names.keys()):#if it is in the markers
                    markers.append(marker(markerID,cX,cY))#Create a new one
            #Write marker's ID ||Prob gonna del later
            

    drawfunnylineslmao()#lmao
    lmaonameslmao()#lmao x 2
    #Showing the current frame
    cv2.imshow("frame",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):#Exits if the q key is pressed
        break
    cleanup_deadmarkers()#Clean up the dead markers
    ret, frame = vid.read()#Getting new frame and ret
    
#Outside of while loop
vid.release()#Releases camera from application
cv2.destroyAllWindows()#Kill all windows