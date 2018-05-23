import i18n, urllib2, json, os
import settings as s

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
