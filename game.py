# req stands for requirements
from REQ import *
from PNE import Player,Enemy,Block
import math,random,string,time

def get_angle(weapn):
    mouse_pos = pygame.mouse.get_pos()
    x,y = weapn.x,weapn.y
    new_y,new_x = mouse_pos[1] - y, mouse_pos[0] - x
    angle = math.atan2(-new_y,new_x)
    angle = math.floor(math.degrees(angle))    
    return round(angle)

def draw(player,enemy,block):
    mx,my = pygame.mouse.get_pos()
    WINDOW.fill(VARIABLE.BACKGROUND)
    s_pos = (40, (VARIABLE.HEIGHT // 2 ) - 200)
    WINDOW.blit(VARIABLE.SCORE.render(f'{player.score}',True,VARIABLE.RED),s_pos)
    player.draw()
    player.draw_weapons()
    block.draw()
    player.update_bullet(enemy)
    enemy.draw()
    taget_rect = WEAPON.TARGET.get_rect(center=(mx,my))
    WINDOW.blit(WEAPON.TARGET,taget_rect)
    pygame.display.update()
    pygame.mouse.set_visible(False)

def game_paused():
    pos = ((VARIABLE.WIDTH // 2), (VARIABLE.HEIGHT // 2))
    WINDOW.blit(WEAPON.PAUSE,(pos[0]+125,pos[1]))
    message = 'GAME  PAUSED'
    WINDOW.blit(VARIABLE.PAUSE.render(message,True,VARIABLE.GREEN),pos)
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

def game(): 
    pygame.display.set_caption('Super Hash')
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
    
    running = True
    paused = False
    while running:
        CLOCK.tick(VARIABLE.FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    paused = not paused
                if event.key == K_w:
                    player.can_jump = True
                    #player.start_pos = player.player.y 
            if event.type == MOUSEBUTTONUP:
                player.shoot()
        if paused:
            game_paused()
            continue
        if player.can_jump:
            player.jump()
        handle_controlls(player,enemy,block)
        draw(player,enemy,block)
    pygame.quit()      

if __name__ == '__main__':
    game()