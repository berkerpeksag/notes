import os
import signal
import time


def sighup_handler(signal, frame):
    print('This is the signal:', signal)

signal.signal(signal.SIGHUP, sighup_handler)

print('PID:', os.getpid())

time.sleep(60)
