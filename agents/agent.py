"""Base Class for a Blackjack Agent"""

import matplotlib.pyplot as plt

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
        running_totals = [0]
        for reward in self.rewards:
            running_totals.append(running_totals[-1] + reward)
            
        plt.plot(running_totals)
        plt.xlabel("Episode")
        plt.ylabel("Running Total")
        plt.title(f"Running Total For {self.name} Agent")

        plt.savefig(f"results/{self.name}_agent_running_total.png")
            
                
    
    