import pygame
import numpy as np
import subprocess
import threading
import json

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
icon = pygame.image.load(f'icons/icon {_iconResolution}px.png')


class getOutput(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            output = str(pick.process.stdout.readline(), 'UTF-8').split()[0] #[process]:[output] 
            if output.split(':')[0] == 'colorpicker':
                color = output.split(':')[1].split(',')
                color = (int(color[0]), int(color[1]), int(color[2]))


class QuickAccessBar(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.process = None

    def run(self):
        self.process = subprocess.Popen(
            ['py', 'QuickAccessBar.py'], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


QAB = None


def redrawPainting(surface, painting=np.array([])):#https://camo.githubusercontent.com/94db1e5e2a4eaa28f99e042e946adbd0fee2739c/68747470733a2f2f696d672e736869656c64732e696f2f636f646163792f67726164652f30333361646533333936343934653439396662666363333030623730343462612f6d61737465723f7374796c653d666c61742d737175617265
    for i in np.arange(painting.shape[0]):
        for j in np.arange(painting.shape[1]):
            pygame.draw.rect(surface, (0,0,0), ())


def openQuickAccessBar():
    global QAB
    QAB = QuickAccessBar()
    QAB.start()


class main():  # threading.Thread):
    def __init__(self):
        # threading.Thread.__init__(self)
        pygame.init()
        self.mousePos = np.array([0, 0])
        self.width = _width
        self.height = _height
        self.paintResolution = np.array([60, 40])
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((255, 255, 255))
        pygame.display.set_caption(f'{_project} - MS Paint {_edition} edition')
        pygame.display.set_icon(icon)
        openQuickAccessBar()

    def run(self):
        global mouseButtonDownLeft, QAB
        while True:
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

            # for x in np.arange(self.paintResolution[0]):
            #     pygame.draw.line(self.screen, (0, 0, 0), (self.width / self.paintResolution[0] * x, 0), (self.width / self.paintResolution[0] * x, self.height), 1)

            # for y in np.arange(self.paintResolution[1]):
            #     pygame.draw.line(self.screen, (0, 0, 0), (0, self.height / self.paintResolution[1] * y), (self.width, self.height / self.paintResolution[1] * y), 1)
            if mouseMoved and mouseButtonDownLeft:
                pygame.draw.rect(self.screen, (255, 0, 50), (int(self.mousePos[0] / (self.width / self.paintResolution[0])) * self.width / self.paintResolution[0], int(
                    self.mousePos[1] / (self.height / self.paintResolution[1])) * self.height / self.paintResolution[1], 10, 10))
            pygame.display.flip()


if __name__ == "__main__":
    mainprocess = main()
    mainprocess.run()
