import math
import numpy as np
import random

from car import Car
from road import Road
from util import get_heading

class RoadManager:
    """
    Manages and spawns roads dynamically.
    """

    ROAD_TEMPLATES = [ # control points, rotation of last road 
        [[[0.0, 0.0], [0.0, 600.0], [200.0, 1200.0], [-200.0, 1600.0], [0.0, 2200.0],], -np.pi/2,], 
        # [[[0.0, 0.0], [0.0, 600.0], [0.0, 1200.0], [0.0, 1600.0], [0.0, 2200.0],], -np.pi/2,], 
        # [[[0.0, 0.0], [400.0, 600.0],], -np.pi/2,]
    ]

    def __init__(self, x_start: float = 0.0, y_start: float = 0.0) -> None:
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_start
        self.y_end = y_start
        self.roads: list[Road] = []

        self.spawn_new_road()

    def spawn_new_road(self) -> None:
        control_points = random.choice(self.ROAD_TEMPLATES)
        self.x_start, self.y_start = self.x_end, self.y_end

        new_road = Road(control_points, self.x_start, self.y_start)

        self.x_end, self.y_end = new_road.get_last_point

        self.roads.append(new_road)

    def check_goal(self, car_position: tuple[float, float]) -> bool:
        car = np.array(car_position[:2])
        end = np.array([self.x_end, self.y_end])
        distance = np.linalg.norm(car - end)

        if distance < 50:
            print(f"🎉 Goal reached (distance={distance:.2f}) — spawning new road...")
            # self.spawn_new_road()
            return True
        return False

    def check_car_on_road(self, car_position: tuple[float, float]) -> float :
        """ returns a signed distnce based on which side of the road """
        min_distance = math.inf
        current_road_dir = 0.0
        for j in range(1, len(self.roads[-1].spline_points)):
            current = self.roads[-1].spline_points[j]
            last = self.roads[-1].spline_points[j-1]

            road_dir = get_heading(current, last)
            vec_to_car = np.array(car_position[:2]) - np.array(current)

            road_perp = np.array([-road_dir[1], road_dir[0]])
            signed_distance = np.dot(vec_to_car, road_perp)

            distance = np.linalg.norm(np.array((current[0], current[1])) - np.array(car_position[:2]))
            distance *= np.sign(signed_distance)

            if abs(distance) < abs(min_distance): ## change so that it checks if its on the road by checking distance < road size 
                min_distance = distance 
                current_road_dir = road_dir

        return min_distance, current_road_dir


    def get_road_direction(): 

        pass
    def draw(self, pg, screen , camera) -> None:
        for road in self.roads:
            road.draw(pg, screen, camera)

    def update(self) -> None:
        pass
