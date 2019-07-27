from tkinter import *
import json

def loadSettings():
    with open('settings.json') as settingsfile:
        return json.load(settingsfile)
settings = loadSettings()
_edition = settings['insider']['edition']
_width = settings['WindowSize']['width']
_height = settings['WindowSize']['height']
selection = None
selected = None
window = Tk()
window.title(f'MS Paint {_edition} edition')
window.geometry(f'{_width}x{_height}')
scrollbar1 = Scrollbar(window)
tree1 = Listbox(window, yscrollcommand=scrollbar1.set)
scrollbar2 = Scrollbar(window)
tree2 = Listbox(window, yscrollcommand=scrollbar2.set)
einstellung = Entry(window)
def finish():
    if selection:
        settings[selection] = einstellung.get()
ok = Button(window, text="OK", command=finish)
tree1.pack(side=LEFT, fill=BOTH)
scrollbar1.pack(side=LEFT, fill=Y)
tree2.pack(side=LEFT, fill=BOTH)
scrollbar2.pack(side=LEFT, fill=Y)
einstellung.pack(side=LEFT, fill=X)
ok.pack(side=LEFT)
def insert1():
    tree1.delete(0, END)
    row = 0
    for key, value in settings.items():
        tree1.insert(row, key)
        row += 1
def insert2(parent):
    tree2.delete(0, END)
    row = 0
    for key, value in settings[parent].items():
        tree2.insert(row, key)
        row += 1
def select1(evt):
    global selected
    row = tree1.curselection()
    if not row == ():
        einstellung.delete(0, END)
        selected = [list(settings.keys())[row[0]], row[0]]
        insert2(list(settings.keys())[row[0]])
def select2(evt):
    global selection
    row = tree2.curselection()
    if not row == () and selected:
        selection = list(settings.keys())[selected[1]]][list(settings[selected[0]].keys())[row[0]]]
        einstellung.delete(0, END)
        einstellung.insert(0, settings[list(settings.keys())[selected[1]]][list(settings[selected[0]].keys())[row[0]]])
tree1.bind('<<ListboxSelect>>', select1)
tree2.bind('<<ListboxSelect>>', select2)
scrollbar1.config(command=tree1.yview)
scrollbar2.config(command=tree2.yview)
insert1()
mainloop()