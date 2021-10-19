import cv2  # Image library
import numpy  # Number Library
import os #File Library
import random #Random Library


vid = cv2.VideoCapture(0)#Grabs the camera
ret, image = vid.read()#Grabs the ret and the frame
grayFrame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
while True:
    
    cv2.imshow("winname",grayFrame)#Shows the frame
    if cv2.waitKey(1) & 0xFF == ord('q'):#Exits if the q key is pressed
        break


vid.release()#Releases camera from application
cv2.destroyAllWindows()#Kill all windows