import pytest
from movement import *
import numpy as np
from collections import Counter

LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3


def test_position():
    a = Position(3, 4)

    assert hash(a) == hash((3, 4))
    assert hash(a) != hash((4, 5))


def test_all_positions():
    a = Position(3, 4)
    b = Position(3, 4)
    c = Position(4, 5)

    d = All_Positions(a, b, c)

    assert hash(d) == hash((3, 4, 3, 4, 4, 5))

def test_frozen_lake_checker():
    a = Position(13, 0)
    b = Position(4, 1)
    c = Position(10, 2)
    d = Position(3, 3)

    assert Frozen_Lake_Checker().check_frozen_lake(a) == True
    assert Frozen_Lake_Checker().check_frozen_lake(b) == False
    assert Frozen_Lake_Checker().check_frozen_lake(c) == True
    assert Frozen_Lake_Checker().check_frozen_lake(d) == False

def test_move():
    x = 3
    y = 4
    pos = Position(x, y)

    assert Move().get_new_position(pos, DOWN) == Position(3, 5)
    assert Move().get_new_position(pos, LEFT) == Position(2, 4)


def test_check_movement():
    x = 1
    y = 2
    pos = Position(x, y)


    assert Movement_Checker().check_movement(pos, DOWN) == True
    assert Movement_Checker().check_movement(pos, LEFT) == True
    assert Movement_Checker().check_movement(pos, RIGHT) == False


def test_check_movement2():

    pos = Position(2, 0)


    assert Movement_Checker().check_movement(pos, DOWN) == False
    assert Movement_Checker().check_movement(pos, UP) == False
    assert Movement_Checker().check_movement(pos, LEFT) == True


def test_check_movement3():
    pos = Position(4, 4)
    assert Movement_Checker().check_movement(pos, RIGHT) == False


def test_check_movement4():
    pos = Position(13, 3)
    assert Movement_Checker().check_movement(pos, UP) == False
    assert Movement_Checker().check_movement(pos, LEFT) == True
    assert Movement_Checker().check_movement(pos, DOWN) == False
    assert Movement_Checker().check_movement(pos, RIGHT) == False


def test_check_movement5():
    pos = Position(17, 3)
    assert Movement_Checker().check_movement(pos, UP) == False
    assert Movement_Checker().check_movement(pos, LEFT) == True
    assert Movement_Checker().check_movement(pos, DOWN) == True
    assert Movement_Checker().check_movement(pos, RIGHT) == True


def test_check_box_movement():
    agent_position = Position(5, 2)
    agent_position2 = Position(6, 1)
    agent_position3 = Position(6, 3)
    agent_position4 = Position(4, 4)
    box_position = Position(6, 2)

    assert Box_Movement_Checker().check_box_movement(agent_position, box_position, RIGHT) == False
    assert Box_Movement_Checker().check_box_movement(agent_position2, box_position, RIGHT) == False
    assert Box_Movement_Checker().check_box_movement(agent_position2, box_position, UP) == False
    assert Box_Movement_Checker().check_box_movement(agent_position2, box_position, DOWN) == True
    assert Box_Movement_Checker().check_box_movement(agent_position3, box_position, UP) == True
    assert Box_Movement_Checker().check_box_movement(agent_position4, box_position, LEFT) == False


def test_check_box_movement2():
    agent_position = Position(4, 4)
    box_position = Position(4, 5)

    agent2_position = Position(3, 5)

    assert Box_Movement_Checker().check_box_movement(agent_position, box_position, DOWN) == False
    assert Box_Movement_Checker().check_box_movement(agent2_position, box_position, RIGHT) == True


def test_move_box():
    box_position = Position(7, 3)

    assert Move_Box().move_box(box_position, UP) == Position(7, 3)
    assert Move_Box().move_box(box_position, DOWN) == Position(7, 4)
    assert Move_Box().move_box(box_position, RIGHT) == Position(8, 3)
    assert Move_Box().move_box(box_position, LEFT) == Position(6, 3)

    box_position2 = Position(3, 3)

    assert Move_Box().move_box(box_position2, LEFT) == Position(3, 3)
    assert Move_Box().move_box(box_position2, DOWN) == Position(3, 4)
    assert Move_Box().move_box(box_position2, RIGHT) == Position(4, 3)
    assert Move_Box().move_box(box_position2, UP) == Position(3, 2)


