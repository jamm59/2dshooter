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

def draw(player):
    mouse_pos = pygame.mouse.get_pos()
    WINDOW.fill(BLACK)
    player.draw()
    player.draw_weapons()
    player.update_bullet()
    pygame.display.update()

def game_paused():
    WINDOW.blit(PAUSE_FONT.render(f'GAME PAUSED',True,WHITE),
    ((VAR.width // 2) - 200, (VAR.height // 2) - 100))
    pygame.display.update()

def handle_controlls(player):
    player.move()

def main():
    player = Player(50,70,W_WIDTH // 2,W_HEIGHT-100)
    #players initial weapon
    w_pos = (player.player.x+10,player.player.y + 25)
    player.update_weapon(
        weapon.R_IMG,
        w_pos
        )
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
        handle_controlls(player)
        draw(player)

    pygame.quit()
      
if __name__ == '__main__':
    main()