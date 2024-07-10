import cv2
import sqlite3

detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)

def insertOrUpdate(Id, Name, Crime, Gender):
    conn = sqlite3.connect("criminal.db")
    cmd = "SELECT * FROM People WHERE ID=" + str(Id)
    cursor = conn.execute(cmd)
    isRecordExists = 0
    for row in cursor:
        isRecordExists = 1
    if isRecordExists == 1:
        cmd = "UPDATE People SET Name='" + str(Name) + "', Gender='" + str(Gender) + "', Crime='" + str(Crime) + "' WHERE ID=" + str(Id)
    else:
        cmd = "INSERT INTO People(ID, Name, Gender, Crime) VALUES('" + str(Id) + "','" + str(Name) + "','" + str(Gender) + "','" + str(Crime) + "')"
    conn.execute(cmd)
    conn.commit()
    conn.close()

Id = input('Enter ID: ')
Name = input('Enter Name: ')
Crime = input('Enter Crime convicted: ')
Gender = input('Enter Gender: ')
insertOrUpdate(Id, Name, Crime, Gender)
sampleNum = 0
while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # incrementing sample number 
        sampleNum = sampleNum + 1
        # saving the captured face in the dataset folder
        cv2.imwrite("dataSet/User." + str(Id) + '.' + str(sampleNum) + ".jpg", gray[y:y+h, x:x+w])
        cv2.waitKey(100)

    cv2.imshow('face', img)
    # wait for 100 milliseconds 
    cv2.waitKey(1)
    # break if the sample number is more than 20
    if sampleNum > 20:
        break
cam.release()
cv2.destroyAllWindows()
