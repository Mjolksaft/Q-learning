import math
from dataclasses import dataclass, asdict, replace

@dataclass
class Car:
    """
    Simple 2D point-mass car with heading (radians).
    - position: (x, y)
    - heading: angle in radians, 0 = +x
    - speed: forward speed (can be negative for reverse)
    Controls:
    - update(dt, accel, steer): accel in m/s^2, steer in rad/s (rate)
    """
    
    size: float
    x: float = 0.0
    y: float = 0.0
    heading: float = 0.0
    speed: float = 100.0

    max_speed: float = 100.0
    max_reverse_speed: float = -10.0 
    max_accel: float = 20.0
    max_steer_rate: float = math.radians(90.0)
    friction: float = 0.5

    def update(self, dt: float, accel: float = 0.0, steer_rate: float = 0.0) -> None:
        if dt <= 0:
            return

        # clamp controls
        accel = max(-self.max_accel, min(self.max_accel, accel))
        steer_rate = max(-self.max_steer_rate, min(self.max_steer_rate, steer_rate))

        # apply friction as opposing acceleration (simple model)
        friction_acc = -self.friction * (1 if self.speed > 0 else -1) if abs(self.speed) > 1e-6 else 0.0

        # net acceleration
        net_accel = accel + friction_acc

        # integrate speed
        self.speed += net_accel * dt
        # clamp speed (allow reverse up to max_reverse_speed)
        self.speed = max(self.max_reverse_speed, min(self.max_speed, self.speed))

        # integrate heading
        self.heading += steer_rate * dt
        # normalize heading to [-pi, pi)
        self.heading = (self.heading + math.pi) % (2 * math.pi) - math.pi

        # integrate position (simple forward motion)
        dx = math.cos(self.heading) * self.speed * dt
        dy = math.sin(self.heading) * self.speed * dt
        self.x += dx
        self.y += dy

    def draw(self, pg, screen, camera) -> None:
        # pg.draw.circle(screen, 'BLUE', (int(self.x), int(self.y)), self.size)
        pg.draw.circle(screen, 'BLUE', (400,300), self.size)