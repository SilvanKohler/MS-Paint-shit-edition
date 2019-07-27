import pygame

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
    return (h,s,v)

def hsv2rgb(h,s,v):
h = hSlider.value
    s = sSlider.value / 100
    v = vSlider.value / 100
    h60 = h / 60
    h60f = int(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
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
    r, g, b, = rSlider.value, gSlider.value, bSlider.value = r * 255, g * 255, b * 255




def main():
    pygame.init()
    screen = pygame.display.set_mode(120,100)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
