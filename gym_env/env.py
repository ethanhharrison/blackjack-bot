import logging
import numpy as np

from gym import Env
from gym.spaces import Discrete, Box
from gym_env.enums import Action
from gym_env.rendering import BlackjackWindow

log = logging.getLogger(__name__)
logging.basicConfig(filename='log/env.log', level=logging.INFO)

class Blackjack(Env):
    """Blackjack Environment"""
    metadata = {"render_modes": ["human"], "render_fps": 30}
    
    def __init__(self, num_decks=1, render_mode=None, verbose=True):
        """
        Only need to initialize the game once in the beginning

        Args:
            num_decks (int): The number of decks to play with
            bet (float): how much to bet
            render_mode (bool, optional): How to render the game. If None, do not render 
        """
        self.num_decks = num_decks
        self.bet = None
        self.observation = None
        self.deck = None
        self.player_hand = None
        self.dealer_hand = None
        self.legal_moves = None
        self.reward = None
        self.terminated = None
        self.can_move = None
        self.screen = None
        self.illegal_move_reward = -1
        
        if not verbose:
            log.disabled = True
        
        # Gym API
        self.render_mode = render_mode
        self.action_space = Discrete(len(Action))
        self.observation_space = Box(
            low=np.array([0, 0, 0]),
            high=np.array([31, 10, 1]),
            dtype=np.float32
        ) # Player's score, dealer's card, usable ace
    
    def reset(self, seed=None, options=None):
        """Resets the game. Creates a new environment and returns the agent's observation"""
        log.info("")
        log.info("==================")
        log.info("Starting new game.")
        log.info("==================")
        
        super().reset(seed=seed)
        
        self.reward = 0
        self.bet = 1
        self.observation = None
        self.terminated = None
        self.can_move = True
        self._create_deck()
        self._deal_cards()
        self._get_observation()
        
        log.info(f"Player hand: {self.player_hand}, Dealer Show Card: {self.dealer_hand[0]}, Dealer Hand: {self.dealer_hand}")
        
        info = {}
        
        return self.observation, info
    
    def step(self, action):
        """
        The agent takes an action and updates the environment. Returns the agent's partial obeservation of the environment.

        Args:
            action: Needs to be an Action type
        """
        self._get_observation()
        if not self._check_game_over():
            if Action(action) not in self.legal_moves:
                self._illegal_move(action)
            else:
                self._process_action(Action(action))
                self._get_observation()
                
        log.info(f"Player: {Action(action)} - Player hand: {self.player_hand}")
        log.info(f"Dealer Show Card: {self.dealer_hand[0]}")
        log.info(f"Dealer Hand: {self.dealer_hand}")        
        
        terminated = self._check_game_over()
        truncated = False
        info = {}
        
        return self.observation, self.reward, terminated, truncated, info
    
    def _check_game_over(self):
        """Check if player/dealer has blackjack or busted"""
        player_sum, _ = self._get_hand_value(self.player_hand)
        dealer_sum, _ = self._get_hand_value(self.dealer_hand)
        game_over = False
        if player_sum == 21 and len(self.player_hand) == 2:
            game_over = True
        if dealer_sum == 21 and len(self.dealer_hand) == 2:
            game_over = True
        if player_sum > 21 or dealer_sum > 21:
            game_over = True
        if not self.can_move:
            game_over = True
        if game_over:
            self._game_over()
        return game_over
    
    def _game_over(self):
        """End of a game. Calculates the reward."""
        
        self.terminated = True
        player_sum, _ = self._get_hand_value(self.player_hand)
        dealer_sum, _ = self._get_hand_value(self.dealer_hand)
        if player_sum == 21 and len(self.player_hand) == 2: 
            self.reward = 1.5 * self.bet # Blackjack
        elif player_sum > 21:
            self.reward = -self.bet # Player busted
        elif dealer_sum > 21:
            self.reward = self.bet # Dealer busted
        elif player_sum > dealer_sum:
            self.reward = self.bet # Player won
        elif player_sum < dealer_sum:
            self.reward = -self.bet # Dealer won
        elif player_sum == dealer_sum:
            self.reward = 0 # Shove
            
        log.info("Game over.")
        log.info(f"Player sum: {player_sum}, Dealer sum: {dealer_sum}")
        log.info(f"Player received reward {self.reward}")
            
    def _process_action(self, action):
        """Process the action by the player."""
        if action == Action.STAY:
            self._process_dealer()
            self.can_move = False
        elif action == Action.DOUBLE:
            self.player_hand.append(self._draw_card())
            self.bet *= 2
            self.can_move = False
            self._process_dealer()
        elif action == Action.HIT:
            self.player_hand.append(self._draw_card())
    
    def _process_dealer(self):
        dealer_sum, _ = self._get_hand_value(self.dealer_hand)
        while dealer_sum < 17:
            self.dealer_hand.append(self._draw_card())
            dealer_sum, _ = self._get_hand_value(self.dealer_hand)
    
    def _get_legal_moves(self):
        """Determines what moves are legal in the current environment"""
        if not self.can_move:
            self.legal_moves = []
            return
        self.legal_moves = [Action.STAY, Action.HIT]
        if len(self.player_hand) == 2:
            self.legal_moves.append(Action.DOUBLE)
            
    def _illegal_move(self, action):
        log.warning(f"{action} is an illegal move, try again. Currently allowed: {self.legal_moves}")
        # self.reward = self.illegal_move_reward
            
    def _get_observation(self):
        """Observe the environment"""
        if not self.terminated:
            self._get_legal_moves()

        player_sum, usable_ace = self._get_hand_value(self.player_hand)
            
        dealer_card = self.dealer_hand[0]
        dealer_value = self._get_card_value(dealer_card)
        
        self._get_legal_moves()
        self.observation = np.array([player_sum, dealer_value, usable_ace], dtype=np.float32)
        
    def _get_card_value(self, card):
        """Get the value of the card"""
        if card[0] in "23456789":
            return int(card[0])
        elif card[0] in "TJQK":
            return 10
        else:
            return 11
        
    def _get_hand_value(self, hand):
        """Get the value of the hand. Also returns how many aces can become soft"""
        total = 0
        usable_aces = 0
        for card in hand:
            card_value = self._get_card_value(card)
            if card_value == 11:
                usable_aces = 1
            total += card_value
        while total > 21 and usable_aces > 0:
            total -= 10
            usable_aces -= 1
        return total, usable_aces
                
    def _create_deck(self):
        """Creates the deck of cards. Face cards and suits are preserved for rendering purposes."""
        values = "23456789TJQKA"
        suits = "SHCD"
        self.deck = []
        _ = [self.deck.append(v + s) for v in values for s in suits for _ in range(self.num_decks)]
            
    def _draw_card(self):
        """Draws a single card from the deck"""
        card = np.random.randint(0, len(self.deck))
        return self.deck.pop(card)
            
    def _deal_cards(self):
        """Deals the deck to the player and the dealer"""
        cards = [self._draw_card() for _ in range(4)]
        self.player_hand = cards[:2]
        self.dealer_hand = cards[2:]
        
    def render(self):
        """Renders the game"""
        if self.render_mode == "human":
            self._render_human()
            self.screen.update()
    
    def _render_human(self):
        """Renders the game"""
        screen_width = 550
        screen_height = 400
        
        if self.screen is None:
            self.screen = BlackjackWindow(screen_width + 50, screen_height + 50)
        self.screen.reset()
        
        player_sum, dealer_card, _ = self.observation
        
        # Dealer's cards
        x, y = 250 - 50 * (len(self.dealer_hand) - 2), 100
        for c in self.dealer_hand[:-1]:
            self.screen.card(x, y, c)
            x += 100
        if not self.terminated:
            self.screen.text(f"Dealer Card: {dealer_card}", 300, 40)
            self.screen.card(x, y, "HIDDEN")
        else:
            dealer_sum, _ = self._get_hand_value(self.dealer_hand)
            self.screen.text(f"Dealer Sum: {dealer_sum}", 300, 40)
            self.screen.card(x, y, self.dealer_hand[-1])
        
        # Player's cards
        self.screen.text(f"Player Sum: {player_sum}", 300, 240)
        x, y = 250 - 50 * (len(self.player_hand) - 2), 300
        for c in self.player_hand:
            self.screen.card(x, y, c)
            x += 100
    
    def close(self):
        """Closes the environment. Used to stop any rendering"""
        pass
    
if __name__ == "__main__":
    # User play
    bj = Blackjack(render_mode="human")
    
    while True:
        bj.reset()
        
        print("Dealer's Card:", bj.dealer_hand[0])
        
        bj.render()
        
        while not bj.terminated:
            bj.render()
            print("Your Hand:", bj.player_hand)
            print("0 = STAY, 1 = HIT, 2 = DOUBLE")
            act = input("Make your move: ")
            bj.step(int(act))
        
        bj.render()
        print("Your Hand:", bj.player_hand)
        print("Dealer's Hand:", bj.dealer_hand) 
            
        if bj.reward > 0:
            print(f"You won {bj.reward}!")
        elif bj.reward == 0:
            print("You shoved")
        else:
            print(f"You lost {bj.reward} :(")
        quit = input("Type 'QUIT' to exit the game. Press ENTER to play again.")
        if quit:
            break