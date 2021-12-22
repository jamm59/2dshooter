# req stands for requirements
from req import *
from PNE import Player,Enemy
import math
import random

def get_angle(weapn):
    mouse_pos = pygame.mouse.get_pos()
    x,y = weapn.x,weapn.y
    new_y,new_x = mouse_pos[1] - y, mouse_pos[0] - x
    angle = math.atan2(-new_y,new_x)
    angle = math.floor(math.degrees(angle))    
    return round(angle)

def draw(player,enemy):
    mx,my = pygame.mouse.get_pos()
    WINDOW.fill(BACK)
    s_pos = ((W_WIDTH // 2)-50, (W_HEIGHT // 2 ) - 100)
    WINDOW.blit(SCORE.render(f'{player.score}',True,RED),s_pos)
    player.draw()
    player.draw_weapons()
    player.update_bullet(enemy)
    enemy.draw()
    WINDOW.blit(weapon.TARGET,(mx-11,my-11))
    pygame.display.update()

def game_paused():
    pos = ((VAR.width // 2) - 300, (VAR.height // 2)-150)
    hand = pygame.transform.rotozoom(weapon.PAUSE,0,0.5)
    WINDOW.blit(hand,(pos[0]+125,pos[1]))
    message = 'GAME             PAUSED'
    WINDOW.blit(PAUSE_FONT.render(message,True,BLACK),pos)
    pygame.display.update()

def handle_controlls(player,enemy):
    enemy.move()
    player.move()

def main():
    player = Player(50,70,W_WIDTH // 2,W_HEIGHT-100)
    #players initial weapon
    w_pos = (player.player.x+10,player.player.y + 25)
    player.update_weapon(weapon.R_IMG,w_pos)
    #enemy 
    enemy = Enemy()

    running = True
    paused = False
    while running:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    paused = not paused
                if event.key == K_w:
                    player.can_jump = True

            if event.type == MOUSEBUTTONUP:
                player.shoot()
        if paused:
            game_paused()
            continue

        if player.can_jump:
            player.jump()

        angle = get_angle(player.player)
        player.rotate_weapon(weapon.R_IMG,angle)
        enemy.create_enemy()
        handle_controlls(player,enemy)
        draw(player,enemy)

    pygame.quit()
      
if __name__ == '__main__':
    main()