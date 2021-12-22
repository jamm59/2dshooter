from req import *
import math
import random

class Bulletobject:
    def __init__(self,image,rect,position,velocity,angle):
        self.rect,self.pos,self.vel = rect,position,velocity
        self.radius,self.width,self.angle = 5, 3,angle
        self.collided = False

    def get_angle(self,enemy):
        ex,ey = enemy[0],enemy[1]
        x,y = self.rect.x,self.rect.y
        d_y,d_x = ey - y, ex - x
        angle = math.atan2(-d_y,d_x)
        return round(angle)

    def rotate_bullet(self,angle):
        angle = round(math.degrees(angle - 90))
        self.image = pygame.transform.rotozoom(weapon.B1_IMG,angle,0.3)

    def follow_enemy(self,angle):
        new_x,new_y = math.cos(angle),math.sin(angle)
        #changing the direction of the bullet before it follow the enemy
        self.vel = 20
        self.rect.x +=  new_x * self.vel
        self.rect.y -= new_y * self.vel


class Player:
    def __init__(self,width,height,x,y):
        self.width,self.height = width,height
        self.x,self.y =x, y
        self.player = pygame.Rect(x,y,width,height)
        self.acc = .85
        self.vel = 10
        self.jump_vel = -20
        self.can_jump = False
        self.maxx_height = self.y - 200
        self.score = 0

        # players weapon
        self.weapon_img = None
        self.weapon_pos = None

        # player bullet
        self.bull_list = []
        self.c = 20
        self.bull_angle = 90
        

    def draw(self):
        pygame.draw.rect(WINDOW,RED,self.player) 
        self.another = pygame.Rect(self.player.x+4,self.player.y+5,self.width-8,self.height-8)
        pygame.draw.rect(WINDOW,WHITE,self.another)

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
        self.bull_angle = math.radians(angle)
        angle -= 55
        new_w = pygame.transform.rotozoom(weapon, angle,1)
        self.weapon_img = new_w
    
    def shoot(self):
        self.bullet = pygame.transform.rotozoom(weapon.B1_IMG,0,0.3)
        pos = (self.player.x + 40,self.player.y + 20)
        rec = self.bullet.get_rect(center=pos)
        angle = self.bull_angle
        self.bull_angle = 90
        if len(self.bull_list) < 20:
            p_weapon = Bulletobject(self.bullet,rec,pos,self.c,angle)
            self.bull_list.append(p_weapon)

    def update_bullet(self,Enemy):
        count = 0
        for bullet in self.bull_list:
            bullet.follow_enemy(bullet.angle)
            for enemy in Enemy.Elist:   
                if pygame.Rect.colliderect(bullet.rect,enemy.rect):
                    Enemy.Elist.remove(enemy)
                    self.score += 1
                    bullet.collided = True
                elif pygame.Rect.colliderect(bullet.rect,enemy.rect) or bullet.rect.y <= 0:    
                    bullet.width = 0
                    try:
                        self.bull_list.remove(bullet)
                    except ValueError as err:
                        pass
            pygame.draw.circle(WINDOW,BLACK,(bullet.rect.x,bullet.rect.y+1),bullet.radius,bullet.width)
            if bullet.radius >= 500:
                bullet.collided = False
                


class Enemyobject:
    def __init__(self,image,rect,pos,speed):
        self.image,self.rect,self.pos,self.vel = image,rect,pos,speed
        
class Enemy:
    def __init__(self):
        self.Elist = []  
        self.vel = 5
        self.count = 100
          
    def create_enemy(self):
        pos = (self.count,20)
        self.count = random.randint(100,W_WIDTH - 100)
        rect = weapon.E_IMG.get_rect(center=pos)
        enemy = Enemyobject(weapon.E_IMG,rect,pos,self.vel)
        if len(self.Elist) <= 20 and random.randint(0,10) == 5:
            self.Elist.append(enemy)
    
    def draw(self):
        for enemy in self.Elist:
            WINDOW.blit(enemy.image,enemy.rect)

    def move(self):
        for enemy in self.Elist:
            enemy.rect.y += enemy.vel
            if enemy.rect.y >= W_HEIGHT:
                self.Elist.remove(enemy)

