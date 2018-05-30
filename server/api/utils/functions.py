import i18n, urllib2, json, os
import settings as s
import json
import requests
import time


def readTextFromYML(path, **kwargs):
    i18n.load_path.append('./resources/')
    print path
    return i18n.t("messages."+path, **kwargs)

def getUserInfo(senderId, token):
    url = "https://graph.facebook.com/"+senderId+"?fields=first_name,last_name,gender,profile_pic&access_token="+token
    print url
    try:
        res = urllib2.urlopen(url)
        data = json.loads(res.read())
        return data["gender"], data["first_name"], data["last_name"], data["profile_pic"]
    except:
        return "", "", "", ""

def convert_milli_time(x):
	return int(round(x * 100)) 

def sendImage(senderId, url):
	headers = {
    	'Content-Type': 'application/json',
	}
	data = {
		"recipient": {
			'id': str(senderId)
		},
		"message": {
			'attachment': {
				'type': 'image',
				"payload":{
					"url": str(url), 
				}
			}
		}
	}
	

	r = requests.post(url = "https://graph.facebook.com/v2.6/me/messages?access_token="+os.environ['PAGE_ACCESS_TOKEN'], headers=headers, data=data)
	print "RESPONSE FROM IMAGE ", str(r.status_code)



current_milli_time = lambda: int(round(time.time() * 1000))

