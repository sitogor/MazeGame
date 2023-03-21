# import the necessary packages
from collections import deque
import imutils
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import time
import matplotlib.ticker as plticker
import matplotlib.pyplot as plt

cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop) 
time.sleep(1)
ret,frame = cap.read() # return a single frame in variable `frame`



lower_red = np.array([0,100,95])
# lower_red = np.array([0,100,80]) ## modified 
upper_red = np.array([7,255,255])

## Trial 


lower_blue = np.array([100, 50, 50])
upper_blue = np.array([130, 255, 255])
# greenLower = (29, 86, 6)  ## Original
greenUpper = (64, 255, 255)     ## Original 
greenLower  = 26,103,104
# greenUpper  = 90,174,133
myInterval = 80
Grids =[]
centrex = [] #Gives the x range for each grid 
centrey = [] #Gives the y range for each grid 
gridrange=[] #Gives the x,y range for each grid 
contour_coord = []
font                   = cv2.FONT_HERSHEY_SIMPLEX
fontScale              = 1
fontColor              = (255,255,255)
thickness              = 2
lineType               = 2

##### FUNCTIONS 
## function to overlay grids and get the gridrange which gives the boundry values for each grid. 

def gridoverlay():
    global frame 
    global ny

    frame = cv2.resize(frame, (1000,1000),interpolation=cv2.INTER_AREA)

       # Draw the grid 
    for i in range(0, frame.shape[0], int(myInterval)):
        cv2.line(frame, (0, i), (frame.shape[1], i), (0, 0, 255), 1)        ## Horizontal lines
    for i in range(0, frame.shape[1], int(myInterval)):
        cv2.line(frame, (i, 0), (i, frame.shape[0]), (0, 0, 255), 1)

    nx = int(frame.shape[0]/myInterval)
    ny = int(frame.shape[1]/myInterval)


    for j in range(ny):
        y=(myInterval/2+j*myInterval)
        for i in range(nx):
            x=(myInterval/2.+float(i)*myInterval)
            frame = cv2.putText(frame,
            '{:d}'.format(i+j*nx), 
            (int(x),int(y)), 
            font, 
            fontScale,
            fontColor,
            thickness,
            lineType)
            
            # if len(centrex) < (ny*nx):
            centrex.append(x) 
            centrey.append(y)

    for k in range((int(ny)*int(nx))):
        centrex[k] = [(centrex[k]-(myInterval/2)), (centrex[k]+(myInterval/2))]
        centrey[k] = [(centrey[k]-(myInterval/2)), (centrey[k]+(myInterval/2))]
        gridrange.append([(centrex[k]),centrey[k]])



######## FUNCTION TO INDENTIFY THE GRIDNUMBER RELATING TO MAZE OR BALL 

def grid_detection(): 
    global grid
    for s in gridrange:
        xrange = s[0] 
        yrange = s[1]


        if contourx >= xrange[0] and contourx <= xrange[1] and contoury >= yrange[0] and contoury <= yrange[1]:
            grid = gridrange.index(s)
            # Grids.append(grid)

### END of functions 


########### PATH DETECTION 


gridoverlay()       # Apply the grids to the image and obtain the gridrange

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# define the range of blue color in HSV color space
lower_blue = np.array([100, 50, 50])
upper_blue = np.array([130, 255, 255])


# threshold the image to extract blue regions
mask = cv2.inRange(hsv, lower_red, upper_red)

# apply morphological transformations to remove noise
kernel = np.ones((5, 5), np.uint8)
opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

# find contours in the binary image
cnts, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

for cnt in cnts:
    area = cv2.contourArea(cnt)
    if area > 100:
        cv2.drawContours(frame, [cnt], 0, (0, 255, 0), 2)
        for i in cnt:
            contourx, contoury = i[0]
            contour_coord.append([contourx,contoury])

            grid_detection()
            Grids.append(grid)

    

Grids = [*set(Grids)]
Grids.sort()
print("Path Grids are: ",Grids)    
print("Number of grids  = ",len(Grids))

### Toms code which needs further correction/hardcoding. 

