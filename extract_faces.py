import face_recognition
import cv2
from PIL import Image, ExifTags
from glob import glob
import random
from paths import *
from accepted_extensions import IMAGE_FILES
from image_edit import preprocessImage

face_cascade = cv2.CascadeClassifier(FACE_CASCADE_XML_FILE_PATH)

savePath = FACES_FOLDER_PATH
loadPath = RAW_IMAGES_FOLDER_PATH
tempFile = TEMP_FILE_PATH
faceCnt = 1000

def changeboxtype(boxes):
    newbox = []
    for box in boxes:
        x,y,w,h = box
        newbox.append((x,y,x+w,y+h))
    return newbox

def cropImage(filename,box,save=False, newfilename='newimg.jpg'):
    img = Image.open(filename)
    w,h = img.size 
    a,b,c,d = box
    if a<=c and b<=d:
        img1 = img.crop((max(a-20,0),max(b-20,0),min(c+20,w-1),min(d+20,h-1)))
    else:
        img1 = img.crop((max(d-20,0),max(a-20,0),min(b+20,w-1),min(c+20,h-1)))
    # img1.show()
    if save:
        img1.save(newfilename)


def extractFaces1(filename):
    global faceCnt
    preprocessImage(filename)

    face_locations = changeboxtype(face_cascade.detectMultiScale(cv2.imread(tempFile), 1.7, 5))

    print (face_locations)

    # img = Image.open(tempFile)
    # img.save(savePath+str(faceCnt)+'.jpg')
    # faceCnt+=1

    for face_location in face_locations:
        cropImage(tempFile,face_location,True,savePath+str(faceCnt)+'.jpg')
        faceCnt+=1

def extractFaces2(filename):
    global faceCnt
    preprocessImage(filename)

    # img = Image.open(tempFile)
    # scale = 0.5
    # width, height = img.size
    # newsize = (int(width*scale), int(height*scale))
    # img = img.resize(newsize)
    # img.save(tempFile)

    image = face_recognition.load_image_file(tempFile)
    face_locations = face_recognition.face_locations(image)

    print (face_locations)

    # img = Image.open(tempFile)
    # img.save(savePath+str(faceCnt)+'.jpg')
    # faceCnt+=1

    for face_location in face_locations:
        cropImage(tempFile,face_location,True,savePath+str(faceCnt)+'.jpg')
        faceCnt+=1

def extractAllFaces(folderspath=loadPath):
    files = []
    for folderpath in folderspath:
        if folderpath[-1]!='/':
            folderpath+='/'
        for ext in IMAGE_FILES:
            files.extend(glob(folderpath+ext))
        
    files = random.sample(files,min(250,len(files)))
    total = len(files)
    count = 0
    print ('Total : '+str(total))
    for filename in files:
        print(filename)
        print('Progress : %.2f %%'%(count/total*100))
        extractFaces2(filename)
        count+=1

# Use this to extract faces from images stored in RAW_IMAGES_FOLDER_PATH and save the cropped faces in FACES_FOLDER_PATH
extractAllFaces()