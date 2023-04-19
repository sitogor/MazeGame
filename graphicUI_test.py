# !/usr/local/bin/python
import tkinter as tk
import os
import cv2
import sys
from PIL import Image, ImageTk
from Hard_code_route import *


fileName = os.environ['ALLUSERSPROFILE'] + "\WebcamCap.txt"
cancel = False

# ***** VARIABLES *****
# use a boolean variable to help control state of time (running or not running)
running = False
# time variables initially set to 0
hours, minutes, seconds = 0, 0, 0

# ***** NOTES ON GLOBAL *****
# global will be used to modify variables outside functions
# another option would be to use a class and subclass Frame

# ***** FUNCTIONS *****
# start, pause, and reset functions will be called when the buttons are clicked
# start function
def start():
    global running
    if not running:
        update()
        running = True

# pause function
def pause():
    global running
    if running:
        # cancel updating of time using after_cancel()
        stopwatch_label.after_cancel(update_time)
        running = False

# reset function
def reset():
    global running
    if running:
        # cancel updating of time using after_cancel()
        stopwatch_label.after_cancel(update_time)
        running = False
    # set variables back to zero
    global hours, minutes, seconds
    hours, minutes, seconds = 0, 0, 0
    # set label back to zero
    stopwatch_label.config(text='00:00:00')

# update stopwatch function
def update():
    # update seconds with (addition) compound assignment operator
    global hours, minutes, seconds
    seconds += 1
    if seconds == 60:
        minutes += 1
        seconds = 0
    if minutes == 60:
        hours += 1
        minutes = 0
    # format time to include leading zeros
    hours_string = f'{hours}' if hours > 9 else f'0{hours}'
    minutes_string = f'{minutes}' if minutes > 9 else f'0{minutes}'
    seconds_string = f'{seconds}' if seconds > 9 else f'0{seconds}'
    # update timer label after 1000 ms (1 second)
    stopwatch_label.config(text=hours_string + ':' + minutes_string + ':' + seconds_string)
    # after each second (1000 milliseconds), call update function
    # use update_time variable to cancel or pause the time using after_cancel
    global update_time
    update_time = stopwatch_label.after(1000, update)

def prompt_ok(event = 0):
    global cancel
    cancel = True


def saveAndExit(event = 0):
    global prevImg

    if (len(sys.argv) < 2):
        filepath = "imageCap.png"
    else:
        filepath = sys.argv[1]

    print ("Output file to: " + filepath)
    prevImg.save(filepath)
    

def resume(event = 0):
    global lmain, cancel

    if cancel == False:
        pass
    else: 
        cancel = False
        mainWindow.bind('<Return>', prompt_ok)
        lmain.after(10, show_frame)

    
vs = cv2.VideoCapture(0)

#change camera function
# def changeCam(event=0, nextCam=-1):
#     global camIndex, cap, fileName #current camera index, capature (cv2), filename to write the camera index

#     if nextCam == -1:
#         camIndex += 1 # cycles through camera indices
#     else:
#         camIndex = nextCam
#     del(cap)
#     cap = cv2.VideoCapture(camIndex) 

#     #try to get a frame, if it returns nothing
#     success, frame = cap.read()
#     if not success:
#         camIndex = 0
#         del(cap)
#         cap = cv2.VideoCapture(camIndex)

#     f = open(fileName, 'w')
#     f.write(str(camIndex))
#     f.close()

# def get_cam_index():
#     try:
#         f = open(fileName, 'r')
#         camIndex = int(f.readline())
#     except:
#         camIndex = 0
#     return camIndex

# def start_capture():
#     global cap
#     cap = cv2.VideoCapture(get_cam_index())
#     capWidth = cap.get(3)
#     capHeight = cap.get(4)

#     success, frame = cap.read()

#     if not success:
#         if camIndex == 0:
#             print("Error, No webcam found!")
#             sys.exit(1)
#         else:
#             changeCam(nextCam=0)
#             success, frame = cap.read()
#             if not success:
#                 print("Error, No webcam found!")
#                 sys.exit(1)

def set_properties():
    global mainWindow, stopwatch_label, lmain 

    mainWindow = tk.Tk(screenName="Camera Capture")
    mainWindow.title('GUI')
    mainWindow.resizable(width=False, height=False)
    mainWindow.bind('<Escape>', lambda e: mainWindow.quit())

    lmain = tk.Label(mainWindow, compound=tk.CENTER, anchor=tk.CENTER, relief=tk.RAISED)
    button = tk.Button(mainWindow, text="Start", command=prompt_ok)
    lmain.pack()
    button.place(bordermode=tk.INSIDE, relx=0.5, rely=0.9, anchor=tk.CENTER, width=300, height=50)
    button.focus()

    stopwatch_label = tk.Label(text='00:00:00', font=('Arial', 60))
    stopwatch_label.pack()

    start_button = tk.Button(text='start', height=5, width=8, font=('Arial', 20), command=lambda:[start(), resume()])
    start_button.pack(side=tk.LEFT)
    pause_button = tk.Button(text='pause', height=5, width=8, font=('Arial',20 ), command=lambda:[pause(), prompt_ok()])
    pause_button.pack(side=tk.LEFT)
    reset_button = tk.Button(text='reset', height=5, width=8, font=('Arial', 20), command=reset)
    reset_button.pack(side=tk.LEFT)
    quit_button = tk.Button(text='quit', height=5, width=8, font=('Arial', 20), command=mainWindow.quit)
    quit_button.pack(side=tk.LEFT)
    #button_changeCam = tk.Button(text="Switch \n Camera", height = 5, width = 8, font=('Arial',20), command=changeCam)
    #button_changeCam.pack(side=tk.LEFT)

def show_frame():
    global cancel, prevImg, button
    frame=frame_loop(vs)
    frame_resize = cv2.resize(frame, (320, 240))
    #_, frame = cap.read()
    cv2image = cv2.cvtColor(frame_resize, cv2.COLOR_BGR2RGBA)

    prevImg = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    if not cancel:
        lmain.after(10, show_frame)
    # global cancel, prevImg, button

    # _, frame2 = pdb.vs.read()
    # cv2image = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGBA)

    # prevImg = Image.fromarray(cv2image)
    # imgtk = ImageTk.PhotoImage(image=prevImg)
    # lmain.imgtk = imgtk
    # lmain.configure(image=imgtk)
    # if not cancel:
    #     lmain.after(10, show_frame)

def main():
    set_properties()
    show_frame()
    mainWindow.mainloop()

if __name__ == "__main__":
    main()