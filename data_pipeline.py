import numpy as np
from environment import *
import torch
from collections import deque

def linear_decay(start, end, number_of_steps, iteration_number):

    iteration_number = min(max(iteration_number, 0), number_of_steps)

    decay_rate = (start - end) / number_of_steps
    return start - decay_rate * iteration_number


def epsilon_greedy(q_values, epsilon):
    if np.random.rand() < epsilon:
        return np.random.randint(len(q_values))
    else:
        return int(np.argmax(q_values))


def one_hot(action, num_actions):
    vec = np.zeros(num_actions, dtype=np.float32)
    vec[action] = 1.0
    return vec


def transform_into_data(
    previous_positions: All_Positions,
    all_actions: All_Actions,
    next_positions: All_Positions,
) -> tuple[torch.Tensor, torch.Tensor]:

    # Unpack previous and next positions
    prev_agent1, prev_agent2, prev_box = previous_positions.get_positions()
    next_agent1, next_agent2, next_box = next_positions.get_positions()
    action1, action2 = all_actions.get_actions()

    # Build input: previous positions + one-hot actions
    input_data = (
        list(prev_agent1.get_position())
        + list(prev_agent2.get_position())
        + list(prev_box.get_position())
        + one_hot(action1, 4).astype(int).tolist()
        + one_hot(action2, 4).astype(int).tolist()
    )

    # Build output: next positions
    output_data = (
        list(next_agent1.get_position())
        + list(next_agent2.get_position())
        + list(next_box.get_position())
    )

    # Convert to tensors in float32
    input_tensor = torch.tensor(input_data, dtype=torch.float32)
    output_tensor = torch.tensor(output_data, dtype=torch.float32)

    return input_tensor, output_tensor


def sample_data(number_of_samples: int) -> tuple[torch.Tensor, torch.Tensor]:

    env = GridWorld_Portal()
    current_observation = env.all_entity_positions

    input_tensors = []
    output_tensors = []

    for _ in range(number_of_samples):
        # Random actions for both agents
        action1, action2 = random.randint(0, 3), random.randint(0, 3)
        actions = All_Actions(action1, action2)

        # Take a step in the environment
        next_observation = env.step(actions)

        # Transform observations and actions into input/output tensors
        input_tensor, output_tensor = transform_into_data(
            current_observation, actions, next_observation
        )

        input_tensors.append(input_tensor)
        output_tensors.append(output_tensor)

        # Update observation for next step
        current_observation = next_observation

    # Stack lists into batch tensors
    input_batch = torch.stack(input_tensors)
    output_batch = torch.stack(output_tensors)

    return input_batch, output_batch


class Replay_Buffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = deque(maxlen=capacity)

    def push(self, tensors):
        for data in tensors:
            self.buffer.append(data)

    def sample(self, batch_size: int) -> torch.Tensor:
        batch = random.sample(self.buffer, batch_size)
        return torch.stack(batch)


class Trajectory:
    def __init__(self, starting_state):
        self.trajectory = [starting_state]

    def add_state_action_pair(self, actions, next_state):
        self.trajectory.append(actions)
        self.trajectory.append(next_state)

    def get_trajectory(self):
        return self.trajectory


class Policy:
    def __init__(self):
        pass

class Random_Policy(Policy):
    def get_actions(self, state):
        action1 = random.randint(0, 3)
        action2 = random.randint(0, 3)

        return All_Actions(action1, action2)

def get_complete_episode(policy: Policy) -> Trajectory:

    env = GridWorld_Portal()
    state = env.all_entity_positions
    trajectory = Trajectory(state)

    for _ in range(1000):
        actions = policy.get_actions(state)

        next_state = env.step(actions)

        trajectory.add_state_action_pair(actions, next_state)
        state = next_state

    return trajectory


def build_trajectory_data(trajectory: Trajectory) -> tuple[torch.Tensor, torch.Tensor]:
    trajectory = trajectory.get_trajectory()

    complete_input_data_tensor = []
    complete_output_data_tensor = []
    for i in range(1000):
        previous_state = trajectory[2*i]
        actions = trajectory[2*i + 1]
        next_state = trajectory[2*i + 2]

        input_data_tensor, output_data_tensor = transform_into_data(previous_state, actions, next_state)
        complete_input_data_tensor.append(input_data_tensor)
        complete_output_data_tensor.append(output_data_tensor)

    return torch.stack(complete_input_data_tensor), torch.stack(complete_output_data_tensor)

