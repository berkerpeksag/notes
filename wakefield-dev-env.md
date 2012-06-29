## .dotfiles

```sh
git init
git remote add origin git@github.com:berkerpeksag/dotfiles.git
git pull --rebase origin master
```

## Git ve GitHub

`.gitconfig` dosyası `.dotfiles` bölümünden geliyor.

```sh
mkdir -p ~/.ssh
cd ~/.ssh
ssh-keygen -t rsa -C "berker.peksag@gmail.com"
```

## Python geliştirme ortamı

```sh
apt-get update && apt-get upgrade && apt-get install git-core sqlite3 \
python-sqlite python-setuptools python-pip python-dev build-essential \
nginx emacs23 curl libcurl3 mercurial
```

```sh
sudo pip install virtualenv
```

## PyPy geliştirme ortamı

```sh
sudo apt-get install \
libffi-dev pkg-config libz-dev libbz2-dev \
libncurses-dev libexpat1-dev libssl-dev \
libgc-dev python-sphinx python-greenlet
```

## Terminator

In `/usr/share/terminator/terminator`:

```python
if not filter((lambda s: '--geometry' in s), sys.argv):
   sys.argv.append('--geometry=1280x1000')
```
