import numpy as np
import random
import pickle
from car import Car
from roadManager import RoadManager


class AiController:
    ACTIONS = [-1, 0, 1]  # -1 = left, 1 = right
    distance_bins = np.linspace(-1, 1, 21)
    heading_bins = np.linspace(-1, 1, 21)
    bins = [distance_bins, heading_bins]

    def __init__(self, max_distance: float, car: Car, road_manager: RoadManager):
        self.max_distance = max_distance
        self.car = car
        self.road_manager = road_manager

        # learning parameters
        self.alpha = 0.1
        self.gamma = 0.95
        self.epsilon = 0.2 
        self.min_epsilon = 0.01
        self.epsilon_decay = 0.995

        self.Q = {}
        self.signed_distance = 0.0
        self.heading_alignment = 0.0
        self.state = np.array([self.signed_distance, self.heading_alignment])
        self.action = 0
        self.reward_val = 0

    def set_state(self, signed_distance, heading_alignment):
        """Set normalized values (-1 to 1)."""
        self.signed_distance = np.clip(signed_distance / self.max_distance, -1, 1)
        self.heading_alignment = np.clip(heading_alignment, -1, 1)
        self.state = np.array([self.signed_distance, self.heading_alignment])

    @staticmethod
    def discretize(state, bins) -> tuple:
        return tuple(np.digitize(s, b) for s, b in zip(state, bins))

    def select_action(self) -> int:
        """action selection."""
        discrete_state = self.discretize(self.state, self.bins)
        if random.random() < self.epsilon:
            action = random.choice(self.ACTIONS)
        else:
            q_values = [self.Q.get((discrete_state, a), 0.0) for a in self.ACTIONS]
            action = self.ACTIONS[int(np.argmax(q_values))]
        self.action = action
        return action

    def reward(self, distance, heading_alignment, off_road) -> float:
        """Reward based on how centered"""
        reward = 1.0
        reward -= abs(distance) * 0.2
        reward += heading_alignment * 0.5
        if heading_alignment < 0:
            reward -= 1.0
        if off_road:
            reward = -100.0
        return reward

    def update_q(self, reward, next_state):
        state_key = self.discretize(self.state, self.bins)
        next_state_key = self.discretize(next_state, self.bins)
        old_q = self.Q.get((state_key, self.action), 0.0)
        next_max = max([self.Q.get((next_state_key, a), 0.0) for a in self.ACTIONS])
        new_q = old_q + self.alpha * (reward + self.gamma * next_max - old_q)
        self.Q[(state_key, self.action)] = new_q
        self.state = next_state

    def update_car(self, dt):
        signed_distance, road_dir = self.road_manager.check_car_on_road((self.car.x, self.car.y))
        car_dir = np.array([np.cos(self.car.heading), np.sin(self.car.heading)])
        heading_alignment = np.dot(car_dir, road_dir)

        self.set_state(signed_distance, heading_alignment)
        action = self.select_action()

        accel = self.car.max_accel  # always move forward
        steer = action * self.car.max_steer_rate
        self.car.update(dt, accel, steer)

        next_signed_distance, road_dir = self.road_manager.check_car_on_road((self.car.x, self.car.y))
        car_dir = np.array([np.cos(self.car.heading), np.sin(self.car.heading)])
        next_heading_alignment = np.dot(car_dir, road_dir)
        next_state = np.array([
            np.clip(next_signed_distance / self.max_distance, -1, 1),
            np.clip(next_heading_alignment, -1, 1)
        ])

        off_road = abs(next_signed_distance) > self.max_distance
        reward = self.reward(next_signed_distance, next_heading_alignment, off_road)
        self.reward_val = reward

        self.update_q(reward, next_state)
        return off_road 

    def train(self, num_episodes: int, dt: float):
        print("Starting training...")
        for episode in range(num_episodes):
            self.car.reset_to_start()
            total_reward = 0
            done = False
            steps = 0

            while not done:
                off_road = self.update_car(dt)
                total_reward += self.reward_val
                steps += 1

                if off_road or steps > 1000:
                    done = True

            self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

            print(
                f"Episode {episode+1}/{num_episodes} | "
                f"Total reward: {total_reward:.2f} | "
                f"Epsilon: {self.epsilon:.3f}"
            )

        print("Training complete!")

    def save_q_table(self, path="q_table.pkl"):
        with open(path, "wb") as f:
            pickle.dump(self.Q, f)
        print(f"Q-table saved to {path}")

    def load_q_table(self, path="q_table.pkl"):
        with open(path, "rb") as f:
            self.Q = pickle.load(f)
        print(f"Q-table loaded from {path}")