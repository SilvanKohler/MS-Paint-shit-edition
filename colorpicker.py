import pygame
import numpy as np

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
    width = 300
    height = 250
    sliderWidth = width - height
    screen = pygame.display.set_mode((width,height))
    colorfield = np.zeros((width, width, 3), dtype=np.int)
    h = 0
    a = np.arange(height)
    for x in a:
        for y in a:
            rgb = hsv2rgb(h,x/height*100,(height-y)/height*100)
            for i in [0,1,2]:
                colorfield[x,y,i] = rgb[i]
    hueLine = np.zeros((height, sliderWidth, 3), dtype=np.int)
    s = np.arange(sliderWidth)
    for y in a:
        rgb = hsv2rgb(y,50,50)
        for x in s:
            for i in [0,1,2]:
                hueLine[y,x,i] = rgb[i]
    colorfield = np.append(colorfield, hueLine, axis=1)
    colorfield.resize((width, height, 3))


    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        pygame.surfarray.blit_array(screen, colorfield)
        pygame.display.flip()

if __name__ == "__main__":
    main()