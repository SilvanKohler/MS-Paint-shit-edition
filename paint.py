import pygame
import numpy as np

def main():
    pygame.init()
    mousePos = np.array([0, 0])
    width = 600
    height = 400
    paintResolution = np.array([60, 40])
    screen = pygame.display.set_mode((width, height))
    print(pygame.QUIT)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEMOTION:
                mousePos = np.array(event.pos)
                print(mousePos)
        screen.fill((255, 255, 255))
        for x in np.arange(paintResolution[0]):
            pygame.draw.line(screen, (0, 0, 0), (width / paintResolution[0] * x, 0), (width / paintResolution[0] * x, height), 1)
        for y in np.arange(paintResolution[1]):
            pygame.draw.line(screen, (0, 0, 0), (0, height / paintResolution[1] * y), (width, height / paintResolution[1] * y), 1)
        pygame.draw.rect(screen, (255, 0, 50), (int(mousePos[0] / (width / paintResolution[0])) * width / paintResolution[0], int(mousePos[1] / (height / paintResolution[1])) * height / paintResolution[1], 10, 10))
        pygame.display.flip()
            


if __name__ == "__main__":
    main()