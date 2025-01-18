"""Base Class for a Blackjack Agent"""

class Agent:
    
    def __init__(self, name):
        self.name = name
        self.episodes = []
        
    def action(self, action_space, observation, info=None):
        """Calculates the action based on the observation and action space"""
        raise NotImplementedError("Base class agent does not have actions implemented!")
    
    def run(self, env, episodes=100):
        """
        Runs the agent for a certain number of episodes. 
        Records the rewards for each episode and the actions taken.
        """
        pass
    
    