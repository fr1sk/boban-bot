import sys
import os
from flask import Flask, request
from dotenv import load_dotenv


#encoding conf
reload(sys)
sys.setdefaultencoding('UTF8')

app = Flask(__name__)
load_dotenv(dotenv_path='.env')

@app.route('/', methods=['GET'])
def verify(): # verify webhook
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.getenv('WEBHOOK_KEY'):
			return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return 'Hello from the backend side!' , 200

@app.route('/get-webhook-key', methods=['GET'])
def key():
	return os.getenv('WEBHOOK_KEY')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8081))
    print "*************************************"
    print "*          DEPLOYMENT DONE          *"
    print "*************************************"
    app.run(debug=False, host='0.0.0.0', port=port)