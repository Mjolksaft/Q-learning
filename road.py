import numpy as np

from util import build_catmull_rom_chain, rotate_spline


class Road:
    def __init__(self, template, x: float = 0.0, y: float = 0.0, angle: float = 0.0):
        self.x = x
        self.y = y
        self.angle = template[1]

        # generate road
        padded = np.vstack([template[0][0], template[0], template[0][-1]])
        spline_points = build_catmull_rom_chain(padded, 50)
        self.spline_points = rotate_spline(
            spline_points, self.angle
        )  ## ROTATE THEN TRANSLATE !!!!!
        self.spline_points += np.array([self.x, self.y])

    def update(self) -> None:
        print("hello world")

    @property
    def get_last_point(self) -> np.ndarray:
        return self.spline_points[-1][0], self.spline_points[-1][1]

    def draw(self, pg, screen, camera) -> None:
        for p in self.spline_points:
            world_pos = np.array(p) - camera.get_pos()
            pg.draw.circle(screen, "RED", world_pos.astype(int), 50)

        for p in self.spline_points:
            world_pos = tuple(np.array(p) - np.array(camera.get_pos()))
            pg.draw.circle(screen, "BLACK", world_pos, 1)