def test_portal():
    box_position = Position(8, 0)
    box_position2 = Position(3, 1)
    box_position3 = Position(3, 2)

    agent_position = Position(8, 4)
    agent_position2 = Position(17, 3)
    agent_position3 = Position(8, 1)


    assert Move_Through_Portal().move_through_portal(agent_position, box_position, RIGHT) == Position(17, 3)
    assert Move_Through_Portal().move_through_portal(agent_position, box_position2, RIGHT) == Position(8, 4)
    assert Move_Through_Portal().move_through_portal(agent_position2, box_position, UP) == Position(8, 4)

    assert Move_Through_Portal().move_through_portal(agent_position2, box_position3, LEFT) == Position(17, 3)
    assert Move_Through_Portal().move_through_portal(agent_position, box_position3, RIGHT) == Position(8, 4)
    assert Move_Through_Portal().move_through_portal(agent_position3, box_position, DOWN) == agent_position3

def test_agent_movement_checker():
    box_position = Position(3, 2)
    box_position3 = Position(8, 0)

    agent_position2 = Position(4, 2)

    agent_position4 = Position(3, 1)

    assert Agent_Movement_Checker().check_agent_movement(agent_position4, box_position3, LEFT) == False
    assert Agent_Movement_Checker().check_agent_movement(agent_position2, box_position, LEFT) == False
    assert Agent_Movement_Checker().check_agent_movement(Position(3, 2), Position(4, 2), RIGHT) == True
    assert Agent_Movement_Checker().check_agent_movement(Position(3, 5), Position(3, 4), DOWN) == False
    assert Agent_Movement_Checker().check_agent_movement(Position(3, 5), Position(3, 4), UP) == True


def test_move_agent():

    box_position = Position(3, 2)
    box_position2 = Position(3, 1)
    box_position3 = Position(8, 0)

    agent_position = Position(8, 4)
    agent_position2 = Position(4, 1)
    agent_position3 = Position(8, 1)

    agent_position4 = Position(3, 1)

    assert Move_Agent().move_agent(agent_position, box_position3, RIGHT) == Position(17, 3)
    assert Move_Agent().move_agent(agent_position4, box_position, DOWN) == Position(3, 2)
    assert Move_Agent().move_agent(agent_position2, box_position2, LEFT) == agent_position2
    assert Move_Agent().move_agent(agent_position3, box_position3, UP) == agent_position3
    assert Move_Agent().move_agent(agent_position3, box_position3, DOWN) == Position(8, 2)


def test_move_everything():

    box_position = Position(3, 2)
    box_position2 = Position(3, 1)
    box_position3 = Position(8, 0)
    box_position4 = Position(4, 2)

    box_position5 = Position(5, 3)
    box_position6 = Position(6, 3)

    agent_position = Position(8, 4)
    agent_position2 = Position(4, 1)
    agent_position3 = Position(1, 5)

    agent_position5 = Position(1, 4)

    agent_position6 = Position(17, 3)

    agent_position7 = Position(4, 3)
    agent2_position = Position(-1, -1)


    agent_position8 = Position(6, 2)
    box_position8 = Position(6, 3)
    box_position9 = Position(6, 4)


    agent_position10 = Position(5, 5)
    agent_position11 = Position(5, 5)

    assert Move_Everything().move_Everything(agent_position5, box_position4, DOWN) == All_Positions(
        agent_position3, agent2_position, box_position4)
    assert Move_Everything().move_Everything(agent_position, box_position3, RIGHT) == All_Positions(
        agent_position6, agent2_position, box_position3)

    assert Move_Everything().move_Everything(agent_position2, box_position2, LEFT) == All_Positions(
        agent_position2, agent2_position, box_position2)

    assert Move_Everything().move_Everything(agent_position3, box_position, UP) == All_Positions(
        agent_position5, agent2_position, box_position)


    assert Move_Everything().move_Everything(agent_position7, box_position5, RIGHT) == All_Positions(
        box_position5, agent2_position, box_position6)

    assert Move_Everything().move_Everything(agent_position8, box_position8, DOWN) == All_Positions(
        box_position8, agent2_position, box_position9)


    assert Move_Everything().move_Everything(agent_position10, box_position9, DOWN) == All_Positions(
        agent_position11, agent2_position, box_position9)
    assert Move_Everything().move_Everything(agent_position10, box_position9, UP) == All_Positions(
        agent_position11, agent2_position, box_position9)


