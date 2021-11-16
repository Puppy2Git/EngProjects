import cv2  # Image library
import numpy  # Number Library
import os #File Library
import random #Random Library
import math# meth
import time#Za warldo
from pysine import sine

#angles
angles = 0

#Json file read stuff
#Target
#   Goal, 0 = extension, 1 = contraction, 2 = both
#   


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
    1 : "Shoulder",
    2 : "Elbow",
    3 : "Forearm",
    }
vid = cv2.VideoCapture(0)#Grabs the camera
ret, frame = vid.read() #Grabs the ret and the frame (ret is useless)
    
markers = []
#Does that marker thing class to store values with ease
class marker:
    """"This is a marker class used to define new markers\n
    marker(The marker's ID, The X position, The Y position)\n
    Ex:\n
    For a new marker with an ID of 1, and Position of (50,23)\n
    >>> boo = markers(1,50,23)"""
    def __init__(self,mID,posX,posY): #When being created
        self.mID = mID #Id
        self.posX = posX #Center X pos
        self.posY = posY #Center Y pos
        self.timer = time.time() # time when created
        self.name = "w h a t" #if it is an invalid marker #
        if (mID in Markers_names.keys()): #if it is in the markers
            self.name = Markers_names[mID] #YES YES YES YES YES
        
    #Updates timer
    def updatetimer(self):
        """Called to update the time to the current time\n
        Ex:\n
        >>> marker.updatetimer()"""
        self.timer = time.time()
    #update position
    def updatepos(self,iX,iY):
        """Called to update the position of the marker\n
        Ex:\n
        The marker has moved to (50,100)\n
        >>> marker.updatepos(50,100)
        """
        self.posX = iX
        self.posY = iY

#takes the angle and gives feedback
def feedback(target):
    """This takes a given target range and plays a predefined sine frequency\n
    feedback(target angle)\n
    Ex:\n
    For a target angle of 50\n
    >>> feedback(50)"""
    global angles
    if angles < target:
        sine(330, 0.1)
    else:
        sine(500, 0.1)
        


#Used to determin if marker is already in array
def in_markers(minput):
    """This returns whether the given ID is in markers\n
    in_markers(Marker ID)\n
    Ex:\n
    To see if marker ID 3 is in the markers list\n
    >>> in_markers(3)"""
    isin = None #not in the list
    for i in range(len(markers)): #Fine I'll check again
        if (markers[i].mID == minput): #I doubt it's going to be in
            isin = i #Oh S**t it is 
    return isin #final answers

#takes the angle and gives feedback


#scraps the dead markers off of the code
def cleanup_deadmarkers():
    """This is called to destroy markers who's timer extend longer than a predetermined time\n
    cleanup_deadmarkers()\n
    This should just be referenced in the while loop only"""
    global markers #Getting markers
    delay = 1 #Delay to kill markers
    markerstoKill = [] #List of markers to kill
    for i in range(len(markers)): #through all markers
        if(time.time() - markers[i].timer >= delay): #if they are too small
            markerstoKill.append(i) #add to the death note
    for tha in markerstoKill: #light
        try: #do
            del markers[tha] #I'll take a potato chip, AND EAT IT
        except: #Light got shot
            None #lmao

#Draws funny lines lamo
def drawfunnylineslmao():
    """This is used to draw the lines between each marker\n
    drawfunnylineslmao()\n
    This should just be referenced in the while loop only"""
    global markers #Getting markers
    global frame #Getting frame to draw to
    for make in markers:
        cv2.circle(frame, (make.posX, make.posY), 4, (0, 0, 255), -1)
    if (len(markers) == 1 or len(markers) == 0): #If there is not enough for a line
        None #Nothing
    elif (len(markers) == 2): #If there is only 2 markers
        cv2.line(frame,(markers[0].posX,markers[0].posY),(markers[1].posX,markers[1].posY),(0,255,255))
    else: #Otherwise if there are 2+
        for i in range(len(markers)): #Through all markers
            if (i == len(markers)-1): #If it is the last marker
                cv2.line(frame,(markers[i].posX,markers[i].posY),(markers[0].posX,markers[0].posY),(0,255,255))
            elif (i != 0): #if it is not the first marker
                cv2.line(frame,(markers[i].posX,markers[i].posY),(markers[i+1].posX,markers[i+1].posY),(0,255,255))
            else: #If it is the first marker
                cv2.line(frame,(markers[i].posX,markers[i].posY),(markers[1].posX,markers[1].posY),(0,255,255))
        

