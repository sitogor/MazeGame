from tkinter import *
import cv2
import numpy as np
from PIL import Image,ImageTk


root = Tk()
root.geometry('700x540')
root.configure(bg='black')
Label(root,text='Arum Cam#1', font=('times new roman', 30, 'bold'), bg='black', fg='red').pack()
f1 = LabelFrame(root,bg='red')
f1.pack()
L1 = Label(f1,bg='red')
L1.pack()
cap = cv2.VideoCapture(2)
Button(root,text='Take Snapshot', font=('times new roman', 30, 'bold'), bg='black',fg='red')

while True:
    img = cap.read()[1]
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img = ImageTk.PhotoImage(Image.fromarray(img))
    L1['Image'] = img


    root.update()
        

