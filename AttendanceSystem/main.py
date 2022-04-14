import face_recognition
from datetime import datetime as dt
import cv2
import numpy as np
import os
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

home_page = tk.Tk()
home_page.geometry('1280x720')
home_page.title("Attendace System")
home_page.minsize(480,480)
home_page.configure(background = 'black')

frame1 = tk.Frame(home_page, bg = 'black')
frame1.place(relx = 0.11,rely = 0, relwidth = 0.80, relheight = 0.118)
frame2 = tk.Frame(home_page,bg= 'black')
frame2.place(relx = 0.11,rely = 0.12, relwidth = 0.80, relheight = 0.12)
frame3 = tk.Frame(home_page, bg = 'black')
frame3.place(relx = 0.11,rely = 0.24, relwidth = 0.80, relheight = 0.56) 
frame4 = tk.Frame(home_page, bg = 'black')
frame4.place(relx = 0.11,rely = 0.80, relwidth = 0.80, relheight = 0.2)

l1 = tk.Label(master= frame1,text = "Attendance System",bg = 'black', fg = "white",font = ('verdana',28,'bold'))
l1.pack(anchor = 'center',pady = 5 )
l2 = tk.Label(master=frame1,text="",font = ('verdana',14,'bold'),bg = "black", fg = "white")
l2.pack(anchor = 'e',side = 'right',pady = 1)
################################## TIMER #######################################
def timer():
    now =  (dt.now()).strftime('%H:%M:%S')
    l2.config(text = now)
    l2.after(1000,timer)
timer()
def read_face():
    abc = face_reader()
    abc.start_face_reading(encodedListKnowFace,classNames)

button1 = tk.Button(frame2,text = "Make Attendance",command = read_face,bg = 'black',bd = "4", fg = "white",font = ('verdana',20,'bold'))
button1.pack(anchor = 'center',pady = 20)

tree = ttk.Treeview(frame3)
tree["columns"] = ("one","two")
tree.column("#0",width = 1)
tree.column("one",width = 125,anchor = 'center')
tree.column("two",width = 200,anchor = 'center')

tree.heading("one", text='Name')
tree.heading("two",text='Login time')
tree.pack()

button2 = tk.Button(frame4,text = "Quit",command = home_page.quit,bg = 'black',bd = "4",  fg = "white",font = ('verdana',20,'bold'),height = 1,width = 7)
button2.pack(anchor = 'e',side= "bottom",pady = 20,padx = 30)
############################################ Code for Face recoginition ###########################################
path = '\images' ##### Create folder with name as "images" and add the images of student. The name of images file is of person's name  
images = []
classNames = []
mylist = os.listdir(path)
if len(mylist) == 0:
    messagebox.showinfo("Error!!!","No any is registered \nPlease go to Image directory and \nSave image with image name is \nsame as Student name..")
    home_page.destroy()
for cls in mylist:
    curimage = cv2.imread(f'{path}/{cls}')
    images.append(curimage)
    classNames.append(os.path.splitext(cls)[0])
def find_Encoding(images):
    encodedList = []
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodedList.append(encode)
    return encodedList
encodedListKnowFace = find_Encoding(images)
class face_reader:
    def start_face_reading(self,encodedListKnowFace,classNames):
        cap = cv2.VideoCapture(0)
        while True:
            success, img = cap.read()  
            imgs = cv2.resize(img,(0,0),None,0.25,0.25)
            imgs = cv2.cvtColor(imgs,cv2.COLOR_BGR2RGB)
            facesInFrame = face_recognition.face_locations(imgs)
            encodefacesInFrame = face_recognition.face_encodings(imgs,facesInFrame)     
            for encodeface, faceloc_Cap in zip(encodefacesInFrame,facesInFrame):
                matches = face_recognition.compare_faces(encodedListKnowFace,encodeface)
                facedis = face_recognition.face_distance(encodedListKnowFace,encodeface)
                matchIndex = np.argmin(facedis)
                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()
                    y1, x2, y2, x1 = faceloc_Cap
                    y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4 
                    cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                    cv2.putText(img,name,(x1-6,y2+25),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)        
            cv2.imshow('WebCam',img)
            key = cv2.waitKey(1)
            if key == ord('q') or key == ord('Q'):
                self.markAttendance(name)
                now = dt.now()
                dtString = now.strftime('%H:%M:%S')
                tree.insert('','end',text = "0", value = (name,dtString))
                cap.release()
                cv2.destroyAllWindows()
                break
    def markAttendance(self,name):
        with open('AttendanceFile.csv','r+') as f:
            myDataList = f.readlines()
            nameList = []           
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
            if name not in nameList:
                now = dt.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'{name},{dtString}\n')
home_page.mainloop()
