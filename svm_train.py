from sklearn.svm import SVC
from sklearn.model_selection import train_test_split 
import face_recognition
import cv2
import seaborn as sn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
from glob import glob
from create_dataset import processFaces
from image_edit import preprocessImage
from paths import *

clf = None
X_train = []
X_test = []
Y_train = []
Y_test = []
confusionMatrix = None
names = None
nameIndex = None


tempFile = TEMP_FILE_PATH
data = {}


def showConfusionMatrix():
    global confusionMatrix, names
    
    ind = [name for name in names]
    col = [name for name in names]

    ind.append('Unknown')
    
    df_cm = pd.DataFrame(confusionMatrix, index = ind,columns = col)
    sn.set(font_scale=1.4) # label size
    sn.heatmap(df_cm, annot=True, annot_kws={"size": 16}) # font size
    plt.show()


def loadData():
    global data,names,nameIndex,confusionMatrix

    if len(glob(PICKLED_DATA_FILE_PATH))==0:
        processFaces()
    pklfile = open(PICKLED_DATA_FILE_PATH,'rb')
    data = pickle.load(pklfile)

    nameIndex = {}
    names = glob(DATASET_FOLDER_PATH+'*')
    for i in range(0,len(names)):
        names[i] = names[i][names[i].rfind('/')+1:]
        nameIndex[names[i]]=i
    nameIndex['Unknown']=len(names)
    
    confusionMatrix = [[0 for i in range(len(nameIndex)-1)] for j in range(len(nameIndex))] 

    print("Data loaded")

def trainModel():
    global data, clf
    global X_train,Y_train,X_test,Y_test

    X = data['encodings']
    Y = data['names']

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state=42) 

    X_train = np.array(X_train)
    X_test = np.array(X_test)
    Y_train = np.array(Y_train)
    Y_test = np.array(Y_test)


    # knn = KNeighborsClassifier(n_neighbors=7) 
    clf = SVC(kernel='rbf') 
    clf.fit(X_train, Y_train) 

    print ("Model trained")

def testModel():
    global clf
    global X_test
    global names,nameIndex,confusionMatrix

    Y_out = clf.predict(X_test)
    # prob = clf.predict_proba(X_test)
    
    total = 0
    correct = 0
    wrong = 0
    for i in range(0,len(Y_test)):
        if (Y_test[i]==Y_out[i]):
            correct+=1
        else:
            wrong+=1
        confusionMatrix[nameIndex[Y_out[i]]][nameIndex[Y_test[i]]]+=1
        total+=1
    
    print ("Correct : "+str(correct))
    print ("Wrong : "+str(wrong))
    print ("Accuracy : "+str(correct/total*100))
    
    showConfusionMatrix()


def recognizeSingleFace(filename):
    global clf
    global data,names

    preprocessImage(filename)

    img = cv2.imread(tempFile)
    rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    boxes = face_recognition.face_locations(rgb)
    encoding = face_recognition.face_encodings(rgb,boxes)
    
    if len(encoding)==0:
        return 'Unknown'
    
    encoding = encoding[0]
    encoding = np.array(encoding)

    face = clf.predict([encoding])[0]
    # prob = knn.predict_proba([encoding])[0]
    # print(prob)
    return face

def recognizeFacesInImage(filename):
    global data,names

    preprocessImage(filename)
    
    img = cv2.imread(tempFile)
    rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    
    boxes = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb,boxes)

    faces = []
    if len(encodings)!=0:
        encodings = np.array(encodings)
        faces = clf.predict(encodings)
    faces = list(set(faces))

    print (faces)
    return faces


loadData()
trainModel()
# testModel()
