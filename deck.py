import random
from card import Card

class Deck:
    """
    Class represented the current deck of the game
    """
    @staticmethod
    def default_deck():
        """
        Creates a deck of 52 cards, 4 suits from 2 to Ace
        """
        deck = set()
        for suit in ["Spades", "Hearts", "Clubs", "Diamonds"]:
            for value in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]:
                deck.add(Card(suit, value))
        return deck
    
    def __init__(self, cards=default_deck()):
        self.cards = cards
        self.num_cards = len(self.cards)
        
    def remove_card(self, card):
        self.cards.remove(card)
        self.num_cards -= 1
        
    def draw_card(self):
        selected_card = random.choice(list(self.cards))
        self.remove_card(selected_card)
        return selected_card
        
        
