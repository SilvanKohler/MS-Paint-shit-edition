from Tkinter import *
import json

def loadSettings():
    with open('settings.json') as settingsfile:
        return json.load(settingsfile)
settings = loadSettings()
selected = []
window = Tk()
window.title(f'MS Paint {settings['edition']} edition')
window.geometry(f'{settings['WindowSize']['width']}x{settings['WindowSize']['height']}')
scrollbar1 = Scrollbar(window)
einstellungen = Listbox(window, yscrollcommand=scrollbar1.set)
einstellung = Entry(window)
def select(evt):
        global selected
        row = einstellungen.curselection()
        if not row == ():
                print(row[0])
                selected = [settings[row[0]], row[0]]
                description.delete(1.0, END)
                description.insert(END, descriptions[row[0]])

einstellungen.bind('<<ListboxSelect>>', select)
scrollbar1.config(command=einstellungen.yview)
def instert():
    row = 0
    for key, value in settings.iteritems():
        einstellungen.insert(row, key)
        row += 1