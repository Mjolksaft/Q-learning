import numpy as np
import pandas as pd
import random
import pickle
from .car import Car
from .roadManager import RoadManager


class AiController:
    ACTIONS = [-1, 0, 1]  # -1 = left, 1 = right
    distance_bins = np.linspace(-1, 1, 21)
    bins = [distance_bins]  # Only distance now

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
        self.state = np.array([self.signed_distance])
        self.action = 0
        self.reward_val = 0

    def set_state(self, signed_distance):
        """Set normalized distance (-1 to 1)."""
        self.signed_distance = np.clip(signed_distance / self.max_distance, -1, 1)
        self.state = np.array([self.signed_distance])

    @staticmethod
    def discretize(state, bins) -> tuple:
        return tuple(np.digitize(s, b) for s, b in zip(state, bins))

    def select_action(self) -> int:
        """Epsilon-greedy action selection."""
        discrete_state = self.discretize(self.state, self.bins)
        if random.random() < self.epsilon:
            action = random.choice(self.ACTIONS)
        else:
            q_values = [self.Q.get((discrete_state, a), 0.0) for a in self.ACTIONS]
            action = self.ACTIONS[int(np.argmax(q_values))]
        self.action = action
        return action

    def reward(self, distance, off_road, finished) -> float:
        """Reward shaping based on distance and heading."""
        reward = 1.0 - abs(distance) * 0.3 * 0.5

        if off_road:
            reward -= 10.0
        if finished:
            reward += 100.0

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
        signed_distance, road_dir = self.road_manager.check_car_on_road(
            (self.car.x, self.car.y)
        )

        self.set_state(signed_distance)
        action = self.select_action()

        accel = self.car.max_accel  # always move forward
        steer = action * self.car.max_steer_rate
        self.car.update(dt, accel, steer)

        next_signed_distance, road_dir = self.road_manager.check_car_on_road(
            (self.car.x, self.car.y)
        )
        next_state = np.array(
            [np.clip(next_signed_distance / self.max_distance, -1, 1)]
        )

        off_road = abs(next_signed_distance) > self.max_distance
        finished = self.road_manager.check_goal((self.car.x, self.car.y), False)
        reward = self.reward(next_signed_distance, off_road, finished)
        self.reward_val = reward

        self.update_q(reward, next_state)
        return off_road, finished

    def train(self, num_episodes: int, dt: float):
        print("Starting training...")
        for episode in range(num_episodes):
            self.car.reset_to_start()
            total_reward = 0
            done = False
            steps = 0

            while not done:
                off_road, finished = self.update_car(dt)
                total_reward += self.reward_val
                steps += 1

                if off_road or finished or steps > 1000:
                    done = True

            self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

            car = np.array([self.car.x, self.car.x])
            end = np.array([self.road_manager.x_end, self.road_manager.y_end])
            distance = np.linalg.norm(car - end)

            print(
                f"Episode {episode + 1}/{num_episodes} | "
                f"Total reward: {total_reward:.2f} | "
                f"Epsilon: {self.epsilon:.3f} | "
                f"finished: {finished} | "
                f"Distance: {distance:.3f}"
            )

        print("Training complete!")

    def save_q_table(self, path="src\\q_learning\\q-table\\q_table.pkl"):
        with open(path, "wb") as f:
            pickle.dump(self.Q, f)
        print(f"Q-table saved to {path}")

    def load_q_table(self, path="src\\q_learning\\q-table\\q_table.pkl"):
        with open(path, "rb") as f:
            self.Q = pickle.load(f)
        print(f"Q-table loaded from {path}")

    def save_q_table_excel(self, path="src\\q_learning\\q-table\\q_table.xlsx"):
        data = []
        for (state, action), value in self.Q.items():
            distance_bin = state[0]
            data.append([distance_bin, action, value])
        df = pd.DataFrame(data, columns=["distance_bin", "action", "q_value"])
        df.to_excel(path, index=False)
        print(f"Q-table saved to {path} (Excel)")