def test_check_box_movement_two_agents():
    box_position = Position(4, 2)
    agent1_position = Position(5, 2)

    agent2_position = Position(6, 3)

    box_position2 = Position(4, 5)
    agent1_position2 = Position(4, 4)

    box_position3 = Position(8, 1)
    agent1_position3 = Position(8, 2)

    positions = All_Positions(agent1_position, agent1_position, box_position)
    positions2 = All_Positions(agent1_position, Position(-1, -1), box_position)
    positions3 = All_Positions(agent1_position, agent2_position, box_position)
    positions4 = All_Positions(agent1_position2, agent1_position2, box_position2)

    positions5 = All_Positions(agent1_position3, agent1_position3, box_position3)
    # agent2_position = Position(5, 2)

    actions1 = All_Actions(RIGHT, RIGHT)
    actions2 = All_Actions(LEFT, LEFT)
    actions3 = All_Actions(UP, UP)
    actions4 = All_Actions(DOWN, DOWN)
    actions5 = All_Actions(UP, DOWN)
    actions6 = All_Actions(UP, LEFT)
    actions7 = All_Actions(UP, RIGHT)
    actions8 = All_Actions(LEFT, RIGHT)

    assert Box_Movement_Checker().check_box_movement_two_agents(positions, actions1) == False
    assert Box_Movement_Checker().check_box_movement_two_agents(positions, actions2) == True
    assert Box_Movement_Checker().check_box_movement_two_agents(positions2, actions2) == False
    assert Box_Movement_Checker().check_box_movement_two_agents(positions3, actions2) == False
    assert Box_Movement_Checker().check_box_movement_two_agents(positions4, actions4) == False

    assert Box_Movement_Checker().check_box_movement_two_agents(positions5, actions3) == True
    assert Box_Movement_Checker().check_box_movement_two_agents(positions5, actions4) == False
    assert Box_Movement_Checker().check_box_movement_two_agents(positions5, actions2) == False
    assert Box_Movement_Checker().check_box_movement_two_agents(positions5, actions1) == False

    assert (
        Box_Movement_Checker().check_box_movement_two_agents(positions5, actions5)
        == False
    )

    assert (
        Box_Movement_Checker().check_box_movement_two_agents(positions, actions6)
        == False
    )
    assert (
        Box_Movement_Checker().check_box_movement_two_agents(positions, actions7)
        == False
    )


def test_agent_movement_checker_two_agents():
    agent1_position = Position(5, 2)
    agent2_position = Position(6, 3)
    box_position = Position(4, 2)

    agent1_position2 = Position(6, 5)
    agent2_position2 = Position(0, 2)

    agent1_position3 = Position(8, 4)
    box_position2 = Position(8, 0)

    agent2_position3 = Position(4, 1)
    agent2_position4 = Position(17, 3)

    box_position3 = Position(7, 3)

    positions = All_Positions(agent1_position, agent2_position, box_position)
    positions2 = All_Positions(agent1_position, agent1_position, box_position)
    positions3 = All_Positions(agent1_position2, agent2_position2, box_position)
    positions4 = All_Positions(agent1_position3, agent2_position, box_position2)

    positions5 = All_Positions(agent1_position, agent2_position3, box_position)

    positions6 = All_Positions(agent1_position, agent2_position4, box_position2)

    positions7 = All_Positions(agent2_position, agent2_position, box_position3)

    actions1 = All_Actions(LEFT, UP)
    actions2 = All_Actions(LEFT, LEFT)
    actions3 = All_Actions(RIGHT, UP)
    actions4 = All_Actions(RIGHT, RIGHT)
    actions5 = All_Actions(DOWN, DOWN)
    actions6 = All_Actions(DOWN, UP)
    actions7 = All_Actions(LEFT, DOWN)
    actions8 = All_Actions(LEFT, RIGHT)


    assert Agent_Movement_Checker().check_agent_movement_two_agents(positions, actions1) == Movement_Check(False, True)
    assert Agent_Movement_Checker().check_agent_movement_two_agents(positions2, actions2) == Movement_Check(True, True)

    assert Agent_Movement_Checker().check_agent_movement_two_agents(positions3, actions5) == Movement_Check(False, True)


    assert Agent_Movement_Checker().check_agent_movement_two_agents(positions3, actions6) == Movement_Check(False, True)




    assert Agent_Movement_Checker().check_agent_movement_two_agents(positions3, actions3) == Movement_Check(True, True)

    assert Agent_Movement_Checker().check_agent_movement_two_agents(positions4, actions3) == Movement_Check(True, True)

    assert Agent_Movement_Checker().check_agent_movement_two_agents(positions6, actions6) == Movement_Check(True, True)



    assert Agent_Movement_Checker().check_agent_movement_two_agents(positions5, actions7) == Movement_Check(False, False)
    assert Agent_Movement_Checker().check_agent_movement_two_agents(positions7, actions4) == Movement_Check(True, True)
    assert Agent_Movement_Checker().check_agent_movement_two_agents(positions7, actions8) == Movement_Check(True, False)