#Returns distance between 2 points
def calculatedistance(x1,x2,y1,y2):
    """This is used to calculate the distance between 2 given points\n
    calculatedistance(X position 1, X posiiton 2, Y position 1, Y position 2)\n
    Ex:\n
    To find the distance between (50,100) and (25, 120)\n
    >>> calculatedistance(50,25,100,120)"""
    return (math.sqrt(math.pow((x2-x1),2)+math.pow((y2-y1),2)))

#Uses the global markers to get le angles and set the global angle
def calculateangle():
    """This is used to calculated the angles between all markers\n
    calculateangles()\n
    This should just be referenced in the while loop only"""
    global markers
    global angles
    temp1 = []
    final = 0
    if (len(markers) == 3):
        for i in range(len(markers)):
            temp1.append(markers[i])
        temp1.sort(key=lambda x: x.mID, reverse=True)
        #So now it is time to find angles
        #0 is E
        #1 is J
        #2 is F
        FtJ = calculatedistance(temp1[2].posX,temp1[1].posX,temp1[2].posY,temp1[1].posY)
        JtE = calculatedistance(temp1[1].posX,temp1[0].posX,temp1[1].posY,temp1[0].posY)
        FtE = calculatedistance(temp1[2].posX,temp1[0].posX,temp1[2].posY,temp1[0].posY)
        
        final = math.acos((FtJ**2 + JtE**2 - FtE**2) / (2 * FtJ * JtE))
    angles = final * 180 / math.pi
        

            
#Draws the names lmao
def lmaonameslmao():
    """This is used to draw the names of each marker\n
    lmaonameslmao()\n
    This should just be referenced in the while loop only"""
    global angles
    global markers #Markers again
    for thang in markers: #Get things in thing
        if (thang.mID != 2):
            cv2.putText(frame, "Name: {0}".format(thang.name),( thang.posX, thang.posY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        else:
            cv2.putText(frame, "Name: {0} Angle: ({1})".format(thang.name,angles),( thang.posX, thang.posY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)

while True: #yes.
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
            (topLeft, topRight, bottomRight, bottomLeft) = corners #Grabbing corners from list
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
            
            cX = int((topLeft[0] + bottomRight[0]) / 2.0) #Center point X
            cY = int((topLeft[1] + bottomRight[1]) / 2.0) #Center point Y
            #Looking to see if there are in markers
            mak = in_markers(markerID)
            if (mak != None): #If they are
                markers[mak].updatetimer() #update the timer
                markers[mak].updatepos(cX,cY) #Update the pos
            else: #Otherwise
                if (markerID in Markers_names.keys()): #if it is in the markers
                    markers.append(marker(markerID,cX,cY)) #Create a new one
            #Write marker's ID ||Prob gonna del later

    calculateangle()
    drawfunnylineslmao() #lmao
    lmaonameslmao() #lmao x 2
    #Showing the current frame
    cv2.imshow("frame",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): #Exits if the q key is pressed
        break

    print("Angle: {0}     ".format(int(angles)), end= "\r")
    target = 90
    feedback(target) #looks and compares target to the real time arm angle
    cleanup_deadmarkers() #Clean up the dead markers
    ret, frame = vid.read() #Getting new frame and ret
    target = 90
    feedback(target) #looks and compares target to the real time arm angle
    
#Outside of while loop
vid.release() #Releases camera from application
cv2.destroyAllWindows() #Kill all windows
