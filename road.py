import numpy as np
from util import build_catmull_rom_chain

class Road:
    def __init__(self, control_points: np.ndarray, x: float = 0.0, y: float = 0.0, angle: float = 0.0):
        self.x = x
        self.y = y
        self.angle = angle

        # generate road 
        padded = np.vstack([control_points[0], control_points, control_points[-1]])
        padded += np.array([self.x, self.y])
        self.spline_points = build_catmull_rom_chain(padded, 50)

        print(self.spline_points[0])


    def update(self) -> None:
        print("hello world")

    @property
    def get_last_point(self) -> np.ndarray:
        return self.spline_points[-1][0], self.spline_points[-1][1]

    def draw(self, pg, screen, camera) -> None:
        for p in self.spline_points:
            world_pos = tuple(np.array(p) - np.array(camera.get_pos()))
            pg.draw.circle(screen, 'RED', world_pos, 50)
        
        for p in self.spline_points:
            world_pos = tuple(np.array(p) - np.array(camera.get_pos()))
            pg.draw.circle(screen, 'BLACK', world_pos, 1)

