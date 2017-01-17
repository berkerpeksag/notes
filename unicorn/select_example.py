import os
import select
import socket

sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock1.bind(('0.0.0.0', 8888))
sock1.listen(10)
sock2.bind(('0.0.0.0', 9999))
sock2.listen(10)

for _ in range(5):
    child_pid = os.fork()
    if child_pid == 0:
        # We could wrap this block with
        # ``try: ... except KeyboardInterrupt: sys.exit()``
        # to avoid printing tracebacks to the console.
        while True:
            readable, _, _ = select.select([sock1, sock2], [], [])
            connection, _ = readable[0].accept()
            with connection.makefile() as fobj:
                print('[%d] %s' % (os.getpid(), fobj.read().strip()))
            connection.close()

os.waitpid(-1, 0)
