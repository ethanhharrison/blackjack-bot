import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        
    def __str__(self):
        return f"{self.value} of {self.suit}"
    
    def __repr__(self):
        return f"Card(suit={self.suit}, value={self.value})"
        
    def __eq__(self, other):
        return self.suit == other.suit and self.value == other.value
    
    def __hash__(self):
        return hash((self.suit, self.value))
    
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
            for value in [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]:
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

class Hand:
    """
    A hand for blackjack. Each hand has the option to stay, hit, double, or split.
    """
    def __init__(
        self,
        cards: list[Card],
        bet_amount: float,
        is_stood: bool = False,
    ) -> None:
        self.cards = cards
        self.bet_amount = bet_amount
        self.is_stood = is_stood
    
    def value(self):
        total = 0
        for card in self.cards:
            total += card.value
        return total
        
    def is_bust(self):
        return self.value() > 21
    
    def can_hit(self):
        return not self.is_stood and not self.is_bust()
    
    def can_double(self):
        return not self.is_stood and len(self.cards) == 2
    
    def can_split(self):
        return not self.is_stood and len(self.cards) == 2 and self.cards[0].value == self.cards[1].value
    
    def __str__(self):
        result = ""
        result = f"Total: {self.value()}, Cards: ["
        for card in self.cards:
            result += str(card) + ", "
        result = result[:-2] + "]"
        return result
            
class Game:
    """
    A game of Blackjack
    """
    def __init__(self, deck: Deck, bet_amount: float):
        self.deck = deck
        
        player_hand = Hand([], bet_amount)
        dealer_hand = Hand([], -1)
        
        player_hand.cards.append(self.deck.draw_card())
        player_hand.cards.append(self.deck.draw_card())
        
        dealer_hand.cards.append(self.deck.draw_card())
        dealer_hand.cards.append(self.deck.draw_card())
        
        self.player_hands = [player_hand]
        self.dealer_hand = dealer_hand
        
    
    def make_action(self, hand: Hand, action: str) -> bool:
        """
        Makes an action with the current hand:
            - stand: no cards added to the hand, and can no longer draw any more cards
            - hit: Add one card to your hand, and you can still add more cards
            - double: double your bet amount and add one card to your hand, but you cannot add any more cards
            - split: Only possible if the two cards in hand have the same value. Makes each card into a new hand
        Returns True if the action was successful, False if not
        """
        if action == "stand":
            hand.is_stood = True
            return True
        elif action == "hit":
            if hand.can_hit():
                hand.cards += [self.deck.draw_card()]
                return True
            else:
                print("Cannot hit again, please take another action.")
                return False
        elif action == "double":
            if hand.can_double():
                hand.cards += [self.deck.draw_card()]
                hand.bet_amount *= 2
                hand.is_stood = True # Cannot make any more actions
                return True
            else:
                print("Cannot double, please take another action.")
                return False
        elif action == "split":
            if hand.can_split():
                new_hand = Hand([hand.cards[0]], self.bet_amount)
                hand.cards = [hand.cards[1]]
                self.player_hands.append(new_hand)
                return True
            else:
                print("Cannot split, please take another action.")
                return False
    
    def get_reward(self) -> int:
        total_reward = 0
        if self.dealer_hand.is_bust():
            for hand in self.player_hands:
                if not hand.is_bust():
                    total_reward += 2 * hand.bet_amount
            return total_reward
        dealer_value = self.dealer_hand.value()
        for hand in self.player_hands:
            if hand.value() > dealer_value:
                total_reward += 2 * hand.bet_amount
            elif hand.value() == dealer_value:
                total_reward += hand.bet_amount
        return total_reward
            
    def play_game(self) -> int:
        # Let player make actions until no more actions remaining
        while True:
            available_hands = []
            for hand in self.player_hands:
                if not hand.is_stood and not hand.is_bust():
                    available_hands.append(hand)
            if len(available_hands) == 0:
                break
            for hand in available_hands:
                success = False
                while not success:
                    print(f"The dealer is showing this card: {self.dealer_hand.cards[0]}")
                    action = input(f"Make an action for this hand: {hand} ").lower()
                    success = self.make_action(hand, action)
        print("Your final hands are:")
        for hand in self.player_hands:
            print(hand)
        # Let dealer make action
        dealer = self.dealer_hand
        while not dealer.is_stood and not dealer.is_bust():
            # Implement dealer strategy, always hit below 17, otherwise stand
            if dealer.value() < 17:
                self.make_action(dealer, "hit")
            else:
                self.make_action(dealer, "stand")
        print(f"The dealer ended with this hand: {dealer}")
        reward = self.get_reward()
        return reward
    
if __name__ == "__main__":
    deck = Deck()
    bet_amount = float(input("Enter how much you want to bet? "))
    game = Game(deck, bet_amount)
    reward = game.play_game()
    print(f"You won {reward}. Yippee! (or not yippee)")