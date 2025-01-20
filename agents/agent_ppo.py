"""Blackjack agent trained using the PPO algorithm"""

import gym
import gym_env
from agents.agent import Agent
from gym.wrappers import NormalizeObservation, NormalizeReward
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

class PPOAgent(Agent):
    
    def __init__(self, name, env):
        super().__init__(name, env)
        try:
            self.model = PPO.load("ppo_blackjack")
        except:
            self.model = PPO("MlpPolicy", self.env, verbose=1)
    
    def train(self, timesteps=1000):
        env_norm = NormalizeObservation(self.env)
        env_norm = NormalizeReward(env_norm)
        self.model.learn(total_timesteps=timesteps)
        self.model.save("ppo_blackjack")
    
    def action(self, action_space, observation, info=None):
        action, _states = self.model.predict(observation)
        return action