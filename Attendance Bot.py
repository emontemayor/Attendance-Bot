#!/home/pi/Attendance-Bot

#Import QR Reader support
import QrReader
from awsUpload import updateAWS
import datetime
from datetime import date
import psutil
import requests
import time
from gpiozero import Buzzer
import json

def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)

# function to add to JSON
def write_json(new_data, filename='file-name.json'):
    with open(filename,'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["students"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)


#init buzzer
buzzer = Buzzer(16)

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
studentList.append(Student('Buster Honeywood',  21302672, False))
studentList.append(Student('William Robert',    21287845, False))
studentList.append(Student('Phoenix Johnson',   21254386, False))
studentList.append(Student('Abigail Russell',   21330636, False))
studentList.append(Student('Cole Jones',        21336643, False))
studentList.append(Student('William Burgaard',  21342116, False))
studentList.append(Student('Anthony Cox',       21302678, False))
studentList.append(Student('Brendon Walker',    21335268, False))
studentList.append(Student('Ashtyn Arnold',     21296684, False))
studentList.append(Student('Michael Cook',      21254473, False))
studentList.append(Student('Jessica Spargen',   21313025, False))
studentList.append(Student('Kaleb Wooten',      21297562, False))
studentList.append(Student('Robert Garcia',     21309082, False))
studentList.append(Student('Megan Harty',       21316258, False))
studentList.append(Student('Gracie George',     21310095, False))
studentList.append(Student('Austin Shever',     21308535, False))
studentList.append(Student('Kyle Koeller',      21167052, False))
studentList.append(Student('NIcholas McCormick',21232246, False))
studentList.append(Student('Russel McDaniel',   21263611, False))
studentList.append(Student('Jacob Frazier',     21179663, False))
studentList.append(Student('Cole Wagner',       21156391, False))
studentList.append(Student('Aaron Newton',      21174553, False))
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
    
    data_for_json = {}
    data_for_json['students'] = []
    data_for_json['students'].append({
        'name': '',
        'time': '',
        })
    
    writeToJSONFile('./','file-name',data_for_json) #create json for MagicMirror
    updateAWS()
    
    
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
    print('Awaiting QR code...')
    num = int(QrReader.readQR())                                 #turn on camera and obtain QR code data
    for obj in studentList:                                      #for loop to run through all student objects in studentList
        if num == obj.idNumber and obj.checked == False:         #If ID input matches student ID, and student hasn't checked in, prepare student name for new packet
            
            buzzer.on() #bzz
            time.sleep(.2)
            buzzer.off()
            time.sleep(.2)
            
            data_to_send["name"] = obj.name
            obj.checked = True
            
            data_to_send["time"] = str(datetime.datetime.now().strftime("%H:%M:%S"))  #get time of registration
            data_to_send["bootup"] = "False"                     #let integromat know this is not boot up
            
            studentCount = studentCount - 1                      #lower student count for while loop tracking
            
            data_for_json = {
                'name': obj.name,
                'time': str(datetime.datetime.now().strftime("%H:%M:%S"))
                }
            write_json(data_for_json)
            updateAWS()
                
            print(data_to_send)
            
            #send data packet. Webhooks will add new row to create spreadsheet with student name and time registered.
            r = requests.post("https://hook.integromat.com/g8ddyjvyl69lmivkkcoglwwkll8a1o5h", json = data_to_send)
            print(r.status_code)

        elif num == obj.idNumber and obj.checked == True:        #if student has already checked in, throw message
            print('Student checked already')
            buzzer.on() #bzz
            time.sleep(.1)
            buzzer.off()
            time.sleep(.1)
            buzzer.on() #bzz
            time.sleep(.1)
            buzzer.off()
            time.sleep(.1)
            buzzer.on() #bzz
            time.sleep(.1)
            buzzer.off()
            time.sleep(.1)
            time.sleep(2)


    