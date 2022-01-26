import math,random,string,threading,time
from REQ import *

def distance(first,second):
    dy,dx = (first[1]-second[1]),(first[0]-second[0])
    return round(math.hypot(dx,dy))

class Bulletobject:
    def __init__(self,image,rect,position,velocity,angle):
        self.rect,self.pos,self.vel = rect,position,velocity
        self.image,self.angle = image,angle
        self.bullet_hit_edge = False
        self.xvel,self.yvel = self.vel,self.vel
        self.deg = round(math.degrees(self.angle))

    def get_angle(self,enemy):
        ex,ey = enemy[0],enemy[1]
        x,y = self.rect.x,self.rect.y
        d_y,d_x = ey - y, ex - x
        angle = math.atan2(-d_y,d_x)
        return round(angle)

    def rotate_bullet(self,angle):
        angle = round(math.degrees(angle - 90))
        self.image = pygame.transform.rotozoom(WEAPON.B1_IMG,angle,0.3)

    def follow_enemy(self,angle):
        new_x,new_y = math.cos(angle),math.sin(angle)
        # changing the direction of the bullet before it follow the enemy
        self.rect.x +=  new_x * self.xvel
        self.rect.y -= new_y * self.yvel


    def hit_edge(self):
        if  self.rect.x <= 30 or self.rect.x >= VARIABLE.WIDTH - 50 or self.rect.y <= 30 or self.rect.y >= VARIABLE.HEIGHT - 50:
            #self.bullet_hit_edge = True
            return True
        return False

class Player:
    def __init__(self,width,height,x,y):
        self.width,self.height = width,height
        self.x,self.y =x, y
        self.player = pygame.Rect(x,y,width,height)
        self.acc,self.vel,self.jump_vel,self.can_jump= .85,10,-20,False
        # fall velocity acceleration and if the player fell
        self.fall,self.fall_acc,self.fall_vel= False,0.01,5
        self.start_pos = VARIABLE.HEIGHT - 100
        self.maxx_height = self.y - 200
        self.score = 0
        # players weapon
        self.weapon_img = None
        self.weapon_pos = None
        # player bullet
        self.bull_list = []
        self.c = 25
        self.bull_angle = 90     
        # block 
        self.block_pos = None
        self.just_left_block = False
        self.circle = Circle()

    def draw(self):
        b_radius = 2
        pygame.draw.rect(WINDOW,VARIABLE.RED,self.player,border_radius=b_radius) 

    def move(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a] and self.player.x > 20:
            self.player.x -= self.vel
        if keys_pressed[pygame.K_d] and self.player.x < VARIABLE.WIDTH - 70:
            self.player.x += self.vel 

        if self.fall:
            self.fall_vel += 0.6
            self.player.y += self.fall_vel

    def jump(self):
        self.jump_vel += self.acc
        self.player.y += math.floor(self.jump_vel)
        if self.player.y >= self.start_pos :
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
        #angle in radians
        rad = self.bull_angle
        self.bull_angle = 90
        #angle in degrees
        deg = round(math.degrees(rad))
        new_img = pygame.transform.rotozoom(WEAPON.BULLET,deg,1)
        pos = (self.player.x + 40,self.player.y + 20)
        rec = new_img.get_rect(center=pos)
        if len(self.bull_list) < 20:
            p_weapon = Bulletobject(new_img,rec,pos,self.c,rad)
            self.bull_list.append(p_weapon)

    def update_bullet(self,Enemy):
        for bullet in self.bull_list:
            if bullet.hit_edge():
                try:
                    self.bull_list.remove(bullet)
                except ValueError as err:
                    pass
            bullet.follow_enemy(bullet.angle)
            for enemy in Enemy.Elist:   
                if pygame.Rect.colliderect(bullet.rect,enemy.rect):
                    Enemy.Elist.remove(enemy)
                    bullet.radius = 0
                    self.score += 1
                    bullet.collided = True
                    self.circle.add_circle((enemy.rect.x,enemy.rect.y))
                if pygame.Rect.colliderect(bullet.rect,enemy.rect):    
                    try:
                        self.bull_list.remove(bullet)
                    except ValueError as err:
                        pass
            
            WINDOW.blit(bullet.image,bullet.rect)   
        self.circle.draw() 


