# PyHex

`PyHex` is a simple python hex viewer for the terminal

## Preview
Displays the Offset and the content of the currently opened file. (Decoded text will be added soon)
![](https://i.imgur.com/PdXMugu.png)

Supports scrolling with the arrow keys
![](https://i.imgur.com/B50L79O.png)

## Installation

### On Ubuntu
*... and other Linux distributions.*

You need to install python 3.8, if you haven't installed it yet:
```
sudo apt install python3.8
```

Then clone this repository to any folder you want:
```
git clone https://github.com/Builditluc/PyHex.git
```

Now you can view any file in `PyHex`:
```
python3 pyhex.py <file_name>
```

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
