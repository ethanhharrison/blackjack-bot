import logging
import numpy as np

from gym import Env
from gym.spaces import Discrete, Tuple
from enums import Action


class Blackjack(Env):
    """Blackjack Environment"""
    
    def __init__(self, num_decks=1, bet=1, render_mode=None):
        """
        Only need to initialize the game once in the beginning

        Args:
            num_decks (int): The number of decks to play with
            bet (float): how much to bet
            render_mode (bool, optional): How to render the game. If None, do not render 
        """
        self.num_decks = num_decks
        self.bet = bet
        self.observation = None
        self.deck = None
        self.player_hand = None
        self.dealer_hand = None
        self.legal_moves = None
        self.reward = None
        self.terminated = None
        self.can_move = None
        self.illegal_move_reward = -1
        
        # Gym API
        self.render_mode = render_mode
        self.action_space = Discrete(len(Action))
        self.observation_space = Tuple((Discrete(32), Discrete(11), Discrete(2))) # Player's score, dealer's card, usable ace
    
    def reset(self):
        """Resets the game. Creates a new environment and returns the agent's observation"""
        self.reward = 0
        self.observation = None
        self.terminated = None
        self.can_move = True
        self._create_deck()
        self._deal_cards()
        self._get_observation()
        return self.observation
    
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
        self._check_game_over()
        return self.observation
    
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
            self.reward -= self.bet # Player busted
        elif dealer_sum > 21:
            self.reward = self.bet # Dealer busted
        elif player_sum > dealer_sum:
            self.reward = self.bet # Player won
        elif player_sum == dealer_sum:
            self.reward = 0 # Player shoved
            
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
        self.reward = self.illegal_move_reward
            
    def _get_observation(self):
        """Observe the environment"""
        if not self.terminated:
            self._get_legal_moves()

        player_sum, usable_ace = self._get_hand_value(self.player_hand)
            
        dealer_card = self.dealer_hand[0]
        dealer_value = self._get_card_value(dealer_card)
        
        self._get_legal_moves()
        self.observation = (player_sum, dealer_value, usable_ace)
        
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
        pass
    
    def close(self):
        """Closes the environment. Used to stop any rendering"""
        pass
    
if __name__ == "__main__":
    bj = Blackjack()
    bj.reset()
    
                
    print("Dealer's Card:", bj.dealer_hand[0])
    
    while not bj.terminated:
        print("Your Hand:", bj.player_hand)
        print("0 = STAY, 1 = HIT, 2 = DOUBLE")
        act = input("Make your move: ")
        bj.step(int(act))
       
    print("Your Hand:", bj.player_hand)
    print("Dealer's Hand:", bj.dealer_hand) 
        
    if bj.reward > 0:
        print(f"You won {bj.reward}!")
    elif bj.reward == 0:
        print("You shoved")
    else:
        print(f"You lost {bj.reward} :(")