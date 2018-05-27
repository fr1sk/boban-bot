import sys, i18n, os
sys.path.append('../../') 
import api.utils.qrHandler as qr
import api.utils.functions as f
import api.utils.map as m
import settings as s

import time
from fbmq import Template, Attachment
from pymessenger2.bot import Bot
line = []
# import api.models.student as Student

def isImage(data):
    if data['object'] == 'page':
        for entry in data['entry']:
            if entry.get('messaging'):
                for messaging in entry['messaging']:
                    senderId = messaging['sender']['id']
                    if messaging.get('message'):
                        if 'attachments' in messaging['message']:
                            if messaging['message']['attachments'][0]['type'] == 'image':
                                print "URL: ", messaging['message']['attachments'][0]['payload']['url']
                                return True, senderId, messaging['message']['attachments'][0]['payload']['url']
 
                    return False, senderId, None
    return None, None, None

def isLocation(data):
    if data['object'] == 'page':
        for entry in data['entry']:
            if entry.get('messaging'):
                for messaging in entry['messaging']:
                    senderId = messaging['sender']['id']
                    if messaging.get('message'):
                        if 'attachments' in messaging['message']:
                            if messaging['message']['attachments'][0]['type'] == 'location':
                                lat = messaging['message']['attachments'][0]['payload']['coordinates']['lat']
                                long = messaging['message']['attachments'][0]['payload']['coordinates']['long']
                                return True, senderId, lat, long
 
                    return False, senderId, None, None
    return None, None, None, None

def handleImage(page, senderId, url):
    img = qr.loadImgFromUrl(url)
    qrRes = qr.decodeQrFromImg(img)
    if qrRes:
        for obj in qrRes:
            if obj.type == 'QRCODE':
                print senderId, 'QR DATA: ', obj.data, os.environ['BOBAN_QR'],obj.data == os.environ['BOBAN_QR']
                print os.environ['BOBAN_QR']
                if obj.data == os.environ['BOBAN_QR']:
                    addUserToQueue(page, senderId)
                else:
                    page.send(senderId, f.readTextFromYML('qrResults.badQR'))
                return
    page.send(senderId, f.readTextFromYML('qrResults.noQR'))

def getStartedHandler(page, senderId):
    gender, fName, lName, pic = f.getUserInfo(senderId, os.environ['PAGE_ACCESS_TOKEN'])
    Student = s.mongo.db.students 
    
    if Student.count({'senderId':senderId}) != 1:
        student = {
            'lastName': lName,
            'firstName': fName,
            'gender': gender,
            'photo': pic,
            'inQueue': False,
            'senderId': senderId
        }
        Student.insert(student)
        Student.save(student)
        print '=> STUDENT SAVED', senderId
    else:
        print '=> STUDENT ALREADY EXISTS', senderId
    
    page.typing_on(senderId)
    page.send(senderId, f.readTextFromYML('getStartedButton.text', ime = fName))
    firstMessage(page, senderId)

def firstMessage(page, senderId):
    buttons = [
        Template.ButtonPostBack(f.readTextFromYML('firstMsg.btn1'), f.readTextFromYML('firstMsg.pl1')),
        Template.ButtonPostBack(f.readTextFromYML('firstMsg.btn2'), f.readTextFromYML('firstMsg.pl2'))
    ]
    page.send(senderId, Template.Buttons(f.readTextFromYML('firstMsg.text'), buttons))
    page.typing_off(senderId)

def sendHelp(page, senderId):
    buttons = [
        Template.ButtonPhoneNumber(f.readTextFromYML('helpMsg.btn1'), f.readTextFromYML('helpMsg.pl1')),
        Template.ButtonPostBack(f.readTextFromYML('helpMsg.btn2'), f.readTextFromYML('helpMsg.pl2'))
    ]
    bot = Bot(os.environ['PAGE_ACCESS_TOKEN'])
    bot.send_image_url(senderId, "https://media.giphy.com/media/l2SqdshrUqCFMEZkk/giphy.gif")
    # f.sendImage(senderId, os.environ['HELP_IMG'])
    page.typing_on(senderId)
    page.send(senderId, f.readTextFromYML('helpMsg.text0'))
    time.sleep(2) 
    page.send(senderId, f.readTextFromYML('helpMsg.text1'))
    time.sleep(1) 
    page.send(senderId, f.readTextFromYML('helpMsg.text2'))
    time.sleep(1)
    page.typing_off(senderId) 
    page.send(senderId, Template.Buttons(f.readTextFromYML('helpMsg.text3'), buttons))

def sendQueueInfo(page, senderId):
    page.send(senderId, f.readTextFromYML('scanQr.text'))


def handleLocation(page, senderId, lat, long):
    loc, time = m.getLocationData(lat, long)
    page.send(senderId, "Sa tvoje lokacije, "+loc + ", treba ti " + time + " do Bobana! :)")
    addTimeToDB(page, senderId, time)

def addTimeToDB(page, senderId, time):
    Student = s.mongo.db.students
    student = Student.find_one({'senderId': str(senderId)})
    student['time'] = str(int(time))
    Student.save(student)


def addUserToQueue(page, senderId):
    Student = s.mongo.db.students
    student = Student.find_one({'senderId': str(senderId)})
    print bool(student['inQueue']), student['inQueue'], student['inQueue'] == True 
    if bool(student['inQueue']):
        page.send(senderId, f.readTextFromYML('leaveQueue.text'))
    else:
        student['inQueue'] = True
        Student.save(student)
        line.append(str(senderId))
        print line
        page.typing_on(senderId)
        time.sleep(2)
        page.send(senderId, f.readTextFromYML('qrResults.success'))
        time.sleep(1)
        page.send(senderId, "Trenutno si "+str(len(line)) +". u redu :)")
        # time.sleep(1)
        # page.send(senderId, f.readTextFromYML('qrResults.after'))
        # time.sleep(1)
        #  page.send(senderId, f.readTextFromYML('qrResults.index')) 

        time.sleep(1)
        if len(line) == 1:
            page.send(senderId, f.readTextFromYML('queue.first')) 
        else:
            numOfStudents = len(line) - 1
            waitTime = numOfStudents * 3
            page.send(senderId, 
                "Trenutno je ispred tebe "+str(numOfStudents)+" studenta, procenjeno vreme cekanja je "+str(waitTime)+" minuta")
            page.send(senderId, f.readTextFromYML('queue.location'))

        page.typing_off(senderId)

def removeUserFromQueue(page, senderId):
    Student = s.mongo.db.students
    student = Student.find_one({'senderId': str(senderId)})
    print bool(student['inQueue']), student['inQueue'], student['inQueue'] == True 
    if bool(student['inQueue']):
        student['inQueue'] = False
        Student.save(student)
        line.remove(senderId)
        
        print line
        page.typing_on(senderId)
        time.sleep(2)
        page.send(senderId, f.readTextFromYML('queueLeft.text'))
        page.typing_off(senderId)
    else:
        page.send(senderId, f.readTextFromYML('notInQueue.text'))
        
