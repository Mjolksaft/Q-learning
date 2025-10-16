import sys
import pygame as pg
import numpy as np

def main():
    pg.init()
    size = (800, 600)
    screen = pg.display.set_mode(size)
    running = True

    control_points 


    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False
        
        screen.fill((255, 255, 255))  # background color

            ## updates the screen
        pg.display.flip()
    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()