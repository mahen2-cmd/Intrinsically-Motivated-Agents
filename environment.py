from movement import *

class GridWorld_Portal:
    def __init__(self):
        self.number_of_steps = 0

        self.agent1_position = Position(0, 2)
        self.agent2_position = Position(3, 5)
        self.box_position = Position(4, 2)

        self.all_entity_positions = All_Positions(self.agent1_position, self.agent2_position, self.box_position)


    def set_position(self, positions):
        self.agent1_position, self.agent2_position, self.box_position = positions.get_positions()
        self.all_entity_positions = positions


    def step(self, actions: All_Actions) -> All_Positions:

        if self.number_of_steps == 1000:
            return self.all_entity_positions


        self.number_of_steps += 1
        self.all_entity_positions = Move_Two_Agents().move_two_agents(self.all_entity_positions, actions)

        self.agent1_position, self.agent2_position, self.box_position = self.all_entity_positions.get_positions()

        return self.all_entity_positions



    def reset(self):
        self.__init__()