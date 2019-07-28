from tkinter import *
import json
import threading
import subprocess


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

window = Tk()
window.title(f'Schnellzugriff - MS Paint {_edition} edition')
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