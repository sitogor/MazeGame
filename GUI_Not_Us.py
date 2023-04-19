import tkinter as tk
import os
import cv2
import sys
from PIL import Image, ImageTk
from grid_gpio import *

cancel = False

running = False
minutes, seconds = 0, 0


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
    global minutes, seconds
    minutes, seconds =0, 0
    # set label back to zero
    stopwatch_label.config(text='00:00')
    pi.set_servo_pulsewidth(servo_pin1, Init_X)
    pi.set_servo_pulsewidth(servo_pin2, Init_Y)


# update stopwatch function
def update():
    # update seconds with (addition) compound assignment operator
    global minutes, seconds
    seconds += 1
    if seconds == 60:
        minutes += 1
        seconds = 0
    
    # format time to include leading zeros
    minutes_string = f'{minutes}' if minutes > 9 else f'0{minutes}'
    seconds_string = f'{seconds}' if seconds > 9 else f'0{seconds}'
    # update timer label after 1000 ms (1 second)
    stopwatch_label.config(text= minutes_string + ':' + seconds_string)
    # after each second (1000 milliseconds), call update function
    # use update_time variable to cancel or pause the time using after_cancel
    global update_time
    update_time = stopwatch_label.after(1000, update)

def prompt_ok(event = 0):
    global cancel
    cancel = True


def resume(event = 0):
    global lmain, cancel

    if cancel == False:
        pass
    else: 
        cancel = False
        mainWindow.bind('<Return>', prompt_ok)
        lmain.after(10, show_frame)

    


cap = cv2.VideoCapture(0)




mainWindow = tk.Tk()
mainWindow.title('GUI')
mainWindow.geometry('600x800')
mainWindow.bind('<Escape>', lambda e: mainWindow.quit())

lmain = tk.Label(mainWindow, compound=tk.CENTER, anchor=tk.CENTER, relief=tk.RAISED)
lmain.pack()


stopwatch_label = tk.Label(text='00:00', font=('Arial', 60))
stopwatch_label.pack()

start_button = tk.Button(text='start', height=5, width=8, font=('Arial', 20), command=lambda:[start(), resume()])
start_button.pack(side=tk.LEFT)
pause_button = tk.Button(text='pause', height=5, width=8, font=('Arial',20 ), command=lambda:[pause(), prompt_ok()])
pause_button.pack(side=tk.LEFT)
reset_button = tk.Button(text='reset', height=5, width=8, font=('Arial', 20), command=reset)
reset_button.pack(side=tk.LEFT)
quit_button = tk.Button(text='quit', height=5, width=8, font=('Arial', 20), command=mainWindow.quit)
quit_button.pack(side=tk.LEFT)


def show_frame():
    global cancel, prevImg, button
    frame=game(cap)
    frame_resize = cv2.resize(frame, (320, 240))
    #_, frame = cap.read()
    cv2image = cv2.cvtColor(frame_resize, cv2.COLOR_BGR2RGBA)

    prevImg = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    if not cancel:
        lmain.after(10, show_frame)

if __name__ == '__main__':
    show_frame()
    mainWindow.mainloop()
