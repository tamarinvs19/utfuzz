import logging
import pathlib
import signal
import sys

from utfuzz.user_interface.printer import my_print


def signal_handler(signal, frame):
    my_print('\nutfuzz has been cancelled!')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

FORMAT = '%(asctime)s | %(filename)s | line:%(lineno)d | %(message)s'
logging.basicConfig(format=FORMAT, filemode='a', filename=pathlib.Path('.utfuzz.log'), level=logging.INFO)
