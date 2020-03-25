import face_recognition
import cv2
import pickle
from glob import glob 
import random
from paths import *

trainX = []
trainY = []
dataset = {}

def processFaces():
    global trainX, trainY, dataset

    names = glob(DATASET_FOLDER_PATH+'*')
    for i in range(0,len(names)):
        names[i] = names[i][names[i].rfind('/')+1:]
    
    total = 0
    for name in names:
        images = glob(DATASET_FOLDER_PATH+name+"/*.jpg")
        l = 50
        if len(images)>=100:
            l = 100
        else:
            l = min(l,len(images))
        images = random.sample(images,l)
        total += l
        dataset[name] = images
    
    count = 0
    for name in names:
        print(name)
        for imagepath in dataset[name]:
            print("Progress %.2f %%"%(count/total*100))
            img = cv2.imread(imagepath)
            rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            box = face_recognition.face_locations(rgb)
            if len(box)==0:
                count+=1
                continue
            encd = face_recognition.face_encodings(rgb,box)[0]
            trainX.append(encd)
            trainY.append(name)
            count+=1
            # break

    print("Processing completed")
    data = {'encodings':trainX,'names':trainY}
    pklfile = open(PICKLED_DATA_FILE_PATH,'wb')
    pickle.dump(data,pklfile)
    pklfile.close()
    print("Processed information stored in pickle file "+PICKLED_DATA_FILE_PATH)
        
# To create your own dataset, place your extracted face images in their corresponding folder (with corresponding name) in DATASET_FOLDER_PATH
# And run this file