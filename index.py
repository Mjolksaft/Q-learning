import sys
import pygame as pg
import numpy as np
from car import Car


def catmull_rom(p0, p1, p2, p3, n_points=20):
    t = np.linspace(0, 1, n_points)[:, None]
    p0, p1, p2, p3 = map(np.array, (p0, p1, p2, p3))
    a = 2*p1
    b = -p0 + p2
    c = 2*p0 - 5*p1 + 4*p2 - p3
    d = -p0 + 3*p1 - 3*p2 + p3
    return 0.5 * (a + (b*t) + (c*t**2) + (d*t**3))


def build_catmull_rom_chain(points, samples_per_segment=100):
    curve = []
    for i in range(len(points) - 3):
        seg = catmull_rom(points[i], points[i+1], points[i+2], points[i+3], samples_per_segment)
        curve.extend(seg)
    return np.array(curve)

control_points = np.array([
    [100, 0],
    [100, 300],
    [500, 300]
])

padded = np.vstack([control_points[0], control_points, control_points[-1]])
spline_points = build_catmull_rom_chain(padded, 50)

my_car = Car(20.0)

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

        # draw road before car
        for p in spline_points:
            pg.draw.circle(screen, (255, 100, 100), p.astype(int), 50)
        
        my_car.draw(pg, screen)


        


        pg.display.flip()
    pg.quit()
    sys.exit()



if __name__ == "__main__":
    main()