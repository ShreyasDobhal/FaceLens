import face_recognition
import cv2
import pickle
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
import random
from glob import glob
# from recognize_faces import recognizeSingleFace,recognizeFacesInImage
from knn_train import recognizeSingleFace, recognizeFacesInImage
# from svm_train import recognizeSingleFace, recognizeFacesInImage
from create_dataset import processFaces
from paths import *

tempFile = TEMP_FILE_PATH
confusionMatrix = None
names = None
nameIndex = None
samples = 25

def showConfusionMatrix():
    global confusionMatrix, names
    
    ind = [name for name in names]
    col = [name for name in names]

    ind.append('Unknown')
    
    df_cm = pd.DataFrame(confusionMatrix, index = ind,columns = col)
    sn.set(font_scale=1.4) # label size
    sn.heatmap(df_cm, annot=True, annot_kws={"size": 16}) # font size
    plt.show()

def initilize():
    global names,nameIndex,confusionMatrix

    nameIndex = {}
    names = glob(DATASET_FOLDER_PATH+'*')
    for i in range(0,len(names)):
        names[i] = names[i][names[i].rfind('/')+1:]
        nameIndex[names[i]]=i
    nameIndex['Unknown']=len(names)
    
    confusionMatrix = [[0 for i in range(len(nameIndex)-1)] for j in range(len(nameIndex))] 


def startTest():
    global confusionMatrix, names, nameIndex
    
    total = 0
    testX = []
    testY = []
    index = []
    i = 0
    
    for name in names:
        images = glob(DATASET_FOLDER_PATH+name+"/*.jpg")
        images = random.sample(images,min(samples,len(images)))
        testX.extend(images)
        testY.extend([name]*len(images))
        index.extend(list(range(i,i+len(images))))
        i+=len(images)
    
    random.shuffle(index)
    
    correct = 0
    wrong = 0
    total = len(index)

    print(total)
    count = 0
    for i in index:
        print("Progress %.1f %%"%(count/total*100))

        curName = recognizeSingleFace(testX[i])

        confusionMatrix[nameIndex[curName]][nameIndex[testY[i]]]+=1

        if (curName==testY[i]):
            correct+=1
        else:
            wrong+=1
        count+=1
        
    print ("Correct : "+str(correct))
    print ("Wrong : "+str(wrong))
    print ("Accuracy : "+str(correct/total*100))
    
    showConfusionMatrix()

def testFacialRecognition():
    files = glob(TEST_DATA_PATH+'*.jpg')
    for filename in files:
        print(filename)
        recognizeFacesInImage(filename)

# This file helps in measuring performance of face recognition
# Uncomment one of the import statments to measure its performance

initilize()
startTest() # works on single extracted faces and creates confusion matrix
# testFacialRecognition() # works on a folder