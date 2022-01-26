# req stands for requirements
from REQ import *
from PNE import Player,Enemy,Block,Menu,Inventory
import math,random,string,time,sys

def get_angle(weapn):
    mouse_pos = pygame.mouse.get_pos()
    x,y = weapn.x,weapn.y
    new_y,new_x = mouse_pos[1] - y, mouse_pos[0] - x
    angle = math.atan2(-new_y,new_x)
    angle = math.floor(math.degrees(angle))    
    return round(angle)

def draw(player,enemy,block,inventory):
    mx,my = pygame.mouse.get_pos()
    WINDOW.fill(VARIABLE.BACKGROUND)
    s_pos = (40, (VARIABLE.HEIGHT // 2 ) - 180)
    WINDOW.blit(VARIABLE.SCORE.render(f'{player.score}',True,VARIABLE.RED),s_pos)
    player.draw()
    player.draw_weapons()
    block.draw()
    player.update_bullet(enemy)
    enemy.draw()
    taget_rect = WEAPON.TARGET.get_rect(center=(mx,my))
    WINDOW.blit(WEAPON.TARGET,taget_rect)
    inventory.draw_task_bar(player,enemy)
    pygame.display.update()
    pygame.mouse.set_visible(False)

def game_paused(menu):
    if VARIABLE.pause_length < 400:
        VARIABLE.pause_length += 25
    #rect
    pause_rect = pygame.Rect(VARIABLE.WIDTH-400,0,VARIABLE.pause_length,VARIABLE.HEIGHT)
    main_rect = pygame.Rect(VARIABLE.WIDTH-300,100,200,70)
    quit_rect = pygame.Rect(VARIABLE.WIDTH-300,210,200,70)
    #display rect
    pygame.draw.rect(WINDOW,VARIABLE.RED,pause_rect)
    pygame.draw.rect(WINDOW,VARIABLE.WHITE,main_rect)
    pygame.draw.rect(WINDOW,VARIABLE.WHITE,quit_rect)
    # rect collision
    mouse_pressed = pygame.mouse.get_pressed()
    if mouse_pressed[0]:
        mouse_pos = pygame.mouse.get_pos()
        if pygame.Rect.collidepoint(main_rect,mouse_pos):
            VARIABLE.game_run = False
        if pygame.Rect.collidepoint(quit_rect,mouse_pos):
            menu.want_to_quit = True
    #font
    FONT = VARIABLE.PAUSE.render('GAME PAUSED',True,VARIABLE.WHITE)
    FONT_MAIN = VARIABLE.PAUSE.render('   MENU',True,VARIABLE.BLACK)
    FONT_QUIT = VARIABLE.PAUSE.render('   QUIT',True,VARIABLE.BLACK)
    # display font
    WINDOW.blit(FONT,(VARIABLE.WIDTH-360,10))
    WINDOW.blit(FONT_MAIN,(main_rect.x-10,main_rect.y+10))
    WINDOW.blit(FONT_QUIT,(quit_rect.x-10,quit_rect.y+10))
    WINDOW.blit(WEAPON.PAUSE,(VARIABLE.WIDTH-250,VARIABLE.WIDTH // 2))
    if menu.want_to_quit:
        menu.draw_quit(2)
    if menu.quit:
        pygame.quit()
        sys.exit()
    pygame.mouse.set_visible(True)
    pygame.display.update()

def handle_controlls(player,enemy,block):
    #player
    angle = get_angle(player.player)
    player.rotate_weapon(WEAPON.R_IMG,angle)
    player.move()
    #enemy
    enemy.create_enemy()
    enemy.move(block.block_list)
    #block
    block.detect_collison1(enemy.Elist)
    block.detect_collison2(player)

def game(menu): 
    pygame.display.set_caption('Super Hash')
    # inventory 
    inventory = Inventory()
    # player object
    player = Player(50,80,40,VARIABLE.HEIGHT-100)
    #players initial weapon
    w_pos = (player.player.x+10,player.player.y + 25)
    player.update_weapon(WEAPON.R_IMG,w_pos)
    #enemy 
    enemy = Enemy()
    #block
    block = Block()
    block.add_block()
    
    paused = False
    while VARIABLE.game_run:
        CLOCK.tick(VARIABLE.FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                VARIABLE.game_run = False
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    paused = not paused
                if event.key == K_w:
                    player.can_jump = True
            if event.type == MOUSEBUTTONUP:
                player.shoot()
        if paused:
            game_paused(menu)
            continue
        else:
            VARIABLE.pause_length = 2
        if player.can_jump:
            player.jump()
        handle_controlls(player,enemy,block)
        draw(player,enemy,block,inventory)
        
    menu.new_start = False      


if __name__ == '__main__':
    menu = Menu()
    game(menu)