#Color by Alexander Garcia S2092733
#Info for json files
#The json file is needed to run
#The json file can add new presets by opening the file and adding them manually,
#It is self explantory



import cv2  # Image library
import numpy  # Number Library
import os #File Library
import random #Random Library

def rgb(r, g, b):  # DUMB function that really only had one purpose!
    return([b, g, r])


temp = os.listdir()#Grabbing all files and folders in dir
myfiles = []
filename = None
for i in range(len(temp)):#Looping through each
    if os.path.isfile(temp[i]):#If it is a file
        if len(str(temp[i])) >= 5:#If it has enough characters
            if str(temp[i])[-4:] == ".jpg":#If the ending is in .jpg
                myfiles.append(temp[i])#Add it to the valid files
filename_valid = False#While false
print("All .jpg files found in directory:")
while filename_valid == False:# 
    for i in range(len(myfiles)):#Loop through all files
        print("({0}) - {1}".format(i,myfiles[i]))#Display all files in the list
    print("Which image would you like to edit? or if you want to use video press -1")#Ask what they would like to edit
    filenumber = input(": ")#Input
    try:#Try
        if (int(filenumber) != -1):
            filename = str(myfiles[int(filenumber)])#To convert to int to grab str from list
        filename_valid = True#Exit the loop
    except IndexError:#If it is not in the array
        for i in range(10):
            print("")
        print("Invalid number")
    except:#If it is not a number
        for i in range(10):
            print("")
        print("That is not a number")

import json
f = open("Alexander_G_data.json")
data = json.load(f)
#Presets Test
#Goal it should ask the user for a list of presets avaible and it should then genearate the windows with the presets
current_presets = data["Presets"]
colors = data["Colors"]
selected_preset = None
valid_preset = False

while valid_preset == False:#While preset is not valid
    print("What preset would you like to use?")
    for i in range(len(list(data["Presets"]))+1):#Through all presets
        if i != len(list(data["Presets"])):#if it is not the 1 + last one
            print("({0}) - {1}".format(i,list(data["Presets"])[i]))#Print from the list
        else:
            print("({0}) - No Presets".format(i))#Otherwise print No preset
    user_preset = input(": ")#Store user input
    try:#If it is an int and in range
        if (int(user_preset) == len(list(data["Presets"]))):#If it is no preset
            valid_preset = True#True
        else:
            selected_preset = data["Presets"][list(data["Presets"])[int(user_preset)]]#If it is a preset
            valid_preset = True
    except IndexError:#If it is out of the list
        print("Number is not in selection")
    except:#If it is not a number
        print("Not a number")


if (filename != None):
    original_image = cv2.imread(filename, 1)  # Color
    grayscale_image_simple = cv2.imread(filename, 0)  # Gray Scale b/c of 0
    grayscale_image = cv2.cvtColor(grayscale_image_simple, cv2.COLOR_GRAY2BGR) # Grayscale image
else:
    vid = cv2.VideoCapture(0)
    ret, image = vid.read()#Grabs the ret and the frame
    thing = numpy.array(image, dtype=numpy.uint8)
    original_image = cv2.cvtColor(thing,cv2.IMREAD_COLOR)
    grayscale_image_simple = cv2.cvtColor(thing,cv2.COLOR_BGR2GRAY)
    grayscale_image = cv2.cvtColor(grayscale_image_simple, cv2.COLOR_GRAY2BGR)
    
image_height = original_image.shape[0]#Image height
image_width = original_image.shape[1]#Image width
image_channels = original_image.shape[2]#Image channels

