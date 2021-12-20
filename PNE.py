from req import *
import math
import random

class Bulletobject:
    def __init__(self,image,rect,position,velocity):
        self.image,self.rect,self.pos,self.vel = image,rect,position,velocity

    def get_angle(self,enemy):
        ex,ey = enemy.x,enemy.y
        x,y = self.rect.x,self.rect.y
        new_y,new_x = ex - y, ey - x
        angle = math.atan2(-new_y,new_x)
        # returns angle in radians
        return round(angle)

    def rotate_bullet(self,x,y):
        angle = 0
        if x == -1 and y == -1:
            angle = 45    # top left
        elif x == -1 and y == 0:
            angle = 90    # left
        elif x == -1 and y == 1:
            angle = 135    # bottom left
        elif x == 0 and y == -1:
            angle = 0    # top
        elif x == 0 and y == 0:
            angle = angle   # no position
        elif x == 0 and y == 1:
            angle = 180   #  bottom
        elif x == 1 and y == -1:
            angle = -45   # top right
        elif x == 1 and y == 0:
            angle = -90   # right 
        elif x == 1 and y == 1:
            angle = -135   # bottom right
        
        self.image = pygame.transform.rotozoom(weapon.B1_IMG,angle,0.4)

    def follow_enemy(self,angle):
        new_x,new_y = math.floor(math.cos(angle)),math.floor(math.sin(angle))
        self.rotate_bullet(new_x,new_y)
        self.rect.x +=  new_x * self.vel
        self.rect.y -= new_y * self.vel


class Player:
    def __init__(self,width,height,x,y):
        self.x,self.y =x, y
        self.player = pygame.Rect(x,y,width,height)
        self.acc = .85
        self.vel = 10
        self.jump_vel = -20
        self.can_jump = False
        self.maxx_height = self.y - 200

        # players weapon
        self.weapon_img = None
        self.weapon_pos = None

        # player bullet
        self.bull_list = []
        self.c = 10

    def draw(self):
        pygame.draw.rect(WINDOW,WHITE,self.player) 

    def move(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a] and self.player.x > 20:
            self.player.x -= self.vel
        if keys_pressed[pygame.K_d] and self.player.x < W_WIDTH - 70:
            self.player.x += self.vel 

    def jump(self):
        self.jump_vel += self.acc
        self.player.y += math.floor(self.jump_vel)
        if self.player.y >= 700 :
            self.can_jump = False
            self.jump_vel = -20

    def update_weapon(self,w_img,pos):
        self.weapon_pos = pos
        self.weapon_img = pygame.transform.rotozoom(w_img,-45,1)
        
    def draw_weapons(self): 
        WINDOW.blit(self.weapon_img, (self.player.x - 15,self.player.y -10))

    def rotate_weapon(self,weapon,angle):
        pos = self.weapon_pos
        angle -= 55
        new_w = pygame.transform.rotozoom(weapon, angle,1)
        self.weapon_img = new_w
    
    def shoot(self):
        self.bullet = pygame.transform.rotozoom(weapon.B1_IMG,0,0.4)
        pos = (self.player.x,self.player.y)
        rec = self.bullet.get_rect(center=pos)

        if len(self.bull_list) < 5:
            p_weapon = Bulletobject(self.bullet,rec,pos,self.c)
            self.bull_list.append(p_weapon)

    def update_bullet(self):
        for bullet in self.bull_list:
            bullet.rect.y -= bullet.vel
            WINDOW.blit(bullet.image, bullet.rect)
            if bullet.rect.y <= 100:
                bullet.image = pygame.transform.rotozoom(weapon.B1_IMG,180,0.4)
                bullet.vel = -bullet.vel
            if bullet.rect.y >= W_HEIGHT - 100:
                bullet.image = pygame.transform.rotozoom(weapon.B1_IMG,0,0.4)
                bullet.vel = -bullet.vel
                # self.bull_list.remove([bullet,rec,pos,vel])


        

class Enemyobject:
    def __init__(self,image,rect,pos,speed):
        self.image,self.rect,self.pos,self.speed = image,rect,pos,speed
        
class Enemy:
    def __init__(self):
        self.Elist = []  
        self.vel = 1 
        self.count = 10
          
    def create_enemy(self):
        pos = (self.count,20)
        if self.count <= W_WIDTH:
            self.count += 20
        else:
            self.count = 10

        rect = weapon.E_IMG.get_rect(center=pos)
        enemy = Enemyobject(weapon.E_IMG,rect,pos,self.vel)
        if len(self.Elist) <= 5:
            self.Elist.append(enemy)
    
    def draw(self):
        for enemy in self.Elist:
            WINDOW.blit(enemy.image,enemy.rect)

    def move(self):
        for enemy in self.Elist:
            enemy.rect.y += enemy.vel