class Enemyobject:
    def __init__(self,image,rect,pos,speed,move=True):
        self.image,self.rect,self.pos,self.vel,self.move_down = image,rect,pos,speed,move
        self.rand_dir = None
        self.lvel = 1
        self.collide_point = None
        self.ground_level = False

class Enemy:
    def __init__(self):
        self.Elist = []  
        self.vel = 5
        self.count = 100
          
    def create_enemy(self):
        if len(self.Elist) <= 5 and random.randint(0,10) == 5:
            pos = (self.count,20)
            self.count = random.randint(100,VARIABLE.WIDTH - 100)

            E_icon = [WEAPON.E_IMG,WEAPON.E1_IMG,WEAPON.E2_IMG]
            #index = random.randint(0,len(E_icon)-1)
            index = 0

            rect = E_icon[index].get_rect(center=pos)
            enemy = Enemyobject(E_icon[index],rect,pos,self.vel)
            enemy.rand_dir = random.randint(1,2)

            self.Elist.append(enemy)
    
    def draw(self):
        for enemy in self.Elist:
            WINDOW.blit(enemy.image,enemy.rect)

    def move(self,b_list):
        for enemy in self.Elist:
            if enemy.move_down:
                enemy.rect.y += enemy.vel
                if enemy.rect.y >= VARIABLE.HEIGHT:
                    self.Elist.remove(enemy)

            if not enemy.move_down or enemy.ground_level:
                if enemy.rand_dir == 1:
                    #move left
                    enemy.rect.x -= enemy.lvel
                else:
                    enemy.rect.x += enemy.lvel

            if not enemy.ground_level and not enemy.move_down:
                for block in b_list:
                    # checking if the enemy reached the edge of the block
                    start,end = enemy.collide_point[0][0],enemy.collide_point[1][0]
                    if enemy.rect.x >= start or enemy.rect.x <= end:
                        enemy.move_down = True
            if enemy.rect.x <= 10 or enemy.rect.x >= VARIABLE.WIDTH-50:
                enemy.lvel = -enemy.lvel

class Blockobject:
    def __init__(self,image,pos):
        self.image,self.pos = image,pos
        self.rect = self.image.get_rect(center=self.pos)
        self.collided_with_player = False