active_windows = [] # Array that contains all active windows
full_image = None
#My custom window class
class cus_window():
    #Creates a new window given the name which should be the same now that I think about it
    def __init__(self, pos = 0,div = 0, irgb = None, newin = False):
        self.name_window = "Window {0}".format(pos)#Sets the name of the window
        self.newwindow = newin #If there is a window attached to it
        self.pos = pos# sets what position it is in the array
        self.posmin = pos
        self.min = []#Sets the min color sheet divider to nothing
        self.max = []#Sets the max color sheet divider to nothing
        self.inverse = None#Sets the inverse paper to nothing
        self.compaper = None#Sets the complete paper to nothing
        self.paper = numpy.zeros(
    (image_height, image_width, image_channels), numpy.uint8)#Defines the color paper dimentions
        cv2.namedWindow(self.name_window)#Creates a new window
        
        #The "Button" for a new slider and divider
        if (self.pos != 0):#If it is not the first window
            if newin: 
                cv2.createTrackbar("New Divider",self.name_window,1,1,lambda x:self.createnew())#
            else:
                cv2.createTrackbar("New Divider",self.name_window,0,1,lambda x:self.createnew())
            cv2.createTrackbar("Divider",self.name_window,div,255-self.pos,lambda x:generate_image(self.pos))
        else:
            cv2.createTrackbar("Selector",self.name_window,0,2,lambda x:generate_image(-1))
        #The RGB values
        if irgb == None:
            cv2.createTrackbar("R",self.name_window,random.randint(0,255),255,lambda x:self.update_colors(0))
            cv2.createTrackbar("G",self.name_window,random.randint(0,255),255,lambda x:self.update_colors(0))
            cv2.createTrackbar("B",self.name_window,random.randint(0,255),255,lambda x:self.update_colors(0))
        else:
            cv2.createTrackbar("R",self.name_window,irgb[0],255,lambda x:self.update_colors(0))
            cv2.createTrackbar("G",self.name_window,irgb[1],255,lambda x:self.update_colors(0))
            cv2.createTrackbar("B",self.name_window,irgb[2],255,lambda x:self.update_colors(0))
        #Generates the paper first time with the random colors
        self.paper[0:image_height, 0:image_width,
             0:image_channels] = rgb(cv2.getTrackbarPos("R",self.name_window),cv2.getTrackbarPos("G",self.name_window),cv2.getTrackbarPos("B",self.name_window))         
        
    #Handles updating the colors then it redraws the image
    def update_colors(self, reg):
        self.paper[0:image_height, 0:image_width,#Redos the paper
             0:image_channels] = rgb(cv2.getTrackbarPos("R",self.name_window),cv2.getTrackbarPos("G",self.name_window),cv2.getTrackbarPos("B",self.name_window))         
        if reg == 0:
            generate_image(-1)#Tells to redraw
    
    
    
    #Destroys the window and removes from list
    def destroy(self):
        cv2.destroyWindow(self.name_window)
        del active_windows[self.pos]
    
    
    
    
    #When the slider of it's self is nudge
    def nudgeslider(self, direction,slider_pos):
        #True if to update upwards (Checking left)
        #False to update downwards (Chcking right)
        if direction:#If the slider infornt got moved
            if cv2.getTrackbarPos("Divider",self.name_window) >= slider_pos:#if it is to the left of the slider
                cv2.setTrackbarPos("Divider",self.name_window,slider_pos-1)
                if (self.pos != len(active_windows)-1):
                    active_windows[self.pos+1].nudgeslider(direction,cv2.getTrackbarPos("Divider",self.name_window))
        else:#If the slider behind got moved
            if cv2.getTrackbarPos("Divider",self.name_window) <= slider_pos:#if it is to the left of the slider
                cv2.setTrackbarPos("Divider",self.name_window,slider_pos+1)
                if (self.pos != 1):
                    active_windows[self.pos-1].nudgeslider(direction,cv2.getTrackbarPos("Divider",self.name_window))
            
    #returns the trackbarposition
    def get_trackpos(self):
        return cv2.getTrackbarPos("Divider",self.name_window)
    
    #Called when the new slider is created and to increase the min
    def slider_update(self, inc):
        if inc:#If a window was created
            self.posmin += 1
        else:
            self.posmin -= 1
            
        cv2.setTrackbarMin("Divider",self.name_window,self.posmin)
        if (cv2.getTrackbarPos("Divider",self.name_window) < self.posmin):
            cv2.setTrackbarPos("Divider",self.name_window, self.posmin)
        if (self.pos != 1):
                active_windows[self.pos-1].slider_update(inc)
            
    
    #Called when The New Divider is moved
    def createnew(self):
        if (cv2.getTrackbarPos("New Divider",self.name_window) == 1) and not self.newwindow:#To create a new window if there is not already one
            self.newwindow = True
            
            active_windows.append(cus_window(self.pos + 1))
            
            self.posmin = 0
            self.slider_update(True)
        #To destory next window
        elif (cv2.getTrackbarPos("New Divider",self.name_window) == 0) and (self.newwindow == True):
            if ((len(active_windows) - 1) == self.pos + 1):#If it is the last window
                active_windows[self.pos+1].destroy()
                self.newwindow = False
                #cv2.setTrackbarMin("Divider",self.name_window,self.pos-1)
                self.slider_update(False)
            else:
                cv2.setTrackbarPos("New Divider",self.name_window,1)#If there is a window after it to tell it not to delete
        cv2.setTrackbarMax("Selector",active_windows[0].name_window,len(active_windows))
        cv2.setTrackbarPos("Selector",active_windows[0].name_window,0)
        generate_image(-1)

