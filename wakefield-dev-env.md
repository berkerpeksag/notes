## SSH Key

```sh
mkdir -p ~/.ssh
cd ~/.ssh
ssh-keygen -t rsa -C "berker.peksag@gmail.com"
```

## Terminator

In `/usr/share/terminator/terminator`:

```python
if not filter((lambda s: '--geometry' in s), sys.argv):
   sys.argv.append('--geometry=1280x1000')
```

## Python

pip ile sistem bazında kurulacak paketler:

* fabric
* virtualenv
* flake8
* pep8