# start = 18
# end = 76
# size = ny ##  change to ny 
# tot = {}
# def path_det(Grid_num, start,end):
# #    print(Grid_num)
#     direction =[]
#     if (Grid_num+1) in Grids:
#         direction.append(Grid_num+1)
#         # Grids_1.remove(Grid_num)
#     if (Grid_num+size) in Grids:
#         direction.append(Grid_num+size)
#         # Grids_1.remove(Grid_num)
#     if (Grid_num - 1) in Grids:
#         direction.append(Grid_num-1)
#         # Grids_1.remove(Grid_num)
#     if (Grid_num - size) in Grids:
#         direction.append(Grid_num-size)
#     if len(direction)==0 or Grid_num==end:
#         direction = [start]
#     #Grids_1.remove(Grid_num)

#     return direction


# # making a list of the removable items in the list
# def remove_func():
#     remove_list =[]
#     for y in Grids:
#         if len(tot[y])==1:
#     #            print(y,tot[y], len(tot[y]))
#                 remove_list.append(tot[y][0])
#     return remove_list


# #removing possible directions to blocks if another block can only move to that block 
# def route_recog(new_tot,remove_ls):
#     for u in Grids:
#         if len(new_tot[u])>1:
#     #        print(tot[u])
#             for x in remove_ls:
#                 if x in new_tot[u]:
#                     new_tot[u].remove(x)
#     return(new_tot)


# # removing all the not possible routes where the ball could be stuck between 2 grids, input of the newest tot dictionary
# def not_poss(new_tot):
#     # key_list = list(new_tot.keys())
#     # print(key_list)
#     for y in Grids:
#         if len(new_tot[y])==1:
#             g = new_tot[y][0]
#             if y in new_tot[g]:
#                 new_tot[g].remove(y)
#     return(new_tot)


# # getting the final dictionary and working out the direction the ball has to take once in a certain grid
# def directions(tot_final,size):
#     final_route={}
#     # turning single value lists into just the integers
#     for x in Grids:
#         tot_final.update({x:tot_final[x][0]})
#     #getting directions for each grid number
#     for x in Grids:
#         if x==tot_final[x]+1:
#             direction = 'l'
#         elif x==tot_final[x]-1:
#             direction = 'r'
#         elif x==tot_final[x]+size:
#             direction = 'u'
#         elif x==tot_final[x]-size:
#             direction = 'd'
#         else:
#             direction = 'end'
#         final_route[x]=direction
#     return final_route


# # rem = remove_func()
# # print(rem)
# for x in range(len(Grids)):
#     maze = path_det(Grids[x],start,end)
#     tot[Grids[x]] = maze
# # print (tot)
# finished =False

# fin=0
# while finished ==False:
#     list_len=0
#     for x in Grids:
#         list_len+=len(tot[x])
#     if list_len==len(tot):
#         print(directions(tot,size))
#         finished = True
#     elif fin==10:
#         finished = True
#     else:
#         rem=remove_func()
#         tot=route_recog(tot,rem)
#         tot=not_poss(tot)
#         print(tot)
#         fin+=1
#         finished = False



# cv2.imshow('img1',frame) #display the captured image
# cv2.waitKey()
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
plt.imshow(frame)
plt.show()


########################################################
#### BALL DETECTION ############

vs = cv2.VideoCapture(0)


# keep looping
while True:
    centrex = [] #Gives the x range for each grid 
    centrey = [] #Gives the y range for each grid 
    gridrange=[] #Gives the x,y range for each grid 
    contour_coord = []
    
    # grab the current frame
    ret, frame = vs.read()

    

    # handle the frame from VideoCapture or VideoStream

    gridoverlay()

    ### Contour detection ###

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None


    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        

        # only proceed if the radius meets a minimum size
        if radius > 5:         ### was originally 15
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)


            contourx, contoury = center 
            contour_coord.append([contourx,contoury])

            grid_detection()
            print(grid)


        else: #if radius < 50:
            print("No ball is detected")
            print("Radius is: ", radius)


    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    


    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

    
vs.release()

# close all windows
cv2.destroyAllWindows()