def test_agent_portal_movement():
    box_position = Position(8, 0)
    box_position2 = Position(3, 1)

    agent_position = Position(8, 4)
    agent_position2 = Position(17, 3)
    agent_position3 = Position(8, 1)
    agent_position4 = Position(7, 0)

    assert Agent_Movement_Checker()._can_move_portal(agent_position, box_position, RIGHT) == True
    assert Agent_Movement_Checker()._can_move_portal(agent_position2, box_position, UP) == True
    assert Agent_Movement_Checker()._can_move_portal(agent_position2, box_position, LEFT) == False

    assert Agent_Movement_Checker()._can_move_portal(agent_position3, box_position, DOWN) == False
    assert Agent_Movement_Checker()._can_move_portal(agent_position4, box_position, RIGHT) == False

    assert Agent_Movement_Checker()._can_move_portal(agent_position, box_position2, RIGHT) == False
    assert Agent_Movement_Checker()._can_move_portal(agent_position2, box_position2, LEFT) == False

def test_move_everything_two_agents():

    assert Move_Two_Agents().move_two_agents(All_Positions(Position(5, 2), Position(6, 3), Position(4, 2))  , All_Actions(LEFT, UP)  ) == All_Positions(Position(5, 2), Position(6, 2), Position(4, 2))
    assert Move_Two_Agents().move_two_agents(All_Positions(Position(5, 2), Position(6, 3), Position(4, 2))  , All_Actions(UP, UP)  )   == All_Positions(Position(5, 1), Position(6, 2), Position(4, 2))
    assert Move_Two_Agents().move_two_agents(All_Positions(Position(5, 2), Position(5, 2), Position(4, 2))  , All_Actions(LEFT, LEFT)) == All_Positions(Position(4, 2), Position(4, 2), Position(3, 2))
    assert Move_Two_Agents().move_two_agents(All_Positions(Position(4, 2), Position(4, 2), Position(3, 2)) , All_Actions(LEFT, LEFT) ) == All_Positions(Position(4, 2), Position(4, 2), Position(3, 2))
    assert Move_Two_Agents().move_two_agents(All_Positions(Position(4, 2), Position(4, 2), Position(3, 2)) , All_Actions(LEFT, DOWN) ) == All_Positions(Position(4, 2), Position(4, 3), Position(3, 2))
    assert Move_Two_Agents().move_two_agents(All_Positions(Position(8, 4), Position(8, 4), Position(8, 3)) , All_Actions(UP, UP) )     == All_Positions(Position(8, 3), Position(8, 3), Position(8, 2))


def helper_test_probabilities(all_positions, expected, total, tolerance):
    counts = Counter(all_positions)

    for _, count in counts.items():
        pct = count / total
        assert abs(pct - expected) <= tolerance

