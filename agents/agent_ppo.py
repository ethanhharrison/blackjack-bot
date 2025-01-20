"""Blackjack agent trained using the PPO algorithm"""

import gym
import gym_env
from agents.agent import Agent
from gym.wrappers import NormalizeObservation, NormalizeReward
from stable_baselines3 import PPO

class PPOAgent(Agent):
    
    def __init__(self, name, env):
        super().__init__(name, env)
        self.model = PPO("MlpPolicy", self.env, verbose=1)
    
    def train(self, timesteps=1000):
        # env_norm = NormalizeObservation(self.env)
        # env_norm = NormalizeReward(env_norm)
        self.model.learn(total_timesteps=timesteps)
        self.model.save("ppo_blackjack")
    
    def action(self, action_space, observation, info=None):
        action, _states = self.model.predict(observation)
        return action
    
    def run(self, load=False, episodes=100):
        if load:
            try:
                self.model = PPO.load("ppo_blackjack")
            except:
                raise FileNotFoundError("Saved PPO model not found")
        super().run(episodes)