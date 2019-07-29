from tkinter import *
import json


def loadSettings():
    with open('settings.json') as settingsfile:
        return json.load(settingsfile)


settings = loadSettings()
_edition = settings['insider']['edition']
_width = settings['toolsWindowSize']['width']
_height = settings['toolsWindowSize']['height']
tools = ['Bleistift', 'Pinsel']
defaultSettingsBrush = settings['toolDefaultSettings']['brush']
selected = None
settingsBrush = defaultSettingsBrush


window = Tk()
window.title(f'Werkzeuge - MS Paint {_edition} edition')
window.geometry(f'{_width}x{_height}')
window.resizable(0, 0)
scrollbar = Scrollbar(window)
menu = Listbox(window, yscrollcommand=scrollbar.set)
menu.pack(side=LEFT, fill=BOTH)
scrollbar.pack(side=LEFT, fill=Y)


def updateTool(i):
    tool = tools[i]
    if tool == "Bleistift":
        print("tool_pencil")
    elif tool == "Pinsel":
        print(f"tool_brush_settings: {settingsBrush}")


def select(evt):
    global selected
    row = menu.curselection()
    if not row == ():
        updateTool(row[0])


menu.bind('<<ListboxSelect>>', select)
scrollbar.config(command=menu.yview)
row = 0
for tool in tools:
    menu.insert(row, tool)
    row += 1
mainloop()
