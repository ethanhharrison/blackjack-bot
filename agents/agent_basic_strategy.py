"""Agent that plays by the book"""

from agents.agent import Agent
from gym_env.enums import Action

class BasicStrategyAgent(Agent):
    
    def __init__(self, name, env):
        super().__init__(name, env)
        self.hard_total_action = {}
        self.soft_total_action = {}
        self._initialize_hard_strategy()
        self._initialize_soft_strategy()
        
    def _initialize_hard_strategy(self):
        """Creates the basic strategy used by the agent when there is no usable ace."""
        all_hit = {dealer_card: Action.HIT for dealer_card in range(2, 12)}
        all_double = {dealer_card: Action.DOUBLE for dealer_card in range(2, 12)}
        all_stay = {dealer_card: Action.STAY for dealer_card in range(2, 12)}
        for player_sum in range(3, 9):
            self.hard_total_action[player_sum] = all_hit
        self.hard_total_action[9] = {dealer_card: Action.DOUBLE for dealer_card in range(3, 7)}
        self.hard_total_action[9].update({dealer_card: Action.DOUBLE for dealer_card in [2] + list(range(7, 12))})
        self.hard_total_action[10] = all_double
        self.hard_total_action[10].update({dealer_card: Action.DOUBLE for dealer_card in range(10, 12)})
        self.hard_total_action[11] = all_double
        self.hard_total_action[12] = {dealer_card: Action.STAY for dealer_card in range(4, 7)}
        self.hard_total_action[12].update({dealer_card: Action.HIT for dealer_card in [2, 3] + list(range(7, 12))})
        for player_sum in range(13, 17):
            self.hard_total_action[player_sum] = {dealer_card: Action.STAY for dealer_card in range(2, 7)}
            self.hard_total_action[player_sum].update({dealer_card: Action.HIT for dealer_card in range(7, 12)})
        for player_sum in range(17, 22):
            self.hard_total_action[player_sum] = all_stay
            
    def _initialize_soft_strategy(self):
        """Creates the basic strategy used by the agent when there is a usable ace."""
        all_hit = {dealer_card: Action.HIT for dealer_card in range(2, 12)}
        all_stay = {dealer_card: Action.STAY for dealer_card in range(2, 12)}
        for player_hand in range(13, 15):
            self.soft_total_action[player_hand] = all_hit
            self.soft_total_action[player_hand][5] = Action.DOUBLE
            self.soft_total_action[player_hand][6] = Action.DOUBLE
        for player_hand in range(15, 18):
            self.soft_total_action[player_hand] = all_hit
            self.soft_total_action[player_hand][4] = Action.DOUBLE
            self.soft_total_action[player_hand][5] = Action.DOUBLE
            self.soft_total_action[player_hand][6] = Action.DOUBLE
        self.soft_total_action[18] = all_stay
        self.soft_total_action[18].update({dealer_card: Action.DOUBLE for dealer_card in range(3, 7)})
        self.soft_total_action[18].update({dealer_card: Action.HIT for dealer_card in range(9, 12)})
        for player_hand in range(19, 22):
            self.soft_total_action[player_hand] = all_stay
            
    def action(self, action_space, observation):
        player_sum, dealer_card, usable_ace = observation
        if not usable_ace:
            act = self.hard_total_action[player_sum][dealer_card]
        else:
            act = self.soft_total_action[player_sum][dealer_card]
        if act not in action_space: # Trying to double when not possible
            return Action.HIT
        else:
            return act
        
    