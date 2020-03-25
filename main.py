from tkinter import *
from tkinter import messagebox

from tkinter.ttk import Progressbar
from colors import color
from PIL import Image, ImageTk
import sys
from sort_files import sortIntoFolders,startSorting
from threading import Thread
from paths import *
from glob import glob

windowSize = [470,470]
windowLocation = [750,200]
windowTitle = "Sort Images by Faces"
tempFile = TEMP_FILE_PATH



class SampleApp(Tk):

    isClosed = False
    progressBar = None
    
    # ProgressFrame Data members
    imgLabel = None
    img = None
    copyingProgressBar = None
    progressFrameChild = None

    # ConflictFrame Data members
    imgLabel1 = None
    imgLabel2 = None
    img1 = None
    img2 = None
    conflictProgressBar = None
    conflictFrameChild = None
    userResponse = None
    repeatAction = None
    REPLACE = 1
    SKIP = 2

    def setProgress(self,progress):
        self.progressBar['value']=progress

    def setDisplayImage(self,imgPath):
        self.img = Image.open(tempFile)
        self.img = self.img.resize((200,200))
        self.img = ImageTk.PhotoImage(self.img)
        self.imgLabel = Label(self.progressFrameChild, image = self.img)
        self.imgLabel.grid(row=6,columnspan=3,sticky=W+E+N+S,padx=5,pady=5)

    def setConflictHandleFrame(self):
        self.show_frame("ConflictFrame")
    
    def setConflictImages(self,originalImg,newImg):
        self.img1 = Image.open(originalImg)
        self.img1 = self.img1.resize((200,200))
        self.img1 = ImageTk.PhotoImage(self.img1)
        self.imgLabel1 = Label(self.conflictFrameChild, image = self.img1)
        self.imgLabel1.grid(row=3,column=0,sticky=W+E+N+S,padx=5,pady=5)

        self.img2 = Image.open(newImg)
        self.img2 = self.img2.resize((200,200))
        self.img2 = ImageTk.PhotoImage(self.img2)
        self.imgLabel2 = Label(self.conflictFrameChild, image = self.img2)
        self.imgLabel2.grid(row=3,column=1,sticky=W+E+N+S,padx=5,pady=5)

    def getUserResponse(self):
        return self.userResponse
    
    def setUserResponse(self,value):
        self.userResponse = value

    def getApplySameResponseValue(self):
        if self.repeatAction.get()==1:
            return True
        else:
            return False

    def exitApplication(self):
        self.isClosed = True
        self.destroy()
        exit()
    
    def isApplicationClosed(self):
        return self.isClosed

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainPage, ProgressFrame, ConflictFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainPage")


    def show_frame(self, page_name):
        if page_name=='ProgressFrame':
            self.progressBar = self.copyingProgressBar
        elif page_name=='ConflictFrame':
            self.progressBar = self.conflictProgressBar
        else:
            self.progressBar = self.copyingProgressBar
        frame = self.frames[page_name]
        frame.tkraise()


class ConflictFrame(Frame):

    img1 = None
    img2 = None
    pgbar = None
    imgLabel1 = None
    imgLabel2 = None

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.controller.conflictFrameChild = self

        Label(self,font=("times new roman",20),bg=color['Background'], width=35).grid(row=2,columnspan=3,sticky=W+E+N+S,padx=5,pady=5)

        self.img1 = Image.open(tempFile)
        self.img1 = self.img1.resize((200,200))
        self.img1 = ImageTk.PhotoImage(self.img1)
        self.imgLabel1 = Label(self, image = self.img1)
        self.imgLabel1.grid(row=3,column=0,sticky=W+E+N+S,padx=5,pady=5)
        self.controller.imgLabel1 = self.imgLabel1

        self.img2 = Image.open(tempFile)
        self.img2 = self.img2.resize((200,200))
        self.img2 = ImageTk.PhotoImage(self.img2)
        self.imgLabel2 = Label(self, image = self.img2)
        self.imgLabel2.grid(row=3,column=1,sticky=W+E+N+S,padx=5,pady=5)
        self.controller.imgLabel2 = self.imgLabel2

        self.pgbar = Progressbar(self,length = 100,value=0)
        self.pgbar.grid(row=7,columnspan=3,sticky=W+E+N+S,padx=5,pady=5)
        self.controller.conflictProgressBar = self.pgbar

        Button(self,text="Replace",font=("times new roman",15),bg=color['ButtonBG'],fg=color['NormalText'],command=lambda : controller.setUserResponse(value=controller.REPLACE)).grid(row=8,columnspan=3,sticky=W+E+N+S,padx=5,pady=5)
        Button(self,text="Skip",font=("times new roman",15),bg=color['ButtonBG'],fg=color['NormalText'],command=lambda : controller.setUserResponse(value=controller.SKIP)).grid(row=9,columnspan=3,sticky=W+E+N+S,padx=5,pady=5)
        
        self.controller.repeatAction = IntVar()
        chkMultiple = Checkbutton(self,text="Apply selection for all files",font=("times new roman",12),bg=color['Background'],fg=color['NormalText'],variable=controller.repeatAction)
        chkMultiple.grid(row=10,columnspan=3,sticky=W+E+N+S,padx=5,pady=5,ipady=3)

        Button(self,text="Exit",font=("times new roman",15),bg=color['ButtonBG'],fg=color['NormalText'],command=lambda : controller.exitApplication()).grid(row=11,columnspan=3,sticky=W+E+N+S,padx=5,pady=5)


