import random

# Suits, Ranks, and Values of Cards

SUITS = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
RANKS = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight',
         'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
VALUES = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
         'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

# Card Class
# Cards have suits, ranks, and values

class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = VALUES[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"


# Deck Class this class should
    # instantiate new deck and hold as a list of Card objects
    # shuffle the deck
    # deal cards

class Deck:
    
    def __init__(self):
        # this only happens once upon creation of a new deck
        self.cards = []
        
        for suit in SUITS:
            for rank in RANKS:
                # this assumes the card class has already been defined
                # create the Card Object here
                self.cards.append(Card(suit, rank))
                
    def shuffle(self):
        # this does not return anything
        random.shuffle(self.cards)
    
    def draw(self):
        # note we remove one card from the list of all_cards
        return self.cards.pop()

    def add_card(self, new_card):
        self.cards.append(new_card)
    
    def __len__(self):
        return len(self.cards)


# Participant Class
# this will cover the dealer and the players

class Participant:
    
    def __init__(self, bankroll, name):
        self.bankroll = bankroll
        self.name = name
        # a new player has no cards
        self.hand = []
            
    def place_bet(self, bet):
        if bet > self.bankroll:
            max_possible = self.bankroll
            self.bankroll = 0
            return max_possible
        else:
            self.bankroll = self.bankroll - bet
            return bet
        
    def add_winnings(self, amount):
        # can add the amount won to the bankroll
        self.bankroll += amount
        
    def hand_value(self):
        hand_value = 0
        num_aces = 0
        for card in self.hand:
            if card.rank == 'Ace':
                num_aces += 1
            hand_value += card.value
        while num_aces >= 1 and hand_value > 21:
            hand_value -= 10
            num_aces -= 1
        return hand_value
    
    def __str__(self):
        return f"{self.name} has {len(self.hand)} cards. Their hand value is: {self.hand_value()}. Their bankroll is {self.bankroll}."

    def add_card(self, new_card):
        self.hand.append(new_card)
