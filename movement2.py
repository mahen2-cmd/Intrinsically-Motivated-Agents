import random

LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3

EMPTY = 0
BLOCK = 2
HEAVY_BOX = 20
AGENTS = [1, 5]

lake_coordinates = [
    (2, 1),
    (2, 2),
    (2, 3),
    (5, 4),
    (7, 0),
    (7, 1),
    (7, 2),
    (9, 0),
    (9, 1),
    (9, 2),
    (9, 3),
    (9, 4),
    (9, 5),
    (11, 1),
    (13, 1),
    (13, 2),
    (10, 3),
    (10, 4),
    (11, 4),
    (12, 4),
    (13, 4),
    (10, 5),
    (11, 5),
    (12, 5),
    (13, 5),
]

box_coordinate = (4, 2)

direction_deltas = {
    LEFT: (-1, 0),
    DOWN: (0, 1),
    RIGHT: (1, 0),
    UP: (0, -1),
}
MAX_X, MAX_Y = 13, 5


class Position:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __repr__(self):
        return f"Position at {self._x}, {self._y}"

    def __eq__(self, pos):
        new_x, new_y = pos.get_position()
        return self._x == new_x and self._y == new_y

    def get_position(self) -> tuple:
        return (self._x, self._y)

    def __hash__(self):
        return hash((self._x, self._y))


class All_Positions:
    def __init__(
        self,
        position_agent1: Position,
        position_agent2: Position,
        position_box: Position,
    ):
        self._position_agent1 = position_agent1
        self._position_agent2 = position_agent2
        self._position_box = position_box

    def __repr__(self):
        return f"Agent 1: {self._position_agent1}, Agent 2: {self._position_agent2}, Box: {self._position_box}"

    def __eq__(self, all_positions):
        agent1_pos, agent2_pos, box_pos = all_positions.get_positions()
        return (
            self._position_agent1 == agent1_pos
            and self._position_agent2 == agent2_pos
            and self._position_box == box_pos
        )

    def __hash__(self):
        x1, y1 = self._position_agent1.get_position()
        x2, y2 = self._position_agent2.get_position()
        b1, b2 = self._position_box.get_position()

        return hash((x1, y1, x2, y2, b1, b2))

    def get_positions(self) -> tuple:
        return (self._position_agent1, self._position_agent2, self._position_box)


class All_Actions:
    def __init__(self, action_agent1: int, action_agent2: int):
        self._action_agent1 = action_agent1
        self._action_agent2 = action_agent2

    def __repr__(self):
        return f"Action Agent 1: {self._action_agent1}, Action Agent 2: {self._action_agent2}"

    def __eq__(self, all_actions):
        action1, action2 = all_actions.get_actions()
        return self._action_agent1 == action1 and self._action_agent2 == action2

    def get_actions(self) -> tuple:
        return (self._action_agent1, self._action_agent2)


class Movement_Check:
    def __init__(self, check1: bool, check2: bool):
        self._check1 = check1
        self._check2 = check2

    def __repr__(self):
        return f"Check 1: {self._check1}, Check 2: {self._check2}"

    def __eq__(self, movement_check):
        check1, check2 = movement_check.get_checks()
        return self._check1 == check1 and self._check2 == check2

    def get_checks(self) -> tuple:
        return (self._check1, self._check2)


class Move:
    def get_new_position(self, pos: Position, action: int) -> Position:

        x, y = pos.get_position()
        dx, dy = direction_deltas[action]

        return Position(x + dx, y + dy)


class Movement_Checker:
    def check_movement(self, position: Position, action: int) -> bool:

        new_position = Move().get_new_position(position, action)
        x, y = new_position.get_position()

        in_bounds = 0 <= x <= MAX_X and 0 <= y <= MAX_Y
        not_in_lake = (x, y) not in lake_coordinates

        return in_bounds and not_in_lake


class Frozen_Lake_Checker:
    def check_frozen_lake(self, position: Position) -> bool:
        x, _ = position.get_position()
        return 10 <= x <= MAX_X


