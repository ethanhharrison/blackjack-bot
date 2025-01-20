"""Agent that will only hit below 12"""

import random
from gym_env.enums import Action
from agents.agent import Agent

class NeverBustAgent(Agent):
    
    def __init__(self, name, env):
        super().__init__(name, env)
        
    def action(self, action_space, observation):
        player_sum, dealer_card, usable_ace = observation
        if player_sum == 11 and Action.DOUBLE in action_space:
            return Action.DOUBLE
        elif player_sum >= 12:
            return Action.STAY
        else:
            return Action.HIT
   