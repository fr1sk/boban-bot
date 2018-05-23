import sys, i18n
sys.path.append('../../') 
import api.utils.qrHandler as qr
import api.utils.functions as f

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

def handleImage(page, senderId, url):
    img = qr.loadImgFromUrl(url)
    qrRes = qr.decodeQrFromImg(img)
    if qrRes:
        for obj in qrRes:
            if obj.type == 'QRCODE':
                page.send(senderId, 'QR DATA: ' + obj.data)
    else:
        page.send(senderId, f.readTextFromYML('qrResults.noQR'))


