import threading
from GAME import game
from PNE import Menu
from REQ import *


def draw(menu):
    WINDOW.fill(VARIABLE.WHITE)
    menu.draw()
    pygame.display.update()
    
def main(): 
    pygame.display.set_caption('Menu')
    menu = Menu()
    menu.update_menu_items()
    run = True
    paused = False
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
        #print(menu.index)
        draw(menu)
    
    pygame.quit()  
        

if __name__ == '__main__':
    main()