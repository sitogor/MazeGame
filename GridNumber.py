import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
try:
    from PIL import Image
except ImportError:
    import Image

import imutils
import cv2
import matplotlib.pyplot as plt



path = r"C:\Users\thoma\OneDrive\Documents\Maze_Project\Image.jpg"

# Open image file
image = Image.open(path)


my_dpi=300.

# Set up figure
fig=plt.figure(figsize=(float(image.size[0])/my_dpi,float(image.size[1])/my_dpi),dpi=my_dpi)
ax=fig.add_subplot(111)

# Remove whitespace from around the image
fig.subplots_adjust(left=0,right=1,bottom=0,top=1)

# Set the gridding interval: here we use the major tick interval
myInterval=15
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

# ny*ny is the total nunbe of grids 

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

image = cv2.imread(path)
# convert to RGB
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
# create a binary thresholded image
_, binary = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)


# find the contours from the thresholded image
contours, hierarchy = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)


Grids = []


for contour in contours:
    for point in contour:
        # print(point)
        contourx, contoury = point[0]

        for s in gridrange:
            xrange = s[0] 
            yrange = s[1]



            if contourx >= xrange[0] and contourx <= xrange[1] and contoury >= yrange[0] and contoury <= yrange[1]:
                grid = gridrange.index(s)
                Grids.append(grid)


Grids = [*set(Grids)]
Grids_1 = Grids
print(Grids)
print(len(Grids))

# draw all contours
image = cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

# show the image with the drawn contours

plt.imshow(image)

plt.show()


print (gridrange)
Grids = Grids_1
size = 6
tot = []
def path_det(Grid_num):
    if (Grid_num+1) in Grids_1:
        direction = ['R', Grid_num]
        # Grids_1.remove(Grid_num)
    elif (Grid_num+size) in Grids_1:
        direction  = ['D', Grid_num]
        # Grids_1.remove(Grid_num)
    elif (Grid_num - 1) in Grids_1:
        direction = ['L', Grid_num]
        # Grids_1.remove(Grid_num)
    elif (Grid_num - size) in Grids_1:
        direction = ['U', Grid_num]
        # Grids_1.remove(Grid_num)
    else:
        direction = ('error')
    return direction

for x in range(len(Grids)):
    maze = path_det(Grids[x])
    tot.append(maze)
print (tot)
