from tkinter import *
import json
def loadSettings():
    with open('settings.json') as settingsfile:
        return json.load(settingsfile)
settings = loadSettings()
_edition = settings['insider']['edition']
_width = settings['WindowSize']['width'] if settings['quickAccessBarWindowSize']['width'] == "windowSize" else settings['quickAccessBarWindowSize']['width']
_height = settings['quickAccessBarWindowSize']['height']
window = Tk()
window.title(f'quick access - MS Paint {_edition} edition')
window.geometry(f'{_width}x{_height}')
