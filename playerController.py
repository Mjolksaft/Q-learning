from car import Car


class PlayerController:
    """Handles player keyboard input and controls the car."""

    def __init__(self, car: Car) -> None:
        self.car = car

    def update(self, pg, dt: float) -> None:
        keys = pg.key.get_pressed()
        accel = 0.0
        steer = 0.0

        if keys[pg.K_UP]:
            accel = self.car.max_accel
        elif keys[pg.K_DOWN]:
            accel = -self.car.max_accel

        if keys[pg.K_LEFT]:
            steer = -self.car.max_steer_rate
        elif keys[pg.K_RIGHT]:
            steer = self.car.max_steer_rate

        self.car.update(dt, accel, steer)
