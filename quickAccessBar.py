from tkinter import *
import json
import threading
import subprocess


class colorpicker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.process = None

    def run(self):
        self.process = subprocess.Popen(['py', 'colorpicker.py'])


def openpicker():
    pick = colorpicker()
    pick.start()


def loadSettings():
    with open('settings.json') as settingsfile:
        return json.load(settingsfile)


settings = loadSettings()
_edition = settings['insider']['edition']
_width = settings['WindowSize']['width'] if settings['quickAccessBarWindowSize'][
    'width'] == "windowSize" else settings['quickAccessBarWindowSize']['width']
_height = settings['quickAccessBarWindowSize']['height']
colorpickerIcon = PhotoImage(file="icons/colorpicker.png")
window = Tk()
window.title(f'quick access - MS Paint {_edition} edition')
window.geometry(f'{_width}x{_height}')


class CustomButton:
    def __init__(self, master, icon, command):
        self.Button = Button(master)
        self.Button.config(image=icon, width="10", height="10")
        self.Button.pack(side=LEFT)


colorpickerButton = CustomButton(window, colorpickerIcon, )
