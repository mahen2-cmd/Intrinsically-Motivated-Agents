from environment import *
from movement import *

def test_step():
    env = GridWorld_Portal()
    env.number_of_steps = 1000


    actions = All_Actions(0, 0)

    observation = env.step(actions)

    all_positions = All_Positions(Position(0, 2), Position(3, 5), Position(4, 2))

    assert observation == all_positions


def test_step2():
    env = GridWorld_Portal()
    actions = All_Actions(RIGHT, UP)

    observation = env.step(actions)

    all_positions = All_Positions(Position(1, 2), Position(3, 4), Position(4, 2))

    assert observation == all_positions
    assert env.number_of_steps == 1

def test_step3():
    env = GridWorld_Portal()
    actions = All_Actions(RIGHT, RIGHT)

    env.set_position( All_Positions(Position(3, 2), Position(3, 2), Position(4, 2)) )


    observation = env.step(actions)

    all_positions = All_Positions(Position(4, 2), Position(4, 2), Position(5, 2))

    assert observation == all_positions
