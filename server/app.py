import sys
import os
import logging
from flask import Flask, request
from dotenv import load_dotenv
from fbmq import Page, Template
import api.conversation.conversation as m
import api.utils.functions as f
import settings as s
# from api.conversation.conversation import handleQrCode

#encoding conf
reload(sys)
sys.setdefaultencoding('UTF8')

app = Flask(__name__)
app.config['DEBUG'] = True
logger = logging.getLogger(__name__)
load_dotenv(dotenv_path='.env')
sys.stdout.flush()
page = Page(os.environ.get('PAGE_ACCESS_TOKEN'))


@app.route('/', methods=['PAGE_ACCESS_TOKEN'])
def verify(): # verify webhook
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.getenv('WEBHOOK_KEY'):
			return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return 'Hello from the backend side!' , 200

page.show_starting_button("START_PAYLOAD")

@app.route('/', methods=['POST'])
def webhook():
    sys.stdout.flush()
    print "WEBHOOK CALLED - /"
    page.handle_webhook(request.get_data(as_text=False))
    data = request.get_json()
    print "req data: ", data
    isImage, senderId, imgUrl = m.isImage(data)
    if isImage:
        m.handleImage(page, senderId, imgUrl)
    return "ok"

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
    sys.stdout.flush()
    app.run(debug=True, host='0.0.0.0', port=port)