#Major generate function!!!
def generate_image(x):
    global full_image
    #Nudging sliders if it was moved
    if x != -1:
        #Nudging windows if it is the last one
        if x == len(active_windows) - 1 and len(active_windows) != 2:
            active_windows[x-1].nudgeslider(False,cv2.getTrackbarPos("Divider","Window {0}".format(x)))
        elif x == 1 and len(active_windows) != 2:#If
            active_windows[x+1].nudgeslider(True,cv2.getTrackbarPos("Divider","Window {0}".format(x)))
        elif x != 1:
            active_windows[x+1].nudgeslider(True,cv2.getTrackbarPos("Divider","Window {0}".format(x)))
            active_windows[x-1].nudgeslider(False,cv2.getTrackbarPos("Divider","Window {0}".format(x)))
        
    #Otherwise and continue
    if (len(active_windows) != 1):
        for i in range(len(active_windows)-1):
            if i == 0:#If it is the first window
                active_windows[i].max = [255,255,255]
                temp = active_windows[i+1].get_trackpos()+1
                active_windows[i].min = [temp,temp,temp]
            else:
                temp = active_windows[i].get_trackpos()
                active_windows[i].max = [temp,temp,temp]
                temp = active_windows[i+1].get_trackpos() + 1
                active_windows[i].min = [temp,temp,temp]
        #Final one
        temp = active_windows[len(active_windows)-1].get_trackpos()
        active_windows[len(active_windows)-1].max = [temp,temp,temp]
        active_windows[len(active_windows)-1].min = [0,0,0]
    
    #Handling generating paper and inverses
    for i in range(len(active_windows)):
        active_windows[i].update_colors(-1)
        active_windows[i].max = numpy.array(active_windows[i].max, dtype="uint8")
        active_windows[i].min = numpy.array(active_windows[i].min, dtype="uint8")
        active_windows[i].inverse = cv2.inRange(grayscale_image,active_windows[i].min,active_windows[i].max)
        active_windows[i].compaper = cv2.bitwise_or(active_windows[i].paper,active_windows[i].paper,mask=active_windows[i].inverse)
    #Generate inital image
    full_image = cv2.bitwise_or(active_windows[0].compaper,active_windows[1].compaper)
    #Regenerate based off of # of windows
    if cv2.getTrackbarPos("Selector",active_windows[0].name_window) == 0:
        if len(active_windows ) > 2:
            for i in range(2,len(active_windows)):
                full_image = cv2.bitwise_or(full_image,active_windows[i].compaper)
    #Reshows the final image
    else:
        full_image = active_windows[cv2.getTrackbarPos("Selector",active_windows[0].name_window)-1].compaper
    cv2.imshow('Custom {0}'.format(filename), full_image)

#Adding the first 2 windows
if (selected_preset != None):
    for i in range(len(selected_preset)):
        if i != len(selected_preset) - 1:
            newwin = True
        else:
            newwin = False
        active_windows.append((cus_window(i,255- i * (int(round(255 / len(selected_preset)))),colors[selected_preset[i]],newwin)))
else:
    active_windows.append(cus_window(0))
    active_windows.append(cus_window(1))

#Generate the image for the first time
generate_image(-1)
#Waiting for a key to be pressed
'''
keypressed = cv2.waitKey(0)
if keypressed == 27:  # esc == 27
    cv2.destroyAllWindows()
elif keypressed == ord('s'):
    if (os.path.isfile('{0}_custom.jpg'.format(filename[:-4]))) == False:
        cv2.imwrite('{0}_custom.jpg'.format(filename[:-4]), full_image)
    else:
        g = 1
        Ndone = True
        while Ndone:
            if (os.path.isfile('{0}_custom_({1}).jpg'.format(filename[:-4],g))) == False:
                cv2.imwrite('{0}_custom_({1}).jpg'.format(filename[:-4],g), full_image)
                Ndone = False
            else:
                g += 1
                
    # cv2.imwrite('photo_RY_1.jpg',customized_image)
    cv2.destroyAllWindows()
'''
dosave = False
while True:
    if (filename == None):
        ret, image = vid.read()#Grabs the ret and the frame
        thing = numpy.array(image, dtype=numpy.uint8)
        original_image = cv2.cvtColor(thing,cv2.IMREAD_COLOR)
        grayscale_image_simple = cv2.cvtColor(thing,cv2.COLOR_BGR2GRAY)
        grayscale_image = cv2.cvtColor(grayscale_image_simple, cv2.COLOR_GRAY2BGR)
        image_height = original_image.shape[0]#Image height
        image_width = original_image.shape[1]#Image width
        image_channels = original_image.shape[2]#Image channels
        generate_image(-1)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):#Exits if the q key is pressed
        break
    elif cv2.waitKey(1) &0xFF == ord('s'):
        dosave = True
        break

if (dosave):
    if(filename == None):
        filename = "Video.jpg"
    if (os.path.isfile('{0}_custom.jpg'.format(filename[:-4]))) == False:
        cv2.imwrite('{0}_custom.jpg'.format(filename[:-4]), full_image)
    else:
        g = 1
        Ndone = True
        while Ndone:
            if (os.path.isfile('{0}_custom_({1}).jpg'.format(filename[:-4],g))) == False:
                cv2.imwrite('{0}_custom_({1}).jpg'.format(filename[:-4],g), full_image)
                Ndone = False
            else:
                g += 1
                
    # cv2.imwrite('photo_RY_1.jpg',customized_image)
cv2.destroyAllWindows()#Kill all windows
vid.release()
f.close()