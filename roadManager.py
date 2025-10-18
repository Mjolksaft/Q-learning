import numpy as np
from road import Road
import random

class RoadManager:
    """
    Manages and spawns roads dynamically.
    """

    ROAD_TEMPLATES = np.array([
        [[0.0, 0.0], [0.0, 100.0], [200.0, 150.0]],
        [[0.0, 0.0], [0.0, 100.0], [200.0, 250.0]],
        [[0.0, 0.0], [0.0, 150.0], [200.0, 100.0]],
    ])

    def __init__(self, x_start: float = 0.0, y_start: float = 0.0) -> None:
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_start
        self.y_end = y_start
        self.roads: list[Road] = []

        self.spawn_new_road()

    def spawn_new_road(self) -> None:
        control_points = random.choice(self.ROAD_TEMPLATES)

        new_road = Road(control_points, self.x_start, self.y_start)

        self.x_end, self.y_end = new_road.get_last_point
        self.x_start, self.y_start = self.x_end, self.y_end

        self.roads.append(new_road)

    def check_goal(self, car_position: tuple[float, float]) -> None:
        car = np.array(car_position[:2])
        end = np.array([self.x_end, self.y_end])
        distance = np.linalg.norm(car - end)

        if distance < 25:
            print(f"🎉 Goal reached (distance={distance:.2f}) — spawning new road...")
            self.spawn_new_road()


    def draw(self, pg, screen) -> None:
        for road in self.roads:
            road.draw(pg, screen)

    def update(self) -> None:
        pass
