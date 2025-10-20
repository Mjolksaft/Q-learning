import numpy as np


class Ai:
    ACTIONS = [-1,0,1] # left, forward, right

    distance_bins = np.linspace(-1, 1, 21)
    bins = [distance_bins]
    # heading_bins = np.linspace(-1, 1, 21)

    def __init__(self, max_distance:float): 
        self.max_distance = max_distance
        self.signed_distance = 0.0
        self.state = np.array([ ## normalized values 
            self.signed_distance
        ], dtype=float)


    def set_signed_distance(self, new_distance) -> None:
        """sets the signed distance as normalized value"""
        if new_distance == 0.0:
            self.signed_distance = 0.0
            return
        self.signed_distance = new_distance / self.max_distance
    
    def reward(self, distance, heading_alignment, finished) -> float:
        """ calculates the reward for the ai"""
        if finished:
            return -100
    
        reward = 1.0
        reward -=(distance) * 0.1
        # reward += heading_alignment * 0.5 ## for checking if ai is going the right direction 
        return reward
    
    def discretize(state, bins):
        discrete = tuple(np.digitize(s, b) for s, b in zip(state, bins))
        return discrete

    def __repr__(self):
        return f"Distance = {self.signed_distance}"
