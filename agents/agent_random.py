"""Random Agent"""

import random
from agents.agent import Agent

class RandomAgent(Agent):
    
    def __init__(self, name, env):
        super().__init__(name, env)
        
    def action(self, action_space, observation):
        return random.choice(action_space)
    
