from gym.envs.registration import register
from gym_env.env import Blackjack

register(
    id="blackjack_env-v0", 
    entry_point="gym_env.env:Blackjack", 
    kwargs={"num_decks": 1, "render_mode": None, "verbose": True}
)