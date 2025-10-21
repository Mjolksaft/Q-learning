import sys
import pygame as pg
import numpy as np

from ai import AiController
from camera import Camera
from car import Car
from playerController import PlayerController
from roadManager import RoadManager

# Initialize core objects
my_road_manager = RoadManager(0.0, 0.0)
my_car = Car(20.0)
my_camera = Camera(800, 600)
my_ai = AiController(200.0, my_car, my_road_manager) 
my_player_controller = PlayerController(my_car)

def main():
    pg.init()
    size = (800, 600)
    screen = pg.display.set_mode(size)
    running = True
    clock = pg.time.Clock()
    font = pg.font.Font(None, 24)

    while running:
        dt = clock.tick(60) / 1000.0  # seconds since last frame

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                running = False

        signed_distance, road_dir = my_road_manager.check_car_on_road((my_car.x, my_car.y))

        my_ai.update_car(dt)
        # my_player_controller.update(pg, dt)
        my_camera.set_position((my_car.x, my_car.y))

        screen.fill((255, 255, 255))
        my_road_manager.draw(pg, screen, my_camera)
        my_car.draw(pg, screen, my_camera)


        car_dir = np.array([np.cos(my_car.heading), np.sin(my_car.heading)])
        next_heading_alignment = np.dot(car_dir, road_dir)
        # HUD info
        fps = clock.get_fps()
        info_text = f"FPS: {fps:4.1f}  Dist: {signed_distance:6.1f} car_align: {next_heading_alignment:6.2f} Reward: {my_ai.action:6.1f}"
        fps_surf = font.render(info_text, True, (0, 0, 0))
        screen.blit(fps_surf, (10, 10))

        pg.display.flip()

    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
