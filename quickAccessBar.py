from tkinter import *
import json
import threading
import subprocess
import os

class colorPicker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.process = None

    def run(self):
        self.process = subprocess.Popen(['py', 'colorpicker.py'])
picker = False
pick = None
def Picker():
    global picker, pick
    if not picker:
        picker = True
        pick = colorPicker()
        pick.start()
    else:
        picker = False
        pick.process.kill()


def loadSettings():
    with open('settings.json') as settingsfile:
        return json.load(settingsfile)


settings = loadSettings()
_edition = settings['insider']['edition']
_width = settings['WindowSize']['width'] if settings['quickAccessBarWindowSize'][
    'width'] == "windowSize" else settings['quickAccessBarWindowSize']['width']
_height = settings['quickAccessBarWindowSize']['height']
_iconResolution = 64 if settings['insider']['allow64pxIcon'] else 32
icon = PhotoImage(file=os.path.join(sp, f'icon {_iconResolution}px.png')
window = Tk()
window.title(f'Schnellzugriff - MS Paint {_edition} edition')
window.iconbitmap(icon)
window.geometry(f'{_width}x{_height}')
window.resizable(0,0)

class CustomButton:
    def __init__(self, master, icon, command):
        self.Button = Button(master, command=command)
        self.Button.config(image=icon, width="10", height="10")
        self.Button.pack(side=LEFT)

colorpickerIcon = PhotoImage(file="icons/colorpicker.png")
colorpickerButton = CustomButton(window, colorpickerIcon, command=Picker)
mainloop()