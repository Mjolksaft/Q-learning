import sys
import pygame as pg
import numpy as np
from car import Car
from roadManager import RoadManager

from util import build_catmull_rom_chain



my_road_manager = RoadManager(0.0, 0.0)
my_car = Car(20.0)



print(my_car.__repr__())
def main():
    pg.init()
    size = (800, 600)
    screen = pg.display.set_mode(size)
    running = True
    clock = pg.time.Clock()

    while running:
        dt = clock.tick(60) / 1000.0  # seconds since last frame
        
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                running = False

        keys = pg.key.get_pressed()

        accel = 0.0
        steer = 0.0

        if keys[pg.K_UP]:
            accel = my_car.max_accel
        elif keys[pg.K_DOWN]:
            accel = -my_car.max_accel

        if keys[pg.K_LEFT]:
            steer = -my_car.max_steer_rate
        elif keys[pg.K_RIGHT]:
            steer = my_car.max_steer_rate

        # Update car
        my_car.update(dt, accel, steer)
        # print(my_car.speed)

        # Draw
        screen.fill((255, 255, 255))


        my_road_manager.draw(pg,screen)
        my_car.draw(pg, screen)

        


        pg.display.flip()
    pg.quit()
    sys.exit()



if __name__ == "__main__":
    main()