class ProgressFrame(Frame):

    img = None
    pgbar = None
    imgLabel = None

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.controller.progressFrameChild = self

        Label(self,font=("times new roman",20),bg=color['Background'], width=35).grid(row=5,columnspan=3,sticky=W+E+N+S,padx=5,pady=5)

        self.img = Image.open(tempFile)
        self.img = self.img.resize((200,200))
        self.img = ImageTk.PhotoImage(self.img)
        self.imgLabel = Label(self, image = self.img)
        self.imgLabel.grid(row=6,columnspan=3,sticky=W+E+N+S,padx=5,pady=5)
        self.controller.imgLabel = self.imgLabel
        
        self.pgbar = Progressbar(self,length = 100,value=0)
        self.pgbar.grid(row=7,columnspan=3,sticky=W+E+N+S,padx=5,pady=5)
        self.controller.copyingProgressBar = self.pgbar
        
        Button(self,text="Exit",font=("times new roman",15),bg=color['ButtonBG'],fg=color['NormalText'],command=lambda : controller.exitApplication()).grid(row=9,columnspan=3,sticky=W+E+N+S,padx=5,pady=5)
    


class MainPage(Frame):

    chkBtns = []
    values = []
    names = []
    chkMultiple = None
    multipleVal = None
    multipleCopyAllowed = False
    selectedNames = []

    def optionSelected(self,index):
        
        if self.values[index].get()==1:
            self.selectedNames.append(self.names[index])
        elif self.names[index] in self.selectedNames:
            self.selectedNames.remove(self.names[index])

    def isMultipleCopyAllowed(self):

        if self.multipleVal.get()==1:
            self.multipleCopyAllowed=True 
        else:
            self.multipleCopyAllowed=False 


    def beginQuery(self):
        
        print(sys.argv[1])
        print(self.selectedNames)
        print(self.multipleCopyAllowed)
        
        sortIntoFolders(sys.argv[1],self.selectedNames)
        Thread(target=lambda : startSorting(allowMultipleCopy=self.multipleCopyAllowed,UI=self.controller),daemon=True).start()
        self.controller.show_frame("ProgressFrame")


    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        Label(self,font=("times new roman",20),bg=color['Background'], width=30).grid(row=1,columnspan=3,sticky=W+E+N+S,padx=5,pady=5)
        
        self.names = glob(DATASET_FOLDER_PATH+'*')
        self.names = [name[name.rfind('/')+1:] for name in self.names]

        cnt = 6
        self.chkBtns = []
        for name in self.names:
            self.values.append(IntVar())
            chkBtn = Checkbutton(self,text=name,font=("times new roman",15),bg=color['Background'],fg=color['NormalText'],command=lambda index=cnt-6: self.optionSelected(index),variable=self.values[cnt-6])
            chkBtn.grid(row=cnt//3,column=cnt%3,sticky=W+N+S,padx=5,pady=5)
            self.chkBtns.append(chkBtn)
            
            cnt+=1

        self.multipleVal = IntVar()
        chkMultiple = Checkbutton(self,text="Allow Multiple Copies",font=("times new roman",15),bg=color['ButtonBG'],fg=color['NormalText'],command=self.isMultipleCopyAllowed,variable=self.multipleVal)
        chkMultiple.grid(row=(cnt+2)//2,columnspan=3,sticky=W+E+N+S,padx=5,pady=5,ipady=3)

        Button(self,text="Start",font=("times new roman",15),bg=color['ButtonBG'],fg=color['NormalText'],command=self.beginQuery).grid(row=(cnt+2)//2+1,columnspan=3,sticky=W+E+N+S,padx=5,pady=5)
        Button(self,text="Cancel",font=("times new roman",15),bg=color['ButtonBG'],fg=color['NormalText'],command=controller.exitApplication).grid(row=(cnt+2)//2+2,columnspan=3,sticky=W+E+N+S,padx=5,pady=5)
        


if __name__ == "__main__":
    print ('python3 /home/shreyas/Desktop/FaceRecog/main.py '+sys.argv[1])

    # messagebox.showinfo("Information",'python3 /home/shreyas/Desktop/FaceRecog/main.py '+sys.argv[1])
    # messagebox.showerror("Error", "Error message")
    # messagebox.showwarning("Warning","Warning message")
    # exit() 
    app = SampleApp()
    app.geometry(str(windowSize[0])+"x"+str(windowSize[1])+"+"+str(windowLocation[0])+"+"+str(windowLocation[1])+"")
    app.title(windowTitle)
    app.mainloop()


# For UI mode :
# Run this file
# python3 main.py <path-to-folder-containing-images-to-be-sorted>