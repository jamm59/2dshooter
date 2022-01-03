import threading
from GAME import game
from PNE import Menu
from REQ import *

def draw_tile(pos,color1,color2):
    width,height = 80,50
    rect1 = pygame.Rect(pos[0],pos[1],width,height)
    rect2 = pygame.Rect(pos[0]+rect1.width,pos[1]+rect1.height,width,height)
    pygame.draw.rect(WINDOW,color1,rect1,border_radius=4)
    pygame.draw.rect(WINDOW,color2,rect2,border_radius=4)

def draw(menu):
    WINDOW.fill(VARIABLE.WHITE)
    #drawing decorations for the menu ui
    draw_tile((VARIABLE.WIDTH-400,VARIABLE.HEIGHT-200),VARIABLE.RED,VARIABLE.YELLOW)
    draw_tile((40,180),VARIABLE.YELLOW,VARIABLE.RED)
    draw_tile((VARIABLE.WIDTH-250,300),VARIABLE.YELLOW,VARIABLE.RED)
    T_FONT = VARIABLE.TITLE.render('SUPER HASH',True,VARIABLE.RED)
    WINDOW.blit(T_FONT,(80,40))
    menu.draw()
    if menu.want_to_quit:
        menu.draw_quit()
    mouse_pos = pygame.mouse.get_pos()
    WINDOW.blit(WEAPON.MOUSE_P,mouse_pos)
    pygame.mouse.set_visible(False)
    pygame.display.update()
    
def main(): 
    pygame.display.set_caption('Menu')
    menu = Menu()
    menu.update_menu_items()
    run = True
    while run:
        CLOCK.tick(VARIABLE.FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            if event.type == KEYDOWN:
                if event.key == K_UP or event.key == K_w:
                    if menu.index <= 1:
                        menu.index = len(menu.menu_names)
                    else:
                        menu.index -= menu.counter
                elif event.key == K_DOWN or event.key == K_s:
                    if menu.index >= len(menu.menu_names):
                        menu.index = 1
                    else:
                        menu.index += menu.counter
            menu.check_collision_with_mouse(event)
        if menu.quit:
            run = False
        if menu.new_start:
            game(menu)
        draw(menu)
    
    pygame.quit()  
        
if __name__ == '__main__':
    main()