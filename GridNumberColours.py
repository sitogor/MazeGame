import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
try:
    from PIL import Image
except ImportError:
    import Image

import imutils
import cv2
import matplotlib.pyplot as plt



# path = "/Users/melvin/Documents/Summer '22 Work for Fun/Line Detection /Test Images /IMG_0309.jpeg"
path = "/Users/melvin/Documents/Summer '22 Work for Fun/Line Detection /Test Images /mazewithblue.JPG"




# Open image file
image = Image.open(path)
image = image.resize((225,225))



my_dpi=300.

# Set up figure
fig=plt.figure(figsize=(float(image.size[0])/my_dpi,float(image.size[1])/my_dpi),dpi=my_dpi)
ax=fig.add_subplot(111)

# Remove whitespace from around the image
fig.subplots_adjust(left=0,right=1,bottom=0,top=1)

# Set the gridding interval: here we use the major tick interval
myInterval=15.
loc = plticker.MultipleLocator(base=myInterval)
ax.xaxis.set_major_locator(loc)
ax.yaxis.set_major_locator(loc)

centre = [] #List with the all the centre coordinates forn each grid. 
centrex = [] #Gives the x range for each grid 
centrey = [] #Gives the y range for each grid 
gridrange=[] #Gives the x,y range for each grid 


# Add the grid
ax.grid(which='major', axis='both', linestyle='-')

# Add the image
ax.imshow(image)

# Find number of gridsquares in x and y direction
nx=abs(int(float(ax.get_xlim()[1]-ax.get_xlim()[0])/float(myInterval)))
ny=abs(int(float(ax.get_ylim()[1]-ax.get_ylim()[0])/float(myInterval)))

# ny*ny is the total nunber of grids 

# Add some labels to the gridsquares
for j in range(ny):
    y=myInterval/2+j*myInterval
    for i in range(nx):
        x=myInterval/2.+float(i)*myInterval
        ax.text(x,y,'{:d}'.format(i+j*nx),color='r',ha='center',va='center',fontsize = 2) 
        centre.append([x,y])
        centrex.append(x) 
        centrey.append(y)
    
for k in range(ny*nx):
    centrex[k] = [(centrex[k]-(myInterval/2)), (centrex[k]+(myInterval/2))]
    centrey[k] = [(centrey[k]-(myInterval/2)), (centrey[k]+(myInterval/2))]
    gridrange.append([(centrex[k]),centrey[k]])



# Save the figure
plt.imshow(image)
plt.show()


############## Contour Coordinates 
contour_coord = []
Grids = []


img = cv2.imread(path)
img = cv2.resize(img, (225,225), interpolation= cv2.INTER_AREA)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_blue = (90,60,0)
upper_blue =(121,255,255)

blue = cv2.inRange(hsv, lower_blue, upper_blue)

cv2.inRange(hsv, lower_blue, upper_blue)

# cnts3 = cv2.findContours(blue,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
cnts3 = cv2.findContours(blue,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

cnts3 = imutils.grab_contours(cnts3)

open('contourdata.txt', 'w').close()

for c in cnts3: 
    cv2.drawContours(img,[c],-1,(0,255,0),3)
    for point in cnts3:
        for i in point:
            contourx, contoury = i[0]
            contour_coord.append([contourx,contoury])
            # with open('contourdata.txt', 'a') as f:
            #     f.write(str([contourx,contoury]))             ## Only for saving data of contour. 
            #     f.write("\n")


            for s in gridrange:
                xrange = s[0] 
                yrange = s[1]

                if contourx >= xrange[0] and contourx <= xrange[1] and contoury >= yrange[0] and contoury <= yrange[1]:
                    grid = gridrange.index(s)
                    Grids.append(grid)


Grids = [*set(Grids)]
print(Grids)    
print(len(Grids))
