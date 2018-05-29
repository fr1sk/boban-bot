import sys
import os
import logging
from flask import Flask, request
from dotenv import load_dotenv
from fbmq import Page, Template
import api.conversation.conversation as m
import api.utils.functions as f
import settings as s
from flask_pymongo import PyMongo
# from api.conversation.conversation import handleQrCode

#encoding conf
reload(sys)
sys.setdefaultencoding('UTF8')

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
logger = logging.getLogger(__name__)
load_dotenv(dotenv_path='.env')
sys.stdout.flush()
page = Page(os.environ.get('PAGE_ACCESS_TOKEN'))
mongo = PyMongo(app)


@app.route('/', methods=['PAGE_ACCESS_TOKEN'])
def verify(): # verify webhook
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.getenv('WEBHOOK_KEY'):
			return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return 'Hello from the backend side!' , 200

page.show_starting_button("START_PAYLOAD")
page.show_persistent_menu([
    Template.ButtonPostBack('Napusti red', 'PAYLOAD_LEAVE_QUEUE'),
    Template.ButtonPostBack('Pomoc', 'PAYLOAD_HELP'),
    Template.ButtonWeb('Poseti MATF Hypatiu', 'https://hypatia.matf.bg.ac.rs:10333/StudInfo/scripts/studenti/prijavljivanjeFormular'),
    ])

@app.route('/', methods=['POST'])
def webhook():
    sys.stdout.flush()
    print "WEBHOOK CALLED - /"
    data = request.get_json()
    print "req data: ", data
    isImage, senderId, imgUrl = m.isImage(data)
    isLocation, senderId, lat, long = m.isLocation(data)
    if senderId:
        if isImage:
            m.handleImage(page, senderId, imgUrl)
        elif isLocation:
            m.handleLocation(page, senderId, lat, long)
        else:
            page.handle_webhook(request.get_data(as_text=False))
    return "ok"

@app.route('/boban', methods=['GET'])
def dashboard():
    Student = s.mongo.db.students
    student = Student.find({'inQueue': True})
    return JsonResponse(student, status=200)

@page.after_send
def after_send(payload, response):
    sys.stdout.flush()
    """:type payload: fbmq.Payload"""
    print "Message is sent..."

@page.handle_message
def message_handler(event):
	""":type event: fbmq.Event"""
	senderId = event.sender_id
	message = event.message_text
	print "\n\n"
	print repr(event)
	if message:
		gender, fName, lName, pic = f.getUserInfo(senderId, os.environ['PAGE_ACCESS_TOKEN'])
		page.send(senderId, f.readTextFromYML('default.text', ime = fName))

@page.callback(['START_PAYLOAD'])
def start_callback(payload, event):
	print("====== GET STARTED PAYLOAD ======")
	senderId = event.sender_id
	m.getStartedHandler(page, senderId)

@page.callback(['PAYLOAD_HELP'])
def help_callback(payload, event):
	print("====== PAYLOAD_HELP ======")
	senderId = event.sender_id
	m.sendHelp(page, senderId)

@page.callback(['PAYLOAD_QUEUE'])
def queue_callback(payload, event):
	print("====== PAYLOAD_QUEUE ======")
	senderId = event.sender_id
	m.sendQueueInfo(page, senderId)

@page.callback(['PAYLOAD_LEAVE_QUEUE'])
def leave_queue_callback(payload, event):
	print("====== PAYLOAD_LEAVE_QUEUE ======")
	senderId = event.sender_id
	m.removeUserFromQueue(page, senderId)

@page.callback(['FIRST_MESSAGE_PAYLOAD'])
def firstMessage(payload, event):
	print("====== FIRST_MESSAGE_PAYLOAD ======")
	senderId = event.sender_id
	m.firstMessage(page, senderId)

@app.route('/get-webhook-key', methods=['GET'])
def key():
	print 'ok'
	return os.getenv('PAGE_ACCESS_TOKEN')	

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8081))
    print "*************************************"
    print "*          DEPLOYMENT DONE          *"
    print "*************************************"
    s.app = app
    s.mongo = mongo
    sys.stdout.flush()
    app.run(debug=True, host='0.0.0.0', port=port)