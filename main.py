import gym
import gym_env
from agents.agent_random import RandomAgent
from agents.agent_never_bust import NeverBustAgent
from agents.agent_basic_strategy import BasicStrategyAgent

def main():
    env_name = "blackjack_env-v0"
    bj_env = gym.make(env_name, render_mode="human")
    # agt = RandomAgent("random", bj_env)
    agt = NeverBustAgent("never_bust", bj_env)
    # agt = BasicStrategyAgent("basic_strategy", bj_env)
    agt.run(episodes=1000)
    
    agt.get_metrics()
    
if __name__ == "__main__":
    main()