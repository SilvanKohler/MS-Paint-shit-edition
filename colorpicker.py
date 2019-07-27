import pygame
import numpy as np
import json
import Slider

def loadSettings():
    with open('settings.json') as settingsfile:
        return json.load(settingsfile)
        
def rgb2hsv(r,g,b):
    cmax = max(r, g, b) / 255
    cmin = min(r, g, b) / 255
    delta = cmax - cmin
    if delta == 0.0:
        h = 0.0
    elif cmax == r / 255:
        h = 60 * ((g - b) / 255 / delta % 6)
    elif cmax == g / 255:
        h = 60 * ((b - r) / 255 / delta + 2)
    elif cmax == b / 255:
        h = 60 * ((r - g) / 255 / delta + 4)
    if cmax == 0.0:
        s = 0.0
    elif cmax != 0.0:
        s = delta / cmax * 100
    v = cmax * 100
    return (h, s, v)

def hsv2rgb(h,s,v):
    h = h / 1
    s = s / 100
    v = v / 100
    h60 = h / 60
    h60f = int(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    if hi == 0:
        r, g, b = v, t, p
    elif hi == 1:
        r, g, b = q, v, p
    elif hi == 2:
        r, g, b = p, v, t
    elif hi == 3:
        r, g, b = p, q, v
    elif hi == 4:
        r, g, b = t, p, v
    elif hi == 5:
        r, g, b = v, p, q
    r, g, b = r * 255, g * 255, b * 255
    return (int(round(r)), int(round(g)), int(round(b)))


def main():
    pygame.init()
    settings = loadSettings()
    width = settings['WindowSize']['width']
    height = settings['WindowSize']['height']
    sliderWidth = width - height
    screen = pygame.display.set_mode((width,height))
    colorfield = np.zeros((width, height, 3), dtype=np.int)
    mousePos = np.array([0,0], dtype=np.int)
    mouseDown = False

    h = 0
    a = np.arange(height)
    for y in a:
        for x in a:
            rgb = hsv2rgb(h,y/height*100,(height-x)/height*100)
            for i in [0,1,2]:
                colorfield[y,x,i] = rgb[i]
                
    s = np.arange(sliderWidth)
    for y in a:
        rgb = hsv2rgb(y, 100, 100)
        for x in s + height:
            for i in [0,1,2]:
                colorfield[x,y,i] = rgb[i]
    
    colorfield.resize((width, height, 3))

    s = Slider.Slider(0, 360, screen)

    
    while True:
        mouseClick = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEMOTION:
                mousePos = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 0:
                    mouseDown = True
                    mouseClick = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 0:
                    mouseDown = False
        Slider.Slider.update(mousePos, mouseDown, mouseClick)
        Slider.Slider.showAll()
        
        pygame.surfarray.blit_array(screen, colorfield)
        pygame.display.flip()

if __name__ == "__main__":
    main()