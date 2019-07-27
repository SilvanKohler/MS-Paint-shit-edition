import pygame
import numpy as np
import subprocess
import threading
from time import sleep
import json

picker = True

def loadSettings():
    with open('settings.json') as settingsfile:
        return json.load(settingsfile)


class colorpicker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.process = None
    def run(self):
        self.process = subprocess.Popen(['py', 'colorpicker.py'])
def openpicker():
    pick = colorpicker()
    pick.start()

            
class main(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        pygame.init()
        settings = loadSettings()
        self.mousePos = np.array([0, 0])
        self.width = settings['WindowSize']['width']
        self.height = settings['WindowSize']['height']
        self.paintResolution = np.array([60, 40])
        self.screen = pygame.display.set_mode((self.width, self.height))
    def run(self):
        while True:
            if not picker and pick:
                pick.process.kill()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEMOTION:
                    self.mousePos = np.array(event.pos)
                    print(self.mousePos)
            self.screen.fill((255, 255, 255))
            for x in np.arange(self.paintResolution[0]):
                pygame.draw.line(self.screen, (0, 0, 0), (self.width / self.paintResolution[0] * x, 0), (self.width / self.paintResolution[0] * x, self.height), 1)
            
            for y in np.arange(self.paintResolution[1]):
                pygame.draw.line(self.screen, (0, 0, 0), (0, self.height / self.paintResolution[1] * y), (self.width, self.height / self.paintResolution[1] * y), 1)

            pygame.draw.rect(self.screen, (255, 0, 50), (int(self.mousePos[0] / (self.width / self.paintResolution[0])) * self.width / self.paintResolution[0], int(self.mousePos[1] / (self.height / self.paintResolution[1])) * self.height / self.paintResolution[1], 10, 10))
            
            pygame.display.flip()

if __name__ == "__main__":
    mainprocess = main()
    mainprocess.start()