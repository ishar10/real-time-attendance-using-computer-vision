import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path="images"
images=[]
classnames=[]
mylist=os.listdir(path)
for cls in mylist:
    currimg=cv2.imread(f"{path}/{cls}")
    images.append(currimg)
    classnames.append(os.path.splitext(cls)[0])
print(classnames)
def findencodeings(images):
    encodelist=[]
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist
def markattendance(name):
    with open("attendance.csv","r+") as f:
        mydatalist=f.readlines()
        namelist=[]
        for line in mydatalist:
            entry=line.split(",")
            namelist.append(entry[0])
        if name not in namelist:
            now=datetime.now()
            dtstring=now.strftime("%H:%M:%S")
            f.writelines(f"\n{name},{dtstring}")

encodelistknow=findencodeings(images)
print("encoding complete...")
cap=cv2.VideoCapture(0)
while True:
    success,img=cap.read()
    imgsmall=cv2.resize(img,(0,0),None,0.5,0.5) #scaled down
    img = cv2.cvtColor(imgsmall, cv2.COLOR_BGR2RGB)

    faceloc = face_recognition.face_locations(imgsmall)
    encode = face_recognition.face_encodings(imgsmall,faceloc)

    for encodeface,facelocc in zip(encode,faceloc):
        matches=face_recognition.compare_faces(encodelistknow,encodeface)
        facedis=face_recognition.face_distance(encodelistknow,encodeface)
        #print(facedis)
        matchindex=np.argmin(facedis)
        if matches[matchindex]:
            name=classnames[matchindex].upper()
            #print(name)
            y1,x2,y2,x1=facelocc
            # y1, x2, y2, x1=y1*2,x2*2,y2*2,x1*2 #scaled up
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markattendance(name)
    cv2.imshow("webcam",img)
    cv2.waitKey(1)





# faceloc=face_recognition.face_locations(imgelon)[0]
# encodeelon=face_recognition.face_encodings(imgelon)[0]
# cv2.rectangle(imgelon,(faceloc[3],faceloc[0]),(faceloc[1],faceloc[2]),(255,0,255),2)
#
# faceloctest=face_recognition.face_locations(imgtest)[0]
# encodeelontest=face_recognition.face_encodings(imgtest)[0]
# cv2.rectangle(imgtest,(faceloctest[3],faceloctest[0]),(faceloctest[1],faceloctest[2]),(255,0,255),2)
#
#
# results=face_recognition.compare_faces([encodeelon],encodeelontest)
# facedistance=face_recognition.face_distance([encodeelon],encodeelontest)