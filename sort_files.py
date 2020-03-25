from recognize_faces import recognizeFacesInImage as dnn
from knn_train import recognizeFacesInImage as knn
from svm_train import recognizeFacesInImage as svm
from threading import Thread
from shutil import copyfile
import os
from glob import glob
from accepted_extensions import IMAGE_FILES
from paths import *
from time import sleep

foldernames = []
currentfolderpath = ''
conflictFiles = []
conflictWithFiles = []
faceRecognitionMethod = knn
total = 0
files = []

def sortIntoFolders(currentfolder, folders):
    global foldernames,currentfolderpath

    foldernames = folders
    currentfolderpath = currentfolder
    if currentfolderpath[-1]!='/':
        currentfolderpath+='/'

    for folder in foldernames:
        try:
            os.mkdir(currentfolderpath+folder)
        except:
            print("Folder "+folder+" already exists")

def handleConflictFiles(UI=None):
    global total

    if UI!=None:
        if UI.isApplicationClosed():
            exit()
        UI.setConflictHandleFrame()
    

    total = len(conflictFiles)
    count = 0
    userResponse = 'UNDEFINED'

    for i in range(0,total):
        print ("Process %.2f %%"%(count/total*100))
        print ("Waiting for user response")
        if UI!=None:
            if UI.isApplicationClosed():
                exit()
            UI.setProgress(count/total*100)
            UI.setConflictImages(conflictWithFiles[i],conflictFiles[i])


            if UI.getApplySameResponseValue()==False or userResponse=='UNDEFINED':
                UI.setUserResponse(value=None)
                while UI.getUserResponse()==None:
                    sleep(0.1)
                if UI.getUserResponse()==UI.REPLACE:
                    userResponse='REPLACE'
                else:
                    userResponse='SKIP'
        else:
            # No UI available
            print(conflictWithFiles[i],conflictFiles[i])
            userResponse = input('Enter REPLACE or SKIP : ')
            
        if userResponse=='REPLACE':
            print("Replacing file")
            copyfile(conflictFiles[i],conflictWithFiles[i])
            if conflictFiles[i] not in conflictFiles[i+1:]:
                os.remove(conflictFiles[i])
        else:
            print("Skipping this file")
        count+=1
    
    print("Finished")

def startSorting(method='knn',allowMultipleCopy=True,UI=None):
    global faceRecognitionMethod
    global total, files, conflictFiles, conflictWithFiles


    if method=='knn':
        faceRecognitionMethod=knn
    elif method=='dnn':
        faceRecognitionMethod=dnn
    elif method=='svm':
        faceRecognitionMethod=svm
    
    files = []
    conflictFiles = []
    conflictWithFiles = []


    for ext in IMAGE_FILES:
        files.extend(glob(currentfolderpath+ext))
    total = len(files)

    count = 0
    for filename in files:
        print("Process %.2f %%"%(count/total*100))

        if UI!=None:
            if UI.isApplicationClosed():
                exit()
            UI.setProgress(count/total*100)
            UI.setDisplayImage(filename)
        
        faces = faceRecognitionMethod(filename)
        imgname = filename[filename.rfind('/')+1:]

        isCopied = False
        for foldername in foldernames:
            if foldername in faces:
                # Save this image there
                if len(glob(currentfolderpath+foldername+'/'+imgname))==0:
                    # Copy the image
                    copyfile(filename, currentfolderpath+foldername+'/'+imgname)
                    isCopied = True
                else:
                    # File with same name already exists
                    conflictFiles.append(filename)
                    conflictWithFiles.append(currentfolderpath+foldername+'/'+imgname)
                if allowMultipleCopy==False:
                    break
        
        if UI!=None:
            if UI.isApplicationClosed():
                exit()
            UI.setProgress(100)

        if isCopied:
            # File is copied somewhere delete the original file
            os.remove(filename)
        count+=1
    
    print ("Copying finished")
    print ("Handling conflicts")
    handleConflictFiles(UI)

    print ("Exiting Application")

    if UI!=None:
        if UI.isApplicationClosed():
            exit()
        UI.exitApplication()
        exit()
    exit()
    print ("Done")


# To run in non UI mode 

# sortingOrder = ['Shreyas']
# sortIntoFolders('/home/shreyas/Desktop/FaceRecog/Test/',sortingOrder)
# startSorting(allowMultipleCopy=False)

