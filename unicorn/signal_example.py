import os
import signal
import time

print('PID:', os.getpid())

signal.signal(signal.SIGUSR1, lambda signum, frame: print(signum, 'received'))

signal.signal(signal.SIGQUIT, lambda signum, frame: print(signum, 'received'))

time.sleep(60)