class Agent_Movement_Checker:

    def check_agent_portal_movement(
        self, agent_position: Position, box_position: Position, action: int
    ) -> bool:
        box_portal_opening_position = Position(8, 0)

        if box_position != box_portal_opening_position:
            return False

        portal_rules = {
            Position(8, 4): RIGHT,
            Position(10, 0): LEFT,
        }

        return portal_rules.get(agent_position) == action

    def check_agent_movement(
        self, agent_position: Position, box_position: Position, action: int
    ) -> bool:
        box_movement_check = Box_Movement_Checker().check_box_movement(
            agent_position, box_position, action
        )
        next_agent_position = Move().get_new_position(agent_position, action)
        movement_check = Movement_Checker().check_movement(agent_position, action)

        if box_movement_check:
            return True

        if movement_check and next_agent_position != box_position:
            return True

        return False

    def check_agent_movement_two_agents(
        self, all_positions: All_Positions, actions: All_Actions
    ) -> Movement_Check:
        agent1_position, agent2_position, box_position = all_positions.get_positions()
        action1, action2 = actions.get_actions()

        mc = Movement_Checker()
        move = Move()

        movement_check1 = mc.check_movement(agent1_position, action1)
        movement_check2 = mc.check_movement(agent2_position, action2)

        next_agent_position1 = move.get_new_position(agent1_position, action1)
        next_agent_position2 = move.get_new_position(agent2_position, action2)

        box_movement_check = Box_Movement_Checker().check_box_movement_two_agents(
            all_positions, actions
        )

        if box_movement_check:
            return Movement_Check(True, True)

        check1 = False
        check2 = False

        if movement_check1 and next_agent_position1 != box_position:
            check1 = True
        if movement_check2 and next_agent_position2 != box_position:
            check2 = True

        portal_check1 = self.check_agent_portal_movement(
            agent1_position, box_position, action1
        )
        portal_check2 = self.check_agent_portal_movement(
            agent2_position, box_position, action2
        )

        if portal_check1:
            check1 = True
        if portal_check2:
            check2 = True

        return Movement_Check(check1, check2)


class Box_Movement_Checker:
    def __init__(self):
        self.mover = Move()
        self.movement_checker = Movement_Checker()

    def check_box_movement(
        self, agent_position: Position, box_position: Position, action: int
    ) -> bool:
        new_agent_position = self.mover.get_new_position(agent_position, action)

        return (
            self.movement_checker.check_movement(box_position, action)
            if new_agent_position == box_position
            else False
        )

    def check_box_movement_two_agents(
        self, all_positions: All_Positions, actions: All_Actions
    ) -> bool:
        agent1_position, agent2_position, box_position = all_positions.get_positions()
        action1, action2 = actions.get_actions()

        if action1 != action2:
            return False

        move = self.mover

        new_agent1_position = move.get_new_position(agent1_position, action1)
        new_agent2_position = move.get_new_position(agent2_position, action2)

        box_movement_check = False

        if (
            new_agent1_position == box_position or new_agent2_position == box_position
        ) and (agent1_position == agent2_position):
            box_movement_check = self.movement_checker.check_movement(
                box_position, action1
            )

        return box_movement_check


class Move_Box:
    def move_box(self, box_position: Position, action: int) -> Position:
        box_movement_check = Movement_Checker().check_movement(box_position, action)

        if box_movement_check:
            return Move().get_new_position(box_position, action)
        else:
            return box_position


class Move_Through_Portal:
    def move_through_portal(
        self, agent_position: Position, box_position: Position, action: int
    ) -> Position:

        box_portal_opening_position = Position(8, 0)

        portal_map = {
            (Position(8, 4), RIGHT): Position(10, 0),  # right → left
            (Position(10, 0), LEFT): Position(8, 4),  # left → right
        }

        if box_position == box_portal_opening_position:
            return portal_map.get((agent_position, action), agent_position)

        return agent_position


