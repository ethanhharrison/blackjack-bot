"""Base Class for a Blackjack Agent"""

class Agent:
    
    def __init__(self, name, env):
        self.name = name
        self.env = env
        self.actions = []
        self.rewards = []
        
    def action(self, action_space, observation, info=None):
        """Calculates the action based on the observation and action space"""
        raise NotImplementedError("Base class agent does not have actions implemented!")
    
    def run(self, episodes=100):
        """
        Runs the agent for a certain number of episodes. 
        Records the rewards for each episode and the actions taken.
        """
        for epoch in range(episodes):
            self.env.reset()
            game_actions = []
            while not self.env.terminated:
                self.env.render()
                act = self.action(self.env.legal_moves, self.env.observation)
                game_actions.append(act)
                self.env.step(act)
            self.env.render()
            self.actions.append(game_actions)
            self.rewards.append(self.env.reward)
            
    def get_metrics(self):
        """Shows the metrics of the agent's performance."""
        pass
            
                
    
    