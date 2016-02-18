import random
import math

import pygame
from pygame.locals import *

_WHITE = (255, 255, 255)
_DEFAULT_COLOR = _WHITE
_DEFAULT_NB_BRANCHES=24

_WIDTH = 800
_HEIGHT = 600

pygame.init()

window = pygame.display.set_mode((_WIDTH, _HEIGHT))

def flip():
    pygame.display.flip()

def pt():
    return (random.randint(0, _WIDTH-1), random.randint(0, _HEIGHT-1))

def snowflake(center, radius, nb_branches=_DEFAULT_NB_BRANCHES, color=_DEFAULT_COLOR):
    for i in range(nb_branches):
        tip = ( center[0] + radius * math.cos(2 * math.pi * i / nb_branches),
                center[1] + radius * math.sin(2 * math.pi * i / nb_branches))
        pygame.draw.line(window, color, center, tip)
    flip()

def cone(center, peak, radius, nb_branches=_DEFAULT_NB_BRANCHES, color=_DEFAULT_COLOR):
    for i in range(nb_branches):
        tip = ( center[0] + radius * math.cos(2 * math.pi * i / nb_branches),
                center[1] + radius * math.sin(2 * math.pi * i / nb_branches))
        pygame.draw.line(window, color, peak, tip)
    flip()

while True:
    snowflake((100, 100), 50)
    cone((150, 50), (150, 200), 100)
    pt()
    pt()
    pt()
