"""Base Class for a Blackjack Agent"""

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from gym_env.enums import Action

class Agent:
    
    def __init__(self, name, env):
        self.name = name
        self.env = env
        self.model = None
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
        
    def visualize_policy(self):
        states = [np.array([x, y, z]) for x in range(3, 22) for y in range(2, 12) for z in range(2)]
        actions = []
        
        if self.model:
            actions = [self.model.predict(np.array(state))[0] for state in states]
        else:
            for state in states:
                legal_moves = [Action.STAY, Action.HIT, Action.DOUBLE]
                act = self.action(legal_moves, state)
                actions.append(act.value)

        hard_action_matrix = np.array(actions).reshape((19, 10, 2))[:, :, 0] # Hard total
        soft_action_matrix = np.array(actions).reshape((19, 10, 2))[:, :, 1] # Soft total
        
        cmap = sns.cubehelix_palette(start=2.8, rot=.1, light=0.9, n_colors=3)
        grid_kws = {'width_ratios': (0.9, 0.03), 'wspace': 0.18}
        fig, (ax, cbar_ax) = plt.subplots(1, 2, gridspec_kw=grid_kws)
        ax = sns.heatmap(hard_action_matrix, ax=ax, cbar_ax=cbar_ax, cmap=ListedColormap(cmap),
                 linewidths=.5, linecolor='lightgray',
                 cbar_kws={'orientation': 'vertical'})
        
        cbar_ax.set_yticklabels(['STAY', 'HIT', 'DOUBLE'])
        cbar_ax.yaxis.set_ticks([1/3, 1, 5/3])
        
        ax.set_ylabel("Player Sum")
        ax.set_xlabel("Dealer Show Card")
        ax.set_title(f"Hard Total Policy for {self.name}")
        
        locs, labels = plt.xticks()
        plt.setp(labels, rotation=0)
        locs, labels = plt.yticks()
        plt.setp(labels, rotation=0)
        
        fig.savefig(f"agents/agent_policies/{self.name}_hard_policy.png")
                
        cmap = sns.cubehelix_palette(start=2.8, rot=.1, light=0.9, n_colors=3)
        grid_kws = {'width_ratios': (0.9, 0.03), 'wspace': 0.18}
        fig, (ax, cbar_ax) = plt.subplots(1, 2, gridspec_kw=grid_kws)
        ax = sns.heatmap(soft_action_matrix, ax=ax, cbar_ax=cbar_ax, cmap=ListedColormap(cmap),
                 linewidths=.5, linecolor='lightgray',
                 cbar_kws={'orientation': 'vertical'})
        
        cbar_ax.set_yticklabels(['STAY', 'HIT', 'DOUBLE'])
        cbar_ax.yaxis.set_ticks([1/3, 1, 5/3])
        
        ax.set_ylabel("Player Sum")
        ax.set_xlabel("Dealer Show Card")
        ax.set_title(f"Soft Total Policy for {self.name}")
        
        locs, labels = plt.xticks()
        plt.setp(labels, rotation=0)
        locs, labels = plt.yticks()
        plt.setp(labels, rotation=0)
        
        fig.savefig(f"agents/agent_policies/{self.name}_soft_policy.png")
    
    