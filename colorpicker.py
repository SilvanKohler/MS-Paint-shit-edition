import pygame
import numpy as np
import json
import Slider

def loadSettings():
    with open('settings.json') as settingsfile:
        return json.load(settingsfile)


settings = loadSettings()
width = settings['WindowSize']['width']
height = settings['WindowSize']['height']
threadsAllowed = settings['insider']['allowThreads']
colorfield = np.zeros((width, height, 3), dtype=np.int)

def rgb2hsv(r, g, b):
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


def hsv2rgb(h, s, v):
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


def noThreads():
    global colorfield
    pygame.init()
    sliderWidth = width - height
    screen = pygame.display.set_mode((width, height))
    mousePos = np.array([0, 0], dtype=np.int)
    mouseDown = False
    h = 0
    a = np.arange(height)
    for y in a:
        for x in a:
            rgb = hsv2rgb(h, y/height*100, (height-x)/height*100)
            for i in [0, 1, 2]:
                colorfield[y, x, i] = rgb[i]

    s = np.arange(sliderWidth)
    for y in a:
        rgb = hsv2rgb(y, 100, 100)
        for x in s + height:
            for i in [0, 1, 2]:
                colorfield[x, y, i] = rgb[i]

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


#
#   $$\     $$\                                           $$\ $$\                     
#   $$ |    $$ |                                          $$ |\__|                    
# $$$$$$\   $$$$$$$\   $$$$$$\   $$$$$$\   $$$$$$\   $$$$$$$ |$$\ $$$$$$$\   $$$$$$\  
# \_$$  _|  $$  __$$\ $$  __$$\ $$  __$$\  \____$$\ $$  __$$ |$$ |$$  __$$\ $$  __$$\ 
#   $$ |    $$ |  $$ |$$ |  \__|$$$$$$$$ | $$$$$$$ |$$ /  $$ |$$ |$$ |  $$ |$$ /  $$ |
#   $$ |$$\ $$ |  $$ |$$ |      $$   ____|$$  __$$ |$$ |  $$ |$$ |$$ |  $$ |$$ |  $$ |
#   \$$$$  |$$ |  $$ |$$ |      \$$$$$$$\ \$$$$$$$ |\$$$$$$$ |$$ |$$ |  $$ |\$$$$$$$ |
#    \____/ \__|  \__|\__|       \_______| \_______| \_______|\__|\__|  \__| \____$$ |
#                                                                           $$\   $$ |
#                                                                           \$$$$$$  |
#                                                                            \______/ 
#





def thread1(a, h):
    global colorfield
    for y in a:
        for x in a:
            rgb = hsv2rgb(h, y/height*100, (height-x)/height*100)
            for i in [0, 1, 2]:
                colorfield[y, x, i] = rgb[i]


def thread2(a, s):
    global colorfield
    for y in a:
        rgb = hsv2rgb(y, 100, 100)
        for x in s + height:
            for i in [0, 1, 2]:
                colorfield[x, y, i] = rgb[i]


def Threads():
    from threading import Thread
    global colorfield
    pygame.init()

    sliderWidth = width - height
    screen = pygame.display.set_mode((width, height))

    mousePos = np.array([0, 0], dtype=np.int)
    mouseDown = False
    h = 0
    a = np.arange(height)
    s = np.arange(sliderWidth)
    Thread1 = Thread(target=thread1, args=(a, h))
    Thread2 = Thread(target=thread2, args=(a, s))
    Thread1.start()
    Thread2.start()
    Thread2.join()
    Thread1.join()
    colorfield.resize((width, height, 3))
    pygame.surfarray.blit_array(screen, colorfield)

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


if threadsAllowed:
    Threads()
else:
    noThreads()


# from threading import Thread
# import pygame
# import numpy as np
# import json
# import Slider
# from timeit import default_timer as timer

# def loadSettings():
#     with open('settings.json') as settingsfile:
#         return json.load(settingsfile)


# settings = loadSettings()
# width = settings['WindowSize']['width']
# height = settings['WindowSize']['height']


# def rgb2hsv(r, g, b):
#     cmax = max(r, g, b) / 255
#     cmin = min(r, g, b) / 255
#     delta = cmax - cmin
#     if delta == 0.0:
#         h = 0.0
#     elif cmax == r / 255:
#         h = 60 * ((g - b) / 255 / delta % 6)
#     elif cmax == g / 255:
#         h = 60 * ((b - r) / 255 / delta + 2)
#     elif cmax == b / 255:
#         h = 60 * ((r - g) / 255 / delta + 4)
#     if cmax == 0.0:
#         s = 0.0
#     elif cmax != 0.0:
#         s = delta / cmax * 100
#     v = cmax * 100
#     return (h, s, v)