class Move_Agent:
    def __init__(self):
        self.mover = Move()
        self.portal_mover = Move_Through_Portal()
        self.movement_checker = Agent_Movement_Checker()

        self.action_map = {
            LEFT: [LEFT, UP, DOWN],
            RIGHT: [RIGHT, UP, DOWN],
            UP: [LEFT, RIGHT, UP],
            DOWN: [LEFT, RIGHT, DOWN],
        }

    def get_actual_action(self, action: int) -> int:
        return random.choice(self.action_map[action])

    def move_agent_frozen_lake(self, agent_position: Position, action: int) -> Position:
        action = self.get_actual_action(action)
        return self.move_agent(agent_position, Position(8, 0), action)

    def move_agent(
        self, agent_position: Position, box_position: Position, action: int
    ) -> Position:

        next_agent_position = self.portal_mover.move_through_portal(
            agent_position, box_position, action
        )
        if next_agent_position != agent_position:
            return next_agent_position

        if self.movement_checker.check_agent_movement(
            agent_position, box_position, action
        ):
            return self.mover.get_new_position(agent_position, action)

        return agent_position


class Move_Everything:
    def __init__(self):
        self.box_movement_checker = Box_Movement_Checker()
        self.agent_mover = Move_Agent()
        self.box_mover = Move_Box()
        self.default_agent_position2 = Position(-1, -1)

    def move_Everything(
        self, agent_position: Position, box_position: Position, action: int
    ) -> All_Positions:
        box_movement_check = self.box_movement_checker.check_box_movement(
            agent_position, box_position, action
        )
        new_agent_position = self.agent_mover.move_agent(
            agent_position, box_position, action
        )
        new_box_position = (
            self.box_mover.move_box(box_position, action)
            if box_movement_check
            else box_position
        )

        return All_Positions(
            new_agent_position, self.default_agent_position2, new_box_position
        )


class Move_Two_Agents:
    def __init__(self):
        self.agent_mover = Move_Agent()
        self.box_mover = Move_Box()
        self.agent_movement_checker = Agent_Movement_Checker()
        self.fl_checker = Frozen_Lake_Checker()
        self.box_movement_checker = Box_Movement_Checker()

    def move_two_agents(
        self, all_positions: All_Positions, actions: All_Actions
    ) -> All_Positions:
        agent1_position, agent2_position, box_position = all_positions.get_positions()
        action1, action2 = actions.get_actions()

        box_movement_check = self.box_movement_checker.check_box_movement_two_agents(
            all_positions, actions
        )

        flc_check1 = self.fl_checker.check_frozen_lake(agent1_position)
        flc_check2 = self.fl_checker.check_frozen_lake(agent2_position)

        if flc_check1:
            new_agent1_position = self.agent_mover.move_agent_frozen_lake(
                agent1_position, action1
            )
        else:
            new_agent1_position = self.agent_mover.move_agent(
                agent1_position, box_position, action1
            )

        if flc_check2:
            new_agent2_position = self.agent_mover.move_agent_frozen_lake(
                agent2_position, action2
            )
        else:
            new_agent2_position = self.agent_mover.move_agent(
                agent2_position, box_position, action2
            )

        if box_movement_check:
            new_box_position = self.box_mover.move_box(box_position, action1)
            return All_Positions(
                new_agent1_position, new_agent2_position, new_box_position
            )

        agent_movement_check = (
            self.agent_movement_checker.check_agent_movement_two_agents(
                all_positions, actions
            )
        )

        check1, check2 = agent_movement_check.get_checks()

        if check1 or flc_check1:
            agent1_position = new_agent1_position
        if check2 or flc_check2:
            agent2_position = new_agent2_position

        return All_Positions(agent1_position, agent2_position, box_position)


# Implement Frozen Lake Actions because they are not really implemented in either environment


class Garden_Environment_Checker:
    def check_garden_environment():
        pass