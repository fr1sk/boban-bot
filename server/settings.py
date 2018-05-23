# settings.py
import logging

def init():
    global log 
    # Get the top-level logger object
    log = logging.getLogger()

    # make it print to the console.
    console = logging.StreamHandler()
    log.addHandler(console)