# def hsv2rgb(h, s, v):
#     h = h / 1
#     s = s / 100
#     v = v / 100
#     h60 = h / 60
#     h60f = int(h60)
#     hi = int(h60f) % 6
#     f = h60 - h60f
#     p = v * (1 - s)
#     q = v * (1 - f * s)
#     t = v * (1 - (1 - f) * s)
#     if hi == 0:
#         r, g, b = v, t, p
#     elif hi == 1:
#         r, g, b = q, v, p
#     elif hi == 2:
#         r, g, b = p, v, t
#     elif hi == 3:
#         r, g, b = p, q, v
#     elif hi == 4:
#         r, g, b = t, p, v
#     elif hi == 5:
#         r, g, b = v, p, q
#     r, g, b = r * 255, g * 255, b * 255
#     return (int(round(r)), int(round(g)), int(round(b)))


# colorfield = np.zeros((width, height, 3), dtype=np.int)


# def thread1(a, h, y):
#     global colorfield
#     for x in a:
#         rgb = hsv2rgb(h, y/height*100, (height-x)/height*100)
#         for i in [0, 1, 2]:
#             colorfield[y, x, i] = rgb[i]


# def thread2(y, s):
#     global colorfield
#     rgb = hsv2rgb(y, 100, 100)
#     for x in s + height:
#         for i in [0, 1, 2]:
#             colorfield[x, y, i] = rgb[i]


# def main():
#     global colorfield
#     pygame.init()

#     sliderWidth = width - height
#     screen = pygame.display.set_mode((width, height))

#     mousePos = np.array([0, 0], dtype=np.int)
#     mouseDown = False
#     start = timer()
#     h = 0
#     a = np.arange(height)
#     threadsgroup = [[]]
#     for y in a:
#         if y == height/10:
#             threadsgroup.append([])
#         if y == height/10*2:
#             threadsgroup.append([])
#         elif y == height/10*3:
#             threadsgroup.append([])
#         elif y == height/10*4:
#             threadsgroup.append([])
#         elif y == height/2:
#             threadsgroup.append([])
#         elif y == height/10*6:
#             threadsgroup.append([])
#         elif y == height/10*7:
#             threadsgroup.append([])
#         elif y == height/10*8:
#             threadsgroup.append([])
#         elif y == height/10*9:
#             threadsgroup.append([])
#         elif y == height:
#             threadsgroup.append([])
#         threadsgroup[len(threadsgroup) -
#                      1].append(Thread(target=thread1, args=(a, h, y)))
#     s = np.arange(sliderWidth)
#     for y in a:
#         if y == height/10:
#             threadsgroup.append([])
#         elif y == height/10*2:
#             threadsgroup.append([])
#         elif y == height/10*3:
#             threadsgroup.append([])
#         elif y == height/10*4:
#             threadsgroup.append([])
#         elif y == height/2:
#             threadsgroup.append([])
#         elif y == height/10*6:
#             threadsgroup.append([])
#         elif y == height/10*7:
#             threadsgroup.append([])
#         elif y == height/10*8:
#             threadsgroup.append([])
#         elif y == height/10*9:
#             threadsgroup.append([])
#         threadsgroup[len(threadsgroup) -
#                      1].append(Thread(target=thread2, args=(y, s)))
#     count = 0
#     for threads in threadsgroup:
#         for thread in threads:
#             count += 1
#             thread.start()
#     colorfield.resize((width, height, 3))
#     pygame.surfarray.blit_array(screen, colorfield)
#     duration = timer() - start
#     print(duration)
#     for threads in threadsgroup:
#         for thread in threads:
#             count += 1
#             thread._stop()

#     s = Slider.Slider(0, 360, screen)

#     while True:
#         mouseClick = False
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 return
#             elif event.type == pygame.MOUSEMOTION:
#                 mousePos = event.pos
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 if event.button == 0:
#                     mouseDown = True
#                     mouseClick = True
#             elif event.type == pygame.MOUSEBUTTONUP:
#                 if event.button == 0:
#                     mouseDown = False
#         Slider.Slider.update(mousePos, mouseDown, mouseClick)
#         Slider.Slider.showAll()

#         pygame.surfarray.blit_array(screen, colorfield)
#         pygame.display.flip()


# if __name__ == "__main__":
#     main()
