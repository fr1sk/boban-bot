# settings.py
import logging

def init():
    global app
    global log
    global mongo

    mongo = None
    app = None
    log = logging.getLogger()

    console = logging.StreamHandler()
    log.addHandler(console)
