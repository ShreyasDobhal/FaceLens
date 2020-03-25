import face_recognition
import cv2 
import pickle
from PIL import Image, ExifTags
from glob import glob
from create_dataset import processFaces
from image_edit import preprocessImage
from paths import *

tempFile = TEMP_FILE_PATH
data = {}
names = {}
totalFreq = {}

def loadData():
    global data,names, totalFreq

    if len(glob(PICKLED_DATA_FILE_PATH))==0:
        processFaces()
    pklfile = open(PICKLED_DATA_FILE_PATH,'rb')
    data = pickle.load(pklfile)

    names = glob(DATASET_FOLDER_PATH+'*')
    for i in range(0,len(names)):
        names[i] = names[i][names[i].rfind('/')+1:]

    for name in names:
        totalFreq[name]=0

    for name in data['names']:
        totalFreq[name]+=1
    
    print("Data loaded")

def recognizeSingleFace(filename):
    global data,names, totalFreq

    preprocessImage(filename)

    img = cv2.imread(tempFile)
    rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    boxes = face_recognition.face_locations(rgb)
    encoding = face_recognition.face_encodings(rgb,boxes)

    if len(encoding)==0:
        return 'Unknown'
    
    encoding = encoding[0]
    matches = face_recognition.compare_faces(data['encodings'],encoding)
        
    freq = {}
    percent = {}

    for name in names:
        freq[name]=0
    
    for i in range(0,len(matches)):
        if (matches[i]):
            freq[data['names'][i]]+=1

    for name in names:
        percent[name]=float('%.2f'%(freq[name]/totalFreq[name]*100))

    curMax = 90
    curName = 'Unknown'
    for name in names:
        if percent[name]>=curMax:
            curMax=percent[name]
            curName=name
    
    face=curName

    return face
    

def recognizeFacesInImage(filename):
    global data,names, totalFreq

    preprocessImage(filename)
    
    img = cv2.imread(tempFile)
    rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    
    boxes = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb,boxes)

    faces = []
    for encoding in encodings:
        matches = face_recognition.compare_faces(data['encodings'],encoding)
        
        freq = {}
        percent = {}

        for name in names:
            freq[name]=0
        
        
        for i in range(0,len(matches)):
            if (matches[i]):
                freq[data['names'][i]]+=1

        for name in names:
            percent[name]=float('%.2f'%(freq[name]/totalFreq[name]*100))

        curMax = 90
        curName = 'Unknown'
        for name in names:
            if percent[name]>=curMax:
                curMax=percent[name]
                curName=name
        
        if (curName in faces)==False:
            faces.append(curName)
    print(faces)

    return faces
      
loadData()