import os

read_fd, write_fd = os.pipe()

print('read_fd:', read_fd, os.get_inheritable(read_fd))
print('write_fd:', write_fd, os.get_inheritable(write_fd))

child_pid = os.fork()

if child_pid == 0:
    os.close(read_fd)

    with open(write_fd, "w") as write_end:
        write_end.write("hello from your child!")
else:
    os.close(write_fd)
    os.waitpid(child_pid, 0)

    with open(read_fd) as read_end:
        message = read_end.read()
    print("received from child:", message)
