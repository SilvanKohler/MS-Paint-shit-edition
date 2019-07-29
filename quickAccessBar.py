from tkinter import *
import json
import threading
import subprocess
import os

pick = None
tool = None

class getColor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            print('colorpicker:' + pick.process.stdout.readline())


class colorPicker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.process = None

    def run(self):
        self.process = subprocess.Popen(['py', 'colorpicker.py'], shell=True, stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
        color = getColor()
        color.start
class toolBox(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.process = None

    def run(self):
        self.process = subprocess.Popen(['py', 'tools.py'], shell=True, stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)


picker_opened = False
tools_opened = False

def Picker():
    global picker_opened, pick
    if not picker_opened:
        picker_opened = True
        pick = colorPicker()
        pick.start()
    else:
        picker_opened = False
        pick.process.kill()
def Tools():
    global tools_opened, tool
    if not tools_opened:
        tools_opened = True
        tool = toolBox()
        tool.start()
    else:
        tools_opened = False
        tool.process.kill()

def loadSettings():
    with open('settings.json') as settingsfile:
        return json.load(settingsfile)


settings = loadSettings()
_edition = settings['insider']['edition']
_width = settings['WindowSize']['width'] if settings['quickAccessBarWindowSize'][
    'width'] == "windowSize" else settings['quickAccessBarWindowSize']['width']
_height = settings['quickAccessBarWindowSize']['height']
_iconResolution = 64 if settings['insider']['allow64pxIcon'] else 32
window = Tk()
window.title(f'Schnellzugriff - MS Paint {_edition} edition')
window.wm_iconbitmap(os.path.join(f'icons/icon {_iconResolution}px.ico'))
window.geometry(f'{_width}x{_height}')
window.resizable(0, 0)


class CustomButton:
    def __init__(self, master, icon, command):
        self.Button = Button(master, command=command)
        self.Button.config(image=icon, width="10", height="10")
        self.Button.pack(side=LEFT)


colorpickerIcon = PhotoImage(file="icons/colorpicker.png")
colorpickerButton = CustomButton(window, colorpickerIcon, command=Picker)
toolsIcon = PhotoImage(file="icons/tools.png")
toolsButton = CustomButton(window, toolsIcon, command=Tools)
mainloop()
