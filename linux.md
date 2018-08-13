### List HDDs with model information

```sh
$ lsblk -io KNAME,TYPE,SIZE,MODEL
```

### Use `socket.type` carefully

Linux's `socket.type` is a bitmask that can include extra info
about socket (like `SOCK_NONBLOCK` bit), therefore we can't do simple
`sock_type == socket.SOCK_STREAM` check, see
[`include/linux/net.h`](https://github.com/torvalds/linux/blob/v4.13/include/linux/net.h#L77)
for more details.

Example usage:

```py
if hasattr(socket, 'SOCK_NONBLOCK'):
    return (sock_type & 0xF) == socket.SOCK_STREAM
return sock_type == socket.SOCK_STREAM
```

Note that this is no longer an issue since Python 3.7:

[Fix socket.type on OSes with SOCK_NONBLOCK](https://bugs.python.org/issue32331)

[Source](https://github.com/python/cpython/commit/e796b2fe26f220107ac50667de6cc86c82b465e3)
