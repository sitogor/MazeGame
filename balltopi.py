import socket
TCP_IP = '169.254.22.20'
TCP_PORT = 5005
MESSAGE = "Hello, world!"


Tx=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Tx.connect((TCP_IP, TCP_PORT))

# s.send(MESSAGE.encode())

# USAGE

# python ball_tracking.py --video ball_tracking_example.mp4

# python ball_tracking.py

# import the necessary packages

import csv
from collections import deque
import imutils
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import time
import matplotlib.pyplot as plt

width  = 1200
height  = 1200 

def draw(x, y, w, h):
   cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)


dict_from_csv = {}

path =  '/Users/melvin/Documents/Testing Files for Maze /hardcode .csv'
with open(path, mode='r') as inp:
    reader = csv.reader(inp)
    dict_from_csv = {rows[0]:rows[1] for rows in reader}
    
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

greenLower  = 26,103,104

lower_blue = np.array([100, 50, 50])
upper_blue = np.array([130, 255, 255])

lower_red = np.array([0,100,95])

upper_red = np.array([7,255,255])


# greenLower = 20,100,90


myInterval = 80


Grids =[]


font                   = cv2.FONT_HERSHEY_SIMPLEX
fontScale              = 1
fontColor              = (255,255,255)
thickness              = 3
lineType               = 2

width  = 1200
height  = 1200 
dst_points = np.array([(0, 0),(0, height),(width, height), (width, 0), ], dtype=np.float32)
min_area = 200

# if a video path was not supplied, grab the reference
# to the webcam
vs = VideoStream(src=0).start()

# otherwise, grab a reference to the video file


# allow the camera or video file to warm up
# time.sleep(2.0)

counter = 0 

# keep looping
while True:
    centrex = [] #Gives the x range for each grid 
    centrey = [] #Gives the y range for each grid 
    gridrange=[] #Gives the x,y range for each grid 
    contour_coord = []
    
	# grab the current frame
    frame = vs.read()

    frame = cv2.resize(frame, (width,height),interpolation=cv2.INTER_AREA)


    #  Convert the frame from BGR to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask that only keeps blue pixels
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Apply a series of morphological transformations to the mask to remove noise and fill holes
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Find contours (i.e., blue rectangles) in the mask
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blue_rectangles_centre = []
    height,width,c = frame.shape
    counter = 0 


    # Loop through all the contours
    for contour in contours:
        # Compute the area of the contour
        area = cv2.contourArea(contour)

        x, y, w, h = cv2.boundingRect(contour) # new 

        # Only consider contours with an area larger than the minimum
        if area > min_area:

            if x  < width/2 and y < height/2:
                # Draw a rectangle around the contour on the original frame
                draw(x, y, w, h)
                # Compute the center of the rectangle
                cxTL, cyTL = x + w // 2, y + h // 2
                counter += 1
                # Add the center coordinates of the rectangle to the list

                
            if x  > width/2 and y < height/2:
                draw(x, y, w, h)
                cxTR, cyTR = x + w // 2, y + h // 2
                counter += 1
                
            if x  < width/2 and y > height/2:
                draw(x, y, w, h)
                cxBL, cyBL = x + w // 2, y + h // 2
                counter += 1
                
            if x  > width/2 and y > height/2:
                draw(x, y, w, h)
                cxBR, cyBR = x + w // 2, y + h // 2
                counter += 1


    if counter == 4:  
        blue_rectangles_centre = [(cxTL, cyTL), (cxBL, cyBL), (cxBR, cyBR),(cxTR,cyTR)]
            


    if len(blue_rectangles_centre) == 4:


        blue_rectangles_centre = np.array(blue_rectangles_centre, dtype=np.float32)
        M = cv2.getPerspectiveTransform(blue_rectangles_centre, dst_points)
        frame = cv2.warpPerspective(frame, M, (width, height))
    

	# handle the frame from VideoCapture or VideoStream
    frame = frame[1] if args.get("video", False) else frame


    # resize the frame, blur it, and convert it to the HSV
    # color space
    # frame = imutils.resize(frame, width=600)
    frame = cv2.resize(frame, (width,height),interpolation=cv2.INTER_AREA)


        # Draw the grid 
    for i in range(0, frame.shape[0], int(myInterval)):
        cv2.line(frame, (0, i), (frame.shape[1], i), (0, 0, 255), 1)        ## Horizontal lines
    for i in range(0, frame.shape[1], int(myInterval)):
        cv2.line(frame, (i, 0), (i, frame.shape[0]), (0, 0, 255), 1)

    nx = int(frame.shape[0]/myInterval)
    ny = int(frame.shape[1]/myInterval)


     ### Adding the numbers to the Grids:

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


    ### Contour detection. 

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    # mask = cv2.inRange(hsv, greenLower, greenUpper)
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
        if radius > 5:         ### was originally 10
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            # print(radius)

            ## code for identifying grid number.


            contourx, contoury = center 
            contour_coord.append([contourx,contoury])

            for s in gridrange:
                xrange = s[0] 
                yrange = s[1]

                if contourx >= xrange[0] and contourx <= xrange[1] and contoury >= yrange[0] and contoury <= yrange[1]:
                    grid = gridrange.index(s)
                    print(grid)
                    try:
                        x=dict_from_csv[str(grid)]
                        print(x)
                        Tx.send(x.encode())
                    # data = s.recv(BUFFER_SIZE)
                    # s.close()

                    # print("recieved data:", data)
                        Grids.append(grid)
                    except:
                        Tx.send(b'nan'.encode())
                    # counter += 1 
                    # print(counter)

    else: 
        radius = 0

        if radius < 15:
            [print("No ball is detected")]
            print("Radius is: ", radius)

    # else: 
        # print(radius)
        # print(cnts)

    # show the frame to our screen\

    cv2.imshow("Frame", frame) 
    key = cv2.waitKey(1) & 0xFF


    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

    # if we are not using a video file, stop the camera video stream
if not args.get("video", False):
    vs.stop()

# otherwise, release the camera
else:
    vs.release()

# close all windows
cv2.destroyAllWindows()

# Grids = [*set(Grids)]
# Grids.sort()
# print(Grids)    
# print(len(Grids))