def test_move_everything_two_agents_frozen_lake():
    all_positions = [
        Move_Two_Agents().move_two_agents(
            All_Positions(Position(8, 4), Position(17, 3), Position(8, 0)),
            All_Actions(RIGHT, DOWN),
        )
        for _ in range(10000)
    ]
    possible_positions = set(all_positions)


    output1 = All_Positions(Position(17, 3), Position(17, 4), Position(8, 0))
    output2 = All_Positions(Position(17, 3), Position(16, 3), Position(8, 0))
    output3 = All_Positions(Position(17, 3), Position(18, 3), Position(8, 0))

    assert output1 in possible_positions
    assert output2 in possible_positions
    assert output3 in possible_positions

    helper_test_probabilities(all_positions, expected = 1/3, total = 10000, tolerance = 0.05)


    all_positions = [
        Move_Two_Agents().move_two_agents(
            All_Positions(Position(12, 2), Position(10, 1), Position(8, 0)),
            All_Actions(RIGHT, DOWN),
        )
        for _ in range(10000)
    ]

    possible_positions = set(all_positions)

    output1 = All_Positions(Position(12, 2), Position(10, 2), Position(8, 0))
    output2 = All_Positions(Position(12, 2), Position(10, 1), Position(8, 0))

    output3 = All_Positions(Position(12, 3), Position(10, 2), Position(8, 0))
    output4 = All_Positions(Position(12, 3), Position(10, 1), Position(8, 0))

    output5 = All_Positions(Position(12, 1), Position(10, 2), Position(8, 0))
    output6 = All_Positions(Position(12, 1), Position(10, 1), Position(8, 0))

    assert output1 in possible_positions
    assert output2 in possible_positions
    assert output3 in possible_positions
    assert output4 in possible_positions
    assert output5 in possible_positions
    assert output6 in possible_positions

    helper_test_probabilities(
        all_positions, expected=1 / 6, total=10000, tolerance=0.1
    )


def test_frozen_lake_actions():
    move = Move_Agent()
    position = Position(12, 1)

    action = LEFT

    outputs = [move.move_agent_frozen_lake(position, action).get_position() for _ in range(10000)]

    expected = 1/3
    total = 10000
    tolerance = 0.05
    counts = Counter(outputs)

    unique_outputs = set(outputs)

    assert unique_outputs == set([(12, 1), (12, 0), (12, 2)])

    for _, count in counts.items():
        pct = count/total
        assert abs(pct - expected) <= tolerance

    position = Position(13, 3)
    action = RIGHT
    outputs = [move.move_agent_frozen_lake(position, action).get_position() for _ in range(10000)]
    unique_outputs = set(outputs)
    assert unique_outputs == set([(13, 3)])

    position = Position(11, 3)
    action = LEFT
    outputs = [
        move.move_agent_frozen_lake(position, action).get_position()
        for _ in range(10000)
    ]
    unique_outputs = set(outputs)
    assert unique_outputs == set([(11, 3), (11, 2)])

    for item, count in counts.items():
        if item == (11, 3):
            pct = count / total
            expected = 2/3
            assert abs(pct - expected) <= tolerance
        if item == (11, 2):
            pct = count / total
            expected = 1 / 3
            assert abs(pct - expected) <= tolerance


def test_check_garden_environment():
    pos1 = Position(27, 4)
    pos2 = Position(5, 0)
    pos3 = Position(30, 1)
    pos4 = Position(13, 3)
    pos5 = Position(16, 2)
    pos6 = Position(15, 7)

    tester = Garden_Environment_Checker()

    assert tester.check_garden_environment(pos1) == True
    assert tester.check_garden_environment(pos2) == False
    assert tester.check_garden_environment(pos3) == False
    assert tester.check_garden_environment(pos4) == False
    assert tester.check_garden_environment(pos5) == True
    assert tester.check_garden_environment(pos6) == False


def test_garden_blockers():
    pass

def test_garden_movement():
    pos1 = Position(14, 5)
    pos2 = Position(15, 5)


    all_positions = [
        Move_Two_Agents().move_two_agents(
            All_Positions(pos1, Position(17, 3), Position(8, 0)),
            All_Actions(RIGHT, LEFT),
        )
        for _ in range(10000)
    ]

    possible_positions = set(all_positions)

    output1 = All_Positions(pos1, Position(17, 4), Position(8, 0))
    output2 = All_Positions(pos1, Position(16, 3), Position(8, 0))
    output3 = All_Positions(pos1, Position(8, 4), Position(8, 0))

    output4 = All_Positions(pos2, Position(17, 4), Position(8, 0))
    output5 = All_Positions(pos2, Position(16, 3), Position(8, 0))
    output6 = All_Positions(pos2, Position(8, 4), Position(8, 0))

    assert output1 in possible_positions
    assert output2 in possible_positions
    assert output3 in possible_positions
    assert output4 in possible_positions
    assert output5 in possible_positions
    assert output6 in possible_positions
