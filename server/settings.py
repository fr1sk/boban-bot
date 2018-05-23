# settings.py
import logging

def init():
    global app
    global log

    app = None
    log = logging.getLogger()

    console = logging.StreamHandler()
    log.addHandler(console)