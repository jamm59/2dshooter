import pygame
from pygame.locals import *
pygame.font.init()

class VARS:
    def __init__(self):
        self.WIDTH = 900
        self.HEIGHT = 950
        self.FPS = 60
        #colors
        self.WHITE  =  (255,255,255)
        self.BLUE   =  (21, 151, 229)
        self.RED    =  (253, 111, 150)
        self.YELLOW =  (255, 164, 0)
        self.GREEN  =  (41, 44, 109)
        self.BLACK  =  (0,0,0)
        self.S_BLUE =  (162, 210, 255)
        self.PURPLE =  (176, 0, 185)
        
        self.NAVY   =  (61, 178, 255)
        self.BACKGROUND   =  (255, 249, 249)
    
        #font 
        self.PAUSE = pygame.font.Font('assets/font/JungleAdventurer.ttf', 60)
        self.TASK_BAR1 = pygame.font.Font('assets/font/PAC-FONT.TTF', 25)
        self.TASK_BAR2 = pygame.font.Font('assets/font/bomb.ttf', 25)
        self.SCORE = pygame.font.Font('assets/font/JungleAdventurer.ttf', 300)
        self.pause_complete = False
        self.pause_length = 2
        self.TITLE = pygame.font.Font('assets/font/bomb.ttf',150)

        # game
        self.game_run = True

class WeaponImage:
    def __init__(self):
        __DIR = 'assets'
        self.x,self.y = 0,0
        self.BACKGROUND = pygame.image.load(f'{__DIR}/others/background.png')
        self.YES = pygame.transform.rotozoom(pygame.image.load(f'{__DIR}/others/yes.png'),0,0.8)
        self.NO = pygame.transform.rotozoom(pygame.image.load(f'{__DIR}/others/no.png'),0,0.6)
        self.ARROW = pygame.transform.rotozoom(pygame.image.load(f'{__DIR}/others/arrow.png'),180,1.7)
        self.BLOCK = pygame.transform.scale(pygame.image.load(f'{__DIR}/weapons/block.png'),(200,50))
        self.R_IMG = pygame.image.load(f'{__DIR}/weapons/mgun.png')
        self.PAUSE = pygame.image.load(f'{__DIR}/weapons/pause.png')
        self.BULLET = pygame.transform.scale(pygame.image.load(f'{__DIR}/weapons/bullet.png'),(20,30))
        self.N_BULLET = pygame.image.load(f'{__DIR}/weapons/new_bullet.png')
        self.E_IMG = pygame.image.load(f'{__DIR}/enemy/enemy.png')
        self.E1_IMG = pygame.image.load(f'{__DIR}/enemy/enemy1.png')
        self.E2_IMG = pygame.image.load(f'{__DIR}/enemy/enemy2.png')
        self.MOUSE_P = pygame.image.load(f'{__DIR}/others/mouse-pointer.png')
        self.TARGET = pygame.image.load(f'{__DIR}/weapons/target.png')


#variables
VARIABLE = VARS()
WEAPON = WeaponImage()

#screen and stuff
WINDOW = pygame.display.set_mode((VARIABLE.WIDTH,VARIABLE.HEIGHT))
CLOCK = pygame.time.Clock()
        