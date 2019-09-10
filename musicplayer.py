import os
from tkinter.filedialog import askdirectory
import pygame
from mutagen.id3 import ID3
from tkinter import *
import tkinter.messagebox as tkMessageBox
import random

root = Tk()
root.wm_title("Music Player")
root.minsize(500,500)

listofsongs=[]
realnames = []

v =StringVar()
songlabel =Label(root,textvariable=v,width=80)
index=0
count=0

ctr=0

def updatelabel():
    global index
    v.set(listofsongs[index])
    
def pausesong(event):
    global ctr
    
    if (ctr==0):
        pygame.mixer.music.pause()
        ctr=1
    elif (ctr==1):
        pygame.mixer.music.unpause()
        ctr=0

def playsong(event):
    v.set(listbox.get(ACTIVE))
    global index
    index = listbox.curselection()[0]
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()

def shufflesongs(event):
    global index
    index = 0
    random.shuffle(listofsongs)
    listbox.delete(0,END)
    for items in listofsongs:
            listbox.insert(0, items)
    
def nextsong(event):
    global index
    index += 1
    if (index < count):
        pygame.mixer.music.load(listofsongs[index])
        pygame.mixer.music.play()
    else:
        index = 0
        pygame.mixer.music.load(listofsongs[index])
        pygame.mixer.music.play()
    try:
      updatelabel()
    except NameError:
        print("Name Error")

def previoussong(event):
    global index
    index -= 1
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    try:
        updatelabel()
    except NameError:
        print("Name Error")

def stopsong(event):
    pygame.mixer.music.stop()
   
def mute(event):
    vol.set(0)

listbox=Listbox(root,selectmode=SINGLE,width=100,height=20,bg="grey",fg="black")
listbox.pack(fill=X)

def directorychooser():
  global count
  global index
    

  directory = askdirectory()
  if(directory):
    count=0
    index=0
    
    del listofsongs[:]
    del realnames[:]

    os.chdir(directory)

    for  files in os.listdir(directory):

        try:
         if files.endswith(".mp3"):

              realdir = os.path.realpath(files)
              audio = ID3(realdir)
              realnames.append(audio['TIT2'].text[0])
              listofsongs.append(files)
        except:
            print(files+" is not a song")

    if listofsongs == [] :
       okay=tkMessageBox.askretrycancel("No Songs Found","No Songs")
       if(okay==True):
           directorychooser()

    else:
        listbox.delete(0, END)
        realnames.reverse()
        for items in realnames:
            listbox.insert(0, items)
        for i in listofsongs:
            count = count + 1
        pygame.mixer.init()
        pygame.mixer.music.load(listofsongs[0])

        pygame.mixer.music.play()
        try:
            updatelabel()
        except NameError:
            print("")
  else:
    return 1

try:
        directorychooser()
except WindowsError:
         print("Windows Error")


def call(event):

 if(True):
    try:
        k=directorychooser()

    except WindowsError:
         print("Windows Error")


songlabel.pack()

def show_value(self):
    i = vol.get()
    pygame.mixer.music.set_volume(i)

vol = Scale(root,from_ = 5,to = 0,orient = VERTICAL ,resolution = 1,command = show_value)
vol.place(x=85, y = 330)
vol.set(5)

framedown =Frame(root,width=400,height=200)
framedown.pack()

openbutton = Button(framedown,text="Open")
openbutton.pack(side=LEFT)

mutebutton = Button(framedown,text="Mute")
mutebutton.pack(side=LEFT)

previousbutton = Button(framedown,text="Prev")
previousbutton.pack(side=LEFT)

playbutton = Button(framedown,text="Play")
playbutton.pack(side=LEFT)

shufflebutton = Button(framedown,text="Shuffle")
shufflebutton.pack(side=LEFT)

stopbutton = Button(framedown,text="Stop")
stopbutton.pack(side=LEFT)

nextbutton = Button(framedown,text="Next")
nextbutton.pack(side=LEFT)

pausebutton = Button(framedown,text="Play/Pause")
pausebutton.pack(side=LEFT)

mutebutton.bind("<Button-1>",mute)
openbutton.bind("<Button-1>",call)
playbutton.bind("<Button-1>",playsong)
shufflebutton.bind("<Button-1>",shufflesongs)
nextbutton.bind("<Button-1>",nextsong)
previousbutton.bind("<Button-1>",previoussong)
stopbutton.bind("<Button-1>",stopsong)
pausebutton.bind("<Button-1>",pausesong)

root.mainloop()
