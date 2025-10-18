import sys
import pygame as pg

from camera import Camera
from car import Car
from roadManager import RoadManager

my_road_manager = RoadManager(0.0, 0.0)
my_car = Car(20.0)
my_camera = Camera(800, 600)

def main():
    pg.init()
    size = (800, 600)
    screen = pg.display.set_mode(size)
    running = True
    clock = pg.time.Clock()
    # small font for HUD (FPS)
    try:
        font = pg.font.Font(None, 24)
    except Exception:
        pg.font.init()
        font = pg.font.Font(None, 24)

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

        # Update 
        my_car.update(dt, accel, steer)

        #misc
        my_camera.set_position((my_car.x, my_car.y))
        my_road_manager.check_goal((my_car.x, my_car.y))
        my_road_manager.check_car_on_road((my_car.x, my_car.y))

        # Draw
        screen.fill((255, 255, 255))
        my_road_manager.draw(pg,screen, my_camera)
        my_car.draw(pg, screen, my_camera)

        # FPS counter (top-left)
        fps = clock.get_fps()
        fps_surf = font.render(f"{fps:4.1f} FPS", True, (0, 0, 0))
        screen.blit(fps_surf, (10, 10))

        pg.display.flip()
    pg.quit()
    sys.exit()



if __name__ == "__main__":
    main()
