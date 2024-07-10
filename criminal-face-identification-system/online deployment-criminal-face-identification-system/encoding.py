import os
import cv2
import face_recognition
import json
import numpy

class Encode:
    def __init__(self, path):
        self.path = path
        self.images = []
        self.classNames = []
        self.myList = os.listdir(self.path)
        self.encodeList = []
        
    def names(self):
        for cl in self.myList:
            curImg = cv2.imread(f'{self.path}/{cl}')
            self.images.append(curImg)
            self.classNames.append(os.path.splitext(cl)[0])
            
        return self.classNames
            
    def findEncodings(self):
        for img in self.images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            self.encodeList.append(encode)
            
        return self.encodeList
    
    def save(self):
        clist = []
        for i in range(len(self.classNames)):
            clist.append(self.encodeList[i].tolist())
        
        data = {"encodeList":clist, "classNames":self.classNames}
        with open("./database/encodings.json", 'w') as file:
            json.dump(data, file)