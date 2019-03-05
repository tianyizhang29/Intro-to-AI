import pygame
import numpy as np
import random

def drawGrid(reveal_matrix):
    WHITE = (243, 236, 219)
    GREEN = (171, 215, 51)
    GREY = (192, 192, 192)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    surface = pygame.display.set_mode((100, 200))

    gridWidth = len(reveal_matrix)
    gridHeight = len(reveal_matrix[0])
    size = 30
    gap = 2

    sufWidth = size * gridWidth + (gridWidth + 1) * gap
    sufHeight = size * gridHeight + (gridHeight + 1) * gap

    surface = pygame.display.set_mode((sufWidth, sufHeight))

    gridlist = reveal_matrix.flatten()

    if not pygame.font.get_init():
        pygame.font.init()

    exitFlag = True
    while exitFlag:
        surface.fill(BLACK)
        for i in range(gridHeight):
            for j in range(gridWidth):
                if gridlist[i * gridWidth + j] == '*':
                    flag = pygame.image.load('flag_red.png')
                    pygame.draw.rect(surface, GREEN, [(gap + size) * j + gap, (gap + size) * i + gap, size, size])
                    surface.blit(flag,((gap + size) * j + gap,(gap + size) * i + gap))
                elif gridlist[i * gridWidth + j] == "W":
                    flag = pygame.image.load('bomb.png')
                    pygame.draw.rect(surface, RED, [(gap + size) * j + gap, (gap + size) * i + gap, size, size])
                    surface.blit(flag,((gap + size) * j + 4,(gap + size) * i + 5))
                elif gridlist[i * gridWidth + j] == "0":
                    pygame.draw.rect(surface, WHITE, [(gap + size) * j + gap, (gap + size) * i + gap, size, size])
                else:
                    pygame.draw.rect(surface, WHITE, [(gap + size) * j + gap, (gap + size) * i + gap, size, size])
                    number = pygame.font.SysFont('helvetica', 18)
                    numberSurface = number.render(str(gridlist[i * gridWidth + j]), True, BLACK)
                    numberRect = numberSurface.get_rect()
                    numberRect.center = ((gap + size) * j + gap + size / 2, (gap + size) * i + gap + size / 2)
                    surface.blit(numberSurface, numberRect)
        pygame.display.flip()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exitflag = False

    pygame.display.set_caption("MineSweeper")

