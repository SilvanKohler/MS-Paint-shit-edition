import json
import subprocess
import threading
from ctypes import POINTER, WINFUNCTYPE, windll
from ctypes.wintypes import BOOL, HWND, RECT

import numpy as np
import pygame

pick = None
mouseButtonDownLeft = False
mouseMoved = False


def loadSettings():
    with open('settings.json') as settingsfile:
        return json.load(settingsfile)


settings = loadSettings()
_edition = settings['insider']['edition']
_iconResolution = 64 if settings['insider']['allow64pxIcon'] else 32
_width = settings['WindowSize']['width']
_height = settings['WindowSize']['height']
_project = "unbenannt"
_canvasResolution = settings['canvasSize']['width'], settings['canvasSize']['height']
canvas = np.full((_canvasResolution[0], _canvasResolution[1], 3), np.NaN)
QAB = None
icon = pygame.image.load(f'icons/icon {_iconResolution}px.png')
color = (0, 0, 0)


class getOutput(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global color
        while True:
            output = str(QAB.process.stdout.readline(),
                         'UTF-8').split()[0]  # [process]:[output]
            if output.split(':')[0] == 'colorpicker':
                color = output.split(':')[1].split(',')
                color = (int(color[0]), int(color[1]), int(color[2]))
            print(output)
class positionQAB(threading.Thread):
    def __init__(self, rect, qab):
        threading.Thread.__init__(self)
        self.rect = rect
        self.QAB = qab
    def run(self):
        self.QAB.process.communicate((self.rect.left, self.rect.top - settings['quickAccessBarWindowSize']['heigth']))

class QuickAccessBar(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.process = None
    def run(self):
        self.process = subprocess.Popen(
            ['py', 'QuickAccessBar.py'], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        catch = getOutput()
        catch.start()





def redrawCanvas(surface, canvas):
    for i in np.arange(canvas.shape[0]):
        for j in np.arange(canvas.shape[1]):
            if not canvas[i,j,0] is np.NaN:
                print(canvas[i, j])
                pygame.draw.rect(surface, canvas[i, j], (i * _width / _canvasResolution[0], j * _width / _canvasResolution[0], _width / _canvasResolution[0], _width / _canvasResolution[0]))

def draw(x, y, color):
    global canvas
    canvas[y,x] = np.array(color)


class main():  # threading.Thread):
    def __init__(self):
        global QAB
        # threading.Thread.__init__(self)
        pygame.init()
        self.prototype = WINFUNCTYPE(BOOL, HWND, POINTER(RECT))
        self.paramflags = (1, "hwnd"), (2, "lprect")
        self.mousePos = np.array([0, 0])
        self.width = _width
        self.height = _height
        self.canvasresolution = _canvasResolution
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((255, 255, 255))
        pygame.display.set_caption(f'{_project} - MS Paint {_edition} edition')
        pygame.display.set_icon(icon)
        QAB = QuickAccessBar()
        QAB.start()
        GetWindowRect = self.prototype(("GetWindowRect", windll.user32), self.paramflags)
        rect = GetWindowRect(pygame.display.get_wm_info()["window"])
        positioningQAB = positionQAB(rect, QAB)
        positioningQAB.start()
    def run(self):
        global mouseButtonDownLeft, QAB, color
        while True:
            GetWindowRect = self.prototype(("GetWindowRect", windll.user32), self.paramflags)
            rect = GetWindowRect(pygame.display.get_wm_info()["window"])
            positioningQAB.rect = rect
            mouseMoved = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QAB.process.kill()
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEMOTION:
                    self.mousePos = np.array(event.pos)
                    mouseMoved = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(event.button)
                    mouseButtonDownLeft = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouseButtonDownLeft = False

            # for x in np.arange(self.canvasresolution[0]):
            #     pygame.draw.line(self.screen, (0, 0, 0), (self.width / self.canvasresolution[0] * x, 0), (self.width / self.canvasresolution[0] * x, self.height), 1)

            # for y in np.arange(self.canvasresolution[1]):
            #     pygame.draw.line(self.screen, (0, 0, 0), (0, self.height / self.canvasresolution[1] * y), (self.width, self.height / self.canvasresolution[1] * y), 1)
            
            
            
            if mouseMoved and mouseButtonDownLeft:
                draw(int(self.mousePos[0] / (self.width / self.canvasresolution[0])) * self.width / self.canvasresolution[0], int(self.mousePos[1] / (self.height / self.canvasresolution[1])) * self.height / self.canvasresolution[1], color)
                # pygame.draw.rect(self.screen, color, (int(self.mousePos[0] / (self.width / self.canvasresolution[0])) * self.width / self.canvasresolution[0], int(
                #     self.mousePos[1] / (self.height / self.canvasresolution[1])) * self.height / self.canvasresolution[1], 10, 10))
            redrawCanvas(self.screen, canvas)
            pygame.display.flip()


if __name__ == "__main__":
    mainprocess = main()
    mainprocess.run()
