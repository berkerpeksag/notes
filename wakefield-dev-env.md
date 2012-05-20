## 64 bit sistemde 32 bit Firefox çalıştırmak

```sh
sudo apt-get install ia32-libs
sudo apt-get install lib32asound2 lib32ncurses5 lib32stdc++6
```

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

## Firefox geliştirme ortamı

```sh
sudo apt-get build-dep firefox
sudo apt-get install mercurial libasound2-dev \
libcurl4-openssl-dev libnotify-dev libxt-dev \
libiw-dev mesa-common-dev autoconf2.13 yasm uuid
```

## PyPy geliştirme ortamı

```sh
sudo apt-get install \
libffi-dev pkg-config libz-dev libbz2-dev \
libncurses-dev libexpat1-dev libssl-dev \
libgc-dev python-sphinx python-greenlet
```
