import sys, i18n, os
sys.path.append('../../') 
import api.utils.qrHandler as qr
import api.utils.functions as f
import api.utils.map as m

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

def handleImage(page, senderId, url):
    img = qr.loadImgFromUrl(url)
    qrRes = qr.decodeQrFromImg(img)
    if qrRes:
        for obj in qrRes:
            if obj.type == 'QRCODE':
                page.send(senderId, 'QR DATA: ' + obj.data)
    else:
        page.send(senderId, f.readTextFromYML('qrResults.noQR'))

def getStartedHandler(page, senderId):
    gender, fName, lName, pic = f.getUserInfo(senderId, os.environ['PAGE_ACCESS_TOKEN'])
    page.send(senderId, f.readTextFromYML('getStartedButton.text', ime = fName))

def handleLocation(page, senderId, lat, long):
    loc, time = m.getLocationData(lat, long)
    page.send(senderId, "Sa tvoje lokacije, "+loc + ", treba ti " + time + " do Bobana! :)")
