# settings.py
import logging

def init():
    global app
    global log
    global mongo
    global line

    line = []
    mongo = None
    app = None
    log = logging.getLogger()

    console = logging.StreamHandler()
    log.addHandler(console)
