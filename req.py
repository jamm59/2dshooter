import pygame
from pygame.locals import *
pygame.font.init()

class Variables:
    def __init__(self):
        self.width = 1000
        self.height = 800

class Weapons:
    def __init__(self):
        __DIR = 'assets/weapons'
        angle = 0
        self.x,self.y = 0,0
        # trying to reduce the size of the image and changing it direction
        self.R_IMG = pygame.image.load(f'{__DIR}/mgun.png')
        # self.L_IMG = pygame.image.load(f'{__DIR}/left.png')
        # self.SHOT_L = pygame.transform.rotozoom(self.L_IMG,angle,0.9)
        # self.ASSIST = pygame.transform.scale(pygame.image.load(f'{__DIR}/assist.png'),(width,height))
        # self.FGUN = pygame.transform.scale(pygame.image.load(f'{__DIR}/firegun.png'),(width,height))
        # self.MGUN = pygame.transform.scale(pygame.image.load(f'{__DIR}/mgun.png'),(width,height))
        self.PAUSE = pygame.image.load(f'{__DIR}/pause.png')
        self.B1_IMG = pygame.image.load(f'{__DIR}/bullet.png')
        self.E_IMG = pygame.image.load(f'{__DIR}/enemy.png')
        self.TARGET = pygame.image.load(f'{__DIR}/target.png')
        # self.BULL2 = pygame.transform.scale(pygame.image.load(f'{__DIR}/bullet2.png'),(width,height))

weapon = Weapons()
#font 
PAUSE_FONT = pygame.font.SysFont('georgia', 60)
SCORE = pygame.font.SysFont('calibri', 150)
#variables
VAR = Variables()
#clock and fps
CLOCK = pygame.time.Clock()
FPS = 60
#screen and stuff
W_WIDTH,W_HEIGHT = 1000,800
WINDOW = pygame.display.set_mode((W_WIDTH,W_HEIGHT))
pygame.display.set_caption('Super Hash')

#COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)
BACK = (250, 237, 240)
RED = (255, 95, 126)
