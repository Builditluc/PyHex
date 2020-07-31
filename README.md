
# PyHex

`PyHex` is a simple python hex viewer for the terminal

[![GitHub version](https://badge.fury.io/gh/builditluc%2Fpyhex.svg)](https://badge.fury.io/gh/builditluc%2Fpyhex)
[![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)
[![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/)

## Preview
Displays the Offset and the content of the currently opened file. The Decoded text is displayed on the right
![](https://i.imgur.com/IQ8ossY.png)

Supports scrolling with the arrow keys
![](https://i.imgur.com/HvKgfWC.png)

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

<br>

MacOS: You need to install python 3.8 from the [python website](https://www.python.org/). 

<br>

Then, download the newest version of `PyHex` and unzip the source code

Now you can view any file in `PyHex`:
```
./pyhex.py <file_name>
```

If you want to be able to use the file, also when not in the downloaded directory, you can add it to a directory that is in the path, such as `/usr/bin`.


### On Windows 10

You need to install python 3.8 from the [python website](https://www.python.org/) <br>
After that install `windows-curses`:
```
pip install windows-curses
```

Download the newest version of `PyHex` and unzip the source code

Now you can view any file in `PyHex`:
```
py pyhex.py <file_name>
```
Note:  if `py` don't work try to use `python` instead

If you want to be able to use the file, also when not in the downloaded directory, move the directory to your documents folder (or any other folder).
Then you can `PyHex` to the path with this simple command
```
set PATH=%PATH%;C:\path\to\the\pyhex\directory
```

