import sys
import pygame as pg
import numpy as np
import math

from car import Car
from roadManager import RoadManager
from road import Road
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
        my_road_manager.update()
        my_road_manager.check_goal((my_car.x, my_car.y))

        check_car_on_road(my_road_manager.roads[0], (my_car.x, my_car.y))

        # Draw
        screen.fill((255, 255, 255))


        my_road_manager.draw(pg,screen)
        my_car.draw(pg, screen)

        


        pg.display.flip()
    pg.quit()
    sys.exit()

def check_car_on_road(road: Road, car_position: Car):
    min_distance = math.inf

    for j in road.spline_points:
        distance = np.linalg.norm(np.array((j[0], j[1])) - np.array((car_position[0], car_position[1])))
        min_distance = min(distance, min_distance)

    return min_distance


if __name__ == "__main__":
    main()