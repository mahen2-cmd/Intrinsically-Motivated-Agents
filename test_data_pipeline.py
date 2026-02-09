from data_pipeline import *
import numpy as np
import pytest
import torch
import torch.nn as nn

def test_linear_decay():
    assert linear_decay(start=5, end=0, number_of_steps=5, iteration_number=2) == 3
    assert linear_decay(start=10, end=0, number_of_steps=100, iteration_number=5) == 9.5
    assert linear_decay(start=10, end=0, number_of_steps=100, iteration_number=0) == 10


def test_epsilon_greedy():

    q_values = np.array([1.0, 2.0, 3.0])  # action 2 is the best

    # Case 1: epsilon = 0 → always pick greedy action
    for _ in range(100):
        action = epsilon_greedy(q_values, epsilon=0.0)
        assert action == 2

    # Case 2: epsilon = 1 → always pick random action
    counts = [0, 0, 0]
    for _ in range(1000):
        action = epsilon_greedy(q_values, epsilon=1.0)
        counts[action] += 1
    # All actions should have been picked at least once
    assert all(c > 0 for c in counts)

    # Case 3: intermediate epsilon = 0.5
    counts = [0, 0, 0]
    for _ in range(5000):
        action = epsilon_greedy(q_values, epsilon=0.5)
        counts[action] += 1
    # Greedy action should be chosen more often than others
    assert counts[2] > max(counts[0], counts[1])


def test_one_hot():

    num_actions = 4  # left, down, right, up

    # Case 1: check length
    vec = one_hot(2, num_actions)
    assert vec.shape == (num_actions,)

    # Case 2: check correct position set to 1
    assert np.array_equal(
        one_hot(0, num_actions), np.array([1, 0, 0, 0], dtype=np.float32)
    )
    assert np.array_equal(
        one_hot(1, num_actions), np.array([0, 1, 0, 0], dtype=np.float32)
    )
    assert np.array_equal(
        one_hot(2, num_actions), np.array([0, 0, 1, 0], dtype=np.float32)
    )
    assert np.array_equal(
        one_hot(3, num_actions), np.array([0, 0, 0, 1], dtype=np.float32)
    )

    # Case 3: invalid input should raise error
    with pytest.raises(IndexError):
        one_hot(4, num_actions)  # out of bounds


def test_transform_into_data():
    previous_positions = All_Positions(Position(3, 2), Position(3, 2), Position(4, 2))
    actions = All_Actions(RIGHT, RIGHT)
    next_positions = All_Positions(Position(4, 2), Position(4, 2), Position(5, 2))

    data_input = [3, 2, 3, 2, 4, 2, 0, 0, 1, 0, 0, 0, 1, 0]
    data_output = [4, 2, 4, 2, 5, 2]

    data_input = torch.tensor(data_input, dtype=torch.float32)
    data_output = torch.tensor(data_output, dtype=torch.float32)

    testing_input, testing_output = transform_into_data(previous_positions, actions, next_positions)

    assert torch.equal(testing_input, data_input)
    assert torch.equal(testing_output, data_output)


def test_sample_data():
    input_data, output_data = sample_data(50)

    assert input_data.shape[0] == output_data.shape[0]
    assert input_data.shape[0] == 50
    assert input_data.shape[1] == 14
    assert output_data.shape[1] == 6


def test_replay_buffer_push():
    input_data, output_data = sample_data(50)
    rb = Replay_Buffer(capacity=100000)

    combined_data = torch.cat([input_data, output_data], dim=1)

    assert combined_data.shape[0] == 50
    assert combined_data.shape[1] == 20

    rb.push(combined_data)

    assert len(rb.buffer) == 50

    # print(rb.sample(50))
    assert rb.sample(50).shape[0] == combined_data.shape[0]
    assert rb.sample(50).shape[1] == combined_data.shape[1]

    sample_10 = rb.sample(10)
    assert sample_10.shape[0] == 10
    assert sample_10.shape[1] == 20

    assert len(sample_10.shape) == 2

    assert type(sample_10) == torch.Tensor

    data_input = torch.Tensor([-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1])
    data_output = torch.Tensor([-1, -1, -1, -1, -1, -1])

    combined_data = torch.cat((data_input, data_output))

    data_input = torch.Tensor(
        [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 - 1, -1, -1, -1, -1, -1]]
    )

    for i in range(100000):
        rb.push(data_input)


    sampled_output = rb.sample(1000)

    tensors = [data_input.reshape(-1) for _ in range(1000)]
    stacked = torch.stack(tensors)

    assert torch.equal(stacked , sampled_output)


def test_trajectory():
    gridworld = GridWorld_Portal()
    starting_state = gridworld.all_entity_positions
    tr = Trajectory(starting_state)

    actions = All_Actions(3, 2)
    next_state = gridworld.step(actions)

    tr.add_state_action_pair(actions, next_state)

    len(tr.get_trajectory()) == 3
    tr.get_trajectory() == [starting_state, actions, next_state]


def test_random_policy():
    actions = Random_Policy().get_actions(3)
    assert type(actions) == All_Actions


def test_get_complete_episode():
    policy = Random_Policy()
    trajectory = get_complete_episode(policy)

    assert type(trajectory) == Trajectory

    trajectory = trajectory.get_trajectory()

    assert len(trajectory) == 2001
    assert type(trajectory[0]) == All_Positions
    assert type(trajectory[-2]) == All_Actions


def test_build_trajectory_data():
    policy = Random_Policy()
    trajectory = get_complete_episode(policy)

    # trajectory = trajectory.get_trajectory()

    input_trajectory_data, output_trajectory_data = build_trajectory_data(trajectory)

    assert type(input_trajectory_data) == torch.Tensor
    assert type(output_trajectory_data) == torch.Tensor

    assert input_trajectory_data.shape == torch.Size([1000, 14])
    assert output_trajectory_data.shape == torch.Size([1000, 6])
