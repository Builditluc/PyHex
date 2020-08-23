
# PyHex

`PyHex` is a simple python hex editor for the terminal

[![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)
[![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/)

## Preview
![](https://i.imgur.com/Wia7wtg.png)
Displays the Offset and the content of the currently opened file. The Decoded text is displayed on the right <br><br>

![](https://i.imgur.com/c6fBf4t.png)
Supports scrolling with the arrow keys <br><br>

![](https://i.imgur.com/0OzgptH.png) <br>
Edit your files in hex supereasy 

## Controls
<table>
<tr><th>Key</th><th>Function</th></tr>
<tr><td>Arrow Keys</td><td>Move the cursor</td></tr>
<tr><td>0-9 & A-F</td><td>Edit the current byte (All of your changes to the file will be displayed in red)</td></tr>
<tr><td>Delete</td><td>Remove the edit at the position of the cursor and restore the original byte</td></tr>
<tr><td>Esc or q</td><td>Quit the program</td></tr>
</table>

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

Then, download the [newest version](https://github.com/Builditluc/PyHex/releases) of `PyHex` and unzip the program

Now you can view any file in `PyHex`:
```
./pyhex.py <file_name>
```

If you want to be able to use the file, also when not in the downloaded directory, you can add it to a directory that is in the path, such as `/usr/bin`.


### On Windows 10

You need to install python 3.8 from the [python website](https://www.python.org/) <br>
Make sure to add python to the PATH (Little checkbox in the python installer) <br>
After that install `windows-curses`:
```
pip install windows-curses
```

Download the [newest version](https://github.com/Builditluc/PyHex/releases) of `PyHex` and unzip the program

Now you can view any file in `PyHex`:
```
pyhex.py <file_name>
```

If you want to be able to use the file, also when not in the downloaded directory, move the directory to your documents folder (or any other folder).
Then you can add `PyHex` to the path with this simple command
```
set PATH=%PATH%;C:\path\to\the\pyhex\directory
```
Note: After you added this directory to the path, don't move it or otherwise it won't work

