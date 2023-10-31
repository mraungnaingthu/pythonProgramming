import cv2
import easygui
import numpy as np
import imageio
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk,Image

gui = tk.Tk()
gui.title('Transform Your Image !')
gui.configure(background='#218384')
gui.geometry('450x500+20+20')
label = Label(gui,background='#00FFFF')

def getImage():
    ImagePath = easygui.fileopenbox()
    transForm((ImagePath))

def transForm(ImagePath):
    originalmage = cv2.imread(ImagePath)
    originalmage = cv2.cvtColor(originalmage,cv2.COLOR_BGR2RGB)
    print('original',originalmage)
    print(originalmage.ndim)

    if originalmage is None:
        print('It is not a valid image File .')
        sys.exit()

    #For 1 image
    image1 = cv2.resize(originalmage,(900,450))

    #For 2 image
    grayScale = cv2.cvtColor(originalmage,cv2.COLOR_BGRA2GRAY)
    image2 = cv2.resize(grayScale,(900,450))

    #For blur image 3
    smoothGray = cv2.medianBlur(grayScale,3)
    image3 = cv2.resize(smoothGray,(900,450))
    getEdge = cv2.adaptiveThreshold(smoothGray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,9,9)
    image4 = cv2.resize(getEdge,(960,500))
    #cv2.imshow('Adaptive Threshold',image4)

    GauImage = cv2.GaussianBlur(originalmage,(7,7),0)
    image5 = cv2.resize(GauImage,(960,540))
    cv2.imshow('GaussialnBlur',image5)

    FinalImage = cv2.bitwise_and(GauImage,GauImage,mask=getEdge)
    image6 = cv2.resize(FinalImage,(960,450))

    images = [image1,image2,image3,image4,image5,image6]
    fig,axes = plt.subplots(3,2,figsize=(8,8),subplot_kw={'xticks':[],'yticks':[]},gridspec_kw=dict(hspace=0.1,wspace=0.1))

    for i,ax in enumerate(axes.flat):
        ax.imshow(images[i],cmap='gray')

    save1 = Button(gui,text='Save TransFormed Image',command=lambda: ImageSave(image6,ImagePath),padx=10,pady=5)
    save1.configure(background='#612184',foreground='#F9F60A')
    save1.pack(side=TOP,pady=20)
    plt.show()

def ImageSave(image6,ImagePath):
    newName = 'TransformedImage'
    path1 = os.path.dirname(ImagePath)
    extension = os.path.splitext(ImagePath)[1]
    path=os.path.join(path1,newName+extension)
    cv2.imwrite(path,cv2.cvtColor(image6,cv2.COLOR_BGR2RGB))
    info = 'Image saved by name'+newName+'at'+path
    tk.messagebox.showinfo(title=None,message=info)

upload=Button(gui,text="Transform Your Image",command=getImage,padx=10,pady=5)
upload.configure(background='#612184', foreground='#F9F60A',font=('calibri',10,'bold'))
upload.pack(side=TOP,pady=150)
gui.mainloop()