class Block:
    def __init__(self):
        self.block_list = []
        width = VARIABLE.WIDTH
        height = VARIABLE.HEIGHT
        center = (width // 2)
        self.x = [150,width-150,center+10,center+200,center-100,width-150]
        self.y = [height-250,height-300,height-150,height-460,250,100]

    def add_block(self):
        for count in range(0,len(self.x)):
            image = WEAPON.BLOCK
            pos = (self.x[count],self.y[count])
            new_block = Blockobject(image,pos)
            self.block_list.append(new_block)

    def draw(self):
        for block in self.block_list:
            WINDOW.blit(block.image,block.rect)

    def move(self,player):
        if player.can_jump:
            for block in self.block_list:
                block.rect.y += 2
    #block collision with enemy
    def detect_collison1(self,enemy_list):
        for block in  self.block_list:
            for enemy in enemy_list:
                if pygame.Rect.colliderect(block.rect,enemy.rect):
                   enemy.move_down = False
                   enemy.collide_point = (block.rect.midleft,block.rect.midright)
                if enemy.rect.y >= VARIABLE.HEIGHT-70:
                    enemy.ground_level = True
                    enemy.move_down = False
    #collision with player       
    def detect_collison2(self,player):
        for block in self.block_list:
            if pygame.Rect.colliderect(block.rect,player.player):
                # what should happen if player collides with the block from below
                if  player.can_jump and (block.rect.top + 10 <  player.player.y < block.rect.bottom):
                    player.jump_vel = -player.jump_vel 
                # what should happen if player collides with the block from above
                # if player is falling or the player is jumping 
                elif (player.fall or player.can_jump) and player.player.bottom >= block.rect.top:
                    player.start_pos = block.rect.top 
                    player.player.bottom = block.rect.top 
                    player.can_jump = False
                    player.jump_vel = -20
                    player.fall = False
                    player.fall_vel = 10
                    block.collided_with_player = True
                    player.just_left_block = False
                # what should happen if player collides with the block from left
                elif player.player.right >= block.rect.left :
                    player.player.x -= 50
                # what should happen if player collides with the block from right
                elif player.player.left <= block.rect.right :
                    player.player.x += 50
            # if the player jumped and if the player is not at the ground level the the player just left the block
            if player.can_jump and not (player.player.y >= VARIABLE.HEIGHT - 100):
                player.just_left_block = True
            # if the player is not jumping,but is still on the block and is at the edge of edge
            # of either the left or right of the block then the player should fall
            if block.collided_with_player:
                crossed_boundary = (player.player.x < block.rect.left + 2 or player.player.x > block.rect.right)
                if not player.can_jump and crossed_boundary:
                    player.fall = True
                    block.collided_with_player = False
            #if player just left the a block and the player is not jumping then the player should fall
            if player.just_left_block and not player.can_jump:
                player.fall = True
            # if player reached bottom then stop falling
            if player.player.y >= VARIABLE.HEIGHT - 100:
                player.fall = False
                player.fall_vel = 10
                player.start_pos = VARIABLE.HEIGHT - 100

                    

        #print(player.can_jump)

class Circleobject:
    def __init__(self,pos):
        self.radius = 5
        self.width = 2
        self.pos = pos

class Circle:
    def __init__(self):
        self.all_circles = []

    def add_circle(self,pos):
        new_c = Circleobject(pos)
        self.all_circles.append(new_c)

    def draw(self):
        for circle in self.all_circles:
            if circle.radius >= 500:
                try:
                    self.all_circles.remove(circle)
                except ValueError:
                    pass
                else:
                    continue

            pygame.draw.circle(WINDOW,VARIABLE.S_BLUE,circle.pos, circle.radius,circle.width)
            circle.radius += 10

class MenuInfo:
    def __init__(self,text,pos,id):
        self.id = id
        self.text = text
        self.pos = pos
        self.width,self.height = 300,80 
        self.rect = pygame.Rect(self.pos[0],self.pos[1],self.width,self.height)
        self.text_pos = (self.rect.x+50,self.rect.y+20)
        self.font = pygame.font.Font('assets/font/zorque.otf', 35)
        self.radius = 0
        self.hover = False
        self.color = None

class Menu:
    def __init__(self):
        self.menu_names = ['   Play','   Store','   Options','   Quit']
        self.menu_items = []
        self.counter = 1
        self.index = 1
        self.arrow_rect = WEAPON.ARROW.get_rect(center=(0,0))
        self.want_to_quit = False
        self.quit = False
        self.new_text = None
        self.new_start = False
        # if its a new game
        file = open('assets/data/new_game.txt','r')
        # if 1 inside the file the its a new game else its not
        data = file.read()
        file.close()
        if int(data):
            self.new_game = True
            with open('assets/data/new_game.txt','w') as file:
                file.write('0')
        else:
            self.new_game = False

    def update_menu_items(self):
        x = 80
        y = 350
        for i,text in enumerate(self.menu_names):
            id = i + 1
            item = MenuInfo(text,(x,y),id)
            self.menu_items.append(item)
            y += 120

    def hover_animation_check(self,item):
        if item.id == self.index:
            item.rect.width,item.rect.height = 350,100
            item.font = pygame.font.Font('assets/font/zorque.otf', 40)
            item.color = (0, 13, 107)
            self.arrow_rect.x = 460
            self.arrow_rect.y = item.rect.y - 5
        else:
            item.rect.width,item.rect.height = 300,80
            item.font = pygame.font.Font('assets/font/zorque.otf', 35)
            item.color = (255, 150, 173)

    def draw(self):
        for item in self.menu_items:
            self.hover_animation_check(item)
            pygame.draw.rect(WINDOW,item.color,item.rect,border_radius=item.radius)
            font = item.font.render(item.text,True,VARIABLE.WHITE)
            WINDOW.blit(font,item.text_pos)
            WINDOW.blit(WEAPON.ARROW,self.arrow_rect)

    def check_collision_with_mouse(self,event):
        for item in self.menu_items:
            if event.type == MOUSEBUTTONUP:
                mpos = pygame.mouse.get_pos()
                if pygame.Rect.collidepoint(item.rect,mpos):
                    if item.text == '   Play':
                        self.intro()
                    elif item.text == '   Store':
                        pass
                    elif item.text == '   Options':
                        pass
                    else: # Quit
                        self.want_to_quit = True
        
    def draw_quit(self,number):
        FONT = pygame.font.Font('assets/font/JungleAdventurer.ttf', 50)
        if number == 1:
            B = pygame.Rect(200 , 300, 500, 300)
        elif number == 2:
            B = pygame.Rect(500 , 400, 400, 300)
        pygame.draw.rect(WINDOW,(20, 47, 67),B)
        WINDOW.blit(FONT.render("Are you sure you ",True,VARIABLE.WHITE),(B.x + 40, B.y + 50 ))
        WINDOW.blit(FONT.render("want to Exit ?",True,VARIABLE.WHITE),(B.x + 55, B.y + 100))
        yes = WEAPON.YES.get_rect(center=(B.x + 150, B.y + 200 ))
        no = WEAPON.NO.get_rect(center=(B.x + 300, B.y + 200 ))
        WINDOW.blit(WEAPON.YES,yes)
        WINDOW.blit(WEAPON.NO,no)

        mpos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:
            if pygame.Rect.collidepoint(yes,mpos):
                self.quit = True
            if pygame.Rect.collidepoint(no,mpos):
                self.want_to_quit = False

    def wait(self,text,count):
        #this function will update the text after one sec
        if count == len(text):
            self.new_start = True
            return 
        else:
            self.new_text = text[count]
            count += 1
            time.sleep(.1)
            self.wait(text,count) 
        
    def draw_intro(self,text):
        WINDOW.fill(VARIABLE.WHITE)
        top,bottom = pygame.Rect(0,0,VARIABLE.WIDTH,150),pygame.Rect(0,VARIABLE.HEIGHT - 150,VARIABLE.WIDTH,150)
        FONT = pygame.font.Font('assets/font/bomb.ttf',40)
        FONT = FONT.render(self.new_text,True,VARIABLE.BLACK)
        WINDOW.blit(FONT,(10,VARIABLE.HEIGHT // 2))
        pygame.draw.rect(WINDOW,VARIABLE.BLACK,top)
        pygame.draw.rect(WINDOW,VARIABLE.BLACK,bottom)
        pygame.display.update()

    def intro(self):
        with open('assets/data/new_user_info.txt','r') as file:
            intro_text = file.readlines()
        intro_text = [i.strip() for i in intro_text]

        if self.new_game:
            index = 0
        else:
            index = 11

        new_thread = threading.Thread(target=self.wait,args=(intro_text,index))
        new_thread.start()
        running = True
        pause = False
        while running:
            CLOCK.tick(VARIABLE.FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    running = False 
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        pause = not pause

            if self.new_start:
                running = False
            self.draw_intro(intro_text)

        


class Inventory:
    def __init__(self):
        self.weapons_owned = []
        self.task_bar = pygame.Rect(0,0,VARIABLE.WIDTH,70)
        self.lives = 5
        with open('assets/data/balance.txt','r') as file:
            data = file.read()
        self.coin = 0
        self.token = int(data)

    # this is the function for the shop section
    def draw(self):
        pass
    def draw_task_bar(self,player,enemy):
        pygame.draw.rect(WINDOW,(255, 203, 203),self.task_bar)
        if self.lives <= 10:
            #draw lives
            self.f_lives = VARIABLE.TASK_BAR1.render('| L '*self.lives,True,VARIABLE.WHITE)
            # the reason i used variable.pause is because i want to use the same font as the pause menu
            self.FONT1 = VARIABLE.TASK_BAR2.render(f'{" "*7}Z{" "*15}TT',True,VARIABLE.WHITE)
            self.FONT2 = VARIABLE.TASK_BAR2.render(f'{self.coin}{" "*9}{self.token}',True,(20, 47, 67))
            WINDOW.blit(self.f_lives,(50,self.task_bar.height // 2 - 10))
        WINDOW.blit(self.FONT1,(VARIABLE.WIDTH - 300,self.task_bar.height // 2 - 10))
        WINDOW.blit(self.FONT2,(VARIABLE.WIDTH - 300,self.task_bar.height // 2 - 10))

        self.coin = player.score // 5
        for enemy in enemy.Elist:
            if pygame.Rect.colliderect(enemy.rect,player.player):
                self.lives -= 1
                rand_l  = [-1,1]
                new_rand = random.randint(0,1)
                n_speed = rand_l[new_rand] * 200
                enemy.rect.x += n_speed
                

