import cv2
import math
import numpy


cl_upper = [0,0,0]
cl_lower = [0,0,0]
vid = cv2.VideoCapture(0)

ret, frame = vid.read()
cv2.namedWindow("Slooders")
cv2.createTrackbar("Upper Hue", "Slooders", 0, 128, lambda x: None)
cv2.createTrackbar("Lower Hue", "Slooders", 0, 128, lambda x: None)
cv2.createTrackbar("Upper Sat", "Slooders", 0, 128, lambda x: None)
cv2.createTrackbar("Lower Sat", "Slooders", 0, 128, lambda x: None)
def tbarpos(name, win):
    return cv2.getTrackbarPos(name,win)
hsv_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)


while True:


    cv2.imshow("Frame",frame)
    cv2.imshow("HSV",hsv_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): #Exits if the q key is pressed
        break
    ret, frame = vid.read()
    hsv_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
