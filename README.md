pacman -S python3# PyHex

`PyHex` is a simple python hex viewer for the terminal

## Preview
Displays the Offset and the content of the currently opened file. (Decoded text will be added soon)
![](https://i.imgur.com/PdXMugu.png)

Supports scrolling with the arrow keys
![](https://i.imgur.com/B50L79O.png)

## Installation

### On GNU/LINUX
*... and other POSIX environments.*

You need to install python 3.8, if you haven't installed it yet:

Debian and debian deriatives:
```
apt install python3.8
```

Arch and arch deriatives:
```
pacman -S python3
```

Alpine linux:
```
apk add python3
```

Fedora:
```
dnf install python3
```

MacOS: You need to install python 3.8 from the [python website](https://www.python.org/). <br>
    
 pacman -S python3
Then clone this repository to any folder you want:
```
git clone https://github.com/Builditluc/PyHex.git
```

Now you can view any file in `PyHex`:
```
python3 pyhex.py <file_name>
```

If you want to be able to use the file, also when not in the cloned directory, you can add it to a directory that is in the path, such as `/usr/bin`.


### On Windows 10

You need to install python 3.8 from the [python website](https://www.python.org/). <br>
After that install `windows-curses`:
```
pip install windows-curses
```

Then clone this repository to any folder you want:
```
git clone https://github.com/Builditluc/PyHex.git
```

Now you can view any file in `PyHex`:
```
py pyhex.py <file_name>
```

Note:  if `py` don't work try to use `python` instead
    
    And for any problems regarding windows, you should have a look at [this](https://wiki.archlinux.org/index.php/Installation_guide)https://wiki.archlinux.org/index.php/Installation_guidehttps://wiki.archlinux.org/index.php/Installation_guide
