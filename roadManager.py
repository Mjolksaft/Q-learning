import numpy as np
from road import Road

class RoadManager:
    """
    Manages and spawns new roads.
    """

    road_control_points_array = np.array([
        [
            [0.0, 0.0],
            [0.0, 350.0],
            [200.0, 400.0]
        ], 
        [
            [0.0, 0.0],
            [0.0, 350.0],
            [200.0, 700.0]
        ],
        [
            [0.0, 0.0],
            [0.0, 350.0],
            [200.0, 400.0]
        ]

    ])

    def __init__(self, x_start: float, y_start: float) -> None:
        self.x_start = x_start
        self.y_start = y_start
        self.roads = []

        # build the first road 
        new_road = Road(self.road_control_points_array[2], self.x_start, self.y_start)

        self.x_end, self.y_end = new_road.get_last_point  # get the last point to check goal

        self.roads.append(new_road)


    def update(self, car_position) -> None:
        # check the position of the car and to see if the car is at the end of the road 
        print("hello world")

    def draw(self, pg, screen) -> None:
        for road in self.roads:
            road.draw(pg, screen)
