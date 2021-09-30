#!/home/pi/Attendance-Bot

#Import QR Reader support
import QrReader
import datetime
from datetime import date
import psutil
import requests
import time

#bootup tracker set to true
bootup = True

#Student class, used to create student objects.
#  name: student name
#  idNumber: student ID
#  checked: boolean to determine if student already checked in. True = checked in, False = not checked in
class Student:
    def __init__(self, name, idNumber, checked):
        self.name = name
        self.idNumber = idNumber
        self.checked = checked
        
    def introduce_self(self):
        print ("my name is " + self.name)

#Student list, populated by Student objects. Students names obtained from class roster.
studentList = []
studentList.append(Student('Buster Honeywood',  0, False))
studentList.append(Student('William Robert',    1, False))
studentList.append(Student('Phoenix Johnson',   2, False))
studentList.append(Student('Abigail Russell',   3, False))
studentList.append(Student('Cole Jones',        4, False))
studentList.append(Student('William Burgaard',  5, False))
studentList.append(Student('Anthony Cox',       6, False))
studentList.append(Student('Brendon Walker',    7, False))
studentList.append(Student('Ashtyn Arnold',     8, False))
studentList.append(Student('Michael Cook',      9, False))
studentList.append(Student('Jessica Spargen',   10, False))
studentList.append(Student('Kaleb Wooten',      11, False))
studentList.append(Student('Robert Garcia',     12, False))
studentList.append(Student('Megan Harty',       13, False))
studentList.append(Student('Gracie George',     14, False))
studentList.append(Student('Austin Shever',     15, False))
studentList.append(Student('Kyle Koeller',      16, False))
studentList.append(Student('NIcholas McCormick',17, False))
studentList.append(Student('Russel McDaniel',   18, False))
studentList.append(Student('Jacob Frazier',     19, False))
studentList.append(Student('Cole Wagner',       20, False))
studentList.append(Student('Aaron Newton',      21, False))
studentList.append(Student('Emil Montemayor',      22, False))
studentList.append(Student('Dr. Jason "Bossman" Ferguson',      23, False))

#studentCount to track total number of students.
studentCount = len(studentList)

#Initialize spreadSheetID. 
spreadSheetID = 0

#If this is the first run since bootup, initialize data packet for Webhooks
if(bootup):
    data_to_send = {}                        #data packet container 
    data_to_send["date"] = str(date.today()) #date 
    data_to_send["bootup"] = "True"          #bootup tracker
    data_to_send["time"] = "nuller"          #current time
    data_to_send["name"] = "nuller"          #name of student
    data_to_send["spreadID"] = "nuller"      #spreadsheet ID generated during boot up.
    
    #send initialization packet to Integromat
    r = requests.post("https://hook.integromat.com/g8ddyjvyl69lmivkkcoglwwkll8a1o5h", json = data_to_send)
    #webhooks will create a google sheet.
    
    print(r.status_code)
    print(data_to_send)
    
    time.sleep(5)                            #Give webhooks time to respond with spread ID [done in integromat]
    
    spreadSheetID = r.text                   #Obtain spreadsheet ID
    print(spreadSheetID)
    data_to_send["spreadID"] = spreadSheetID #add spreadsheet ID to data packet

    bootup = False                           #flip bootup tracker


#Continue while loop until all students have registered
while(studentCount != 0):     
    num = int(QrReader.readQR())                                  #temporary input for ID
    for obj in studentList:                              #for loop to run through all student objects in studentList
        if num == obj.idNumber and obj.checked == False:         #If ID input matches student ID, and student hasn't checked in, prepare student name for new packet
            data_to_send["name"] = obj.name
            obj.checked = True
            
            data_to_send["time"] = str(datetime.datetime.now())  #get time of registration
            data_to_send["bootup"] = "False"                     #let integromat know this is not boot up
            
            studentCount = studentCount - 1                      #lower student count for while loop tracking
            
            print(data_to_send)
            
            #send data packet. Webhooks will add new row to create spreadsheet with student name and time registered.
            r = requests.post("https://hook.integromat.com/g8ddyjvyl69lmivkkcoglwwkll8a1o5h", json = data_to_send)
            print(r.status_code)

        elif num == obj.idNumber and obj.checked == True:        #if student has already checked in, throw message
            print('Student checked already')



    