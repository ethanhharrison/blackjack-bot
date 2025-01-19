import gym
import gym_env
from agents.agent_random import RandomAgent
from agents.agent_never_bust import NeverBustAgent

def main():
    env_name = "blackjack_env-v0"
    bj_env = gym.make(env_name, render_mode="human")
    agt = NeverBustAgent("never_bust", bj_env)
    agt.run()
    
    print(agt.rewards)
    print("Avg Reward: ", sum(agt.rewards) / len(agt.rewards))
    
if __name__ == "__main__":
    main()