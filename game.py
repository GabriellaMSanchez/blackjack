from entities import Card, Deck, Participant

def run():
    # first get user settings at the beginning of the game
    bankroll = get_user_bankroll()
    # next is setting up player object, dealer object, and deck object.
    player, dealer, deck = setup(bankroll)
    playing = True
    while playing:
        play_round(player, dealer, deck)
        playing = ask_player_to_play_again()

def ask_player_to_play_again():
    return input(f"Would you like to play again? [Y/N] ").lower() == 'y'

def play_round(player, dealer, deck):
    # player places their bet
    bet = get_user_bet()
    # place the bet
    place_bet(player, dealer, bet)
    # deal the cards
    deal(player, dealer, deck)
    # hits the user until the user is busted or chooses to stay
    hit_or_stay(player, deck)
    # check to see if the player is busted
    if not player_is_busted(player):
        dealers_turn(player, dealer, deck)
    else:
        print(f"Your hand value is {player.hand_value()}. You have busted.")
    # check winner
    dealer_won = dealer_did_win(player, dealer, bet)
    if dealer_won:
        print(f"Dealer won! {bet * 2} added to bankroll.")
        add_winnings(dealer, bet)
    else:
        print(f"Player won! {bet * 2} added to bankroll.")
        add_winnings(player, bet)
    # player and deal should return their hands to the original deck
    cleanup(player, dealer, deck)

def setup(bankroll):
    player = Participant(bankroll, "Player")
    dealer = Participant(bankroll, "Dealer")
    deck = Deck()
    deck.shuffle()
    return (player, dealer, deck)

def get_user_bankroll():
    # choose bankroll
    print("Welcome to Blackjack!")
    bankroll = input("Player, what is the value of your bankroll? ")
    while not bankroll.isnumeric():
        print("Hey! That's not a number!")
        bankroll = input("What is the value of your bankroll? ")
    return int(bankroll)

def get_user_bet():
    # choose bet
    bet = input(f"What would you like to bet?: ")
    while not bet.isnumeric():
        print("Hey! That's not a number!")
        bet = input(f"What would you like to bet?: ")
    return int(bet)

def place_bet(player, dealer, bet):
    player.place_bet(bet)
    dealer.place_bet(bet)

def deal(player, dealer, deck):
    add_card(player, deck)
    add_card(dealer, deck)
    add_card(player, deck)
    add_card(dealer, deck)

def ask_user_to_hit(player):
    # hit_me will result in a bool
    return input(f"Player your hands' value is: {player.hand_value()}.\
        \nWould you like to hit? [Y/N] ").lower().startswith('y')

def hit_or_stay(player, deck):
    is_busted = False
    hit_me = ask_user_to_hit(player)

    while not is_busted and hit_me:
        add_card(player, deck)
        is_busted = player_is_busted(player)
        if is_busted:
            break
        hit_me = ask_user_to_hit(player)

def player_is_busted(player) -> bool:
    if player.hand_value() > 21:
        return True
    return False

def dealers_turn(player, dealer, deck):
    is_busted = False

    while not is_busted and dealer.hand_value() < player.hand_value():
        add_card(dealer, deck)
        is_busted = player_is_busted(dealer)

def add_card(player, deck):
    player.add_card(deck.draw())

def dealer_did_win(player, dealer, bet):
    if player_is_busted(player):
        return True
    if player_is_busted(dealer):
        return False
    # if no one is busted run below
    if dealer.hand_value() >= player.hand_value():
        return True
    else:
        return False

def add_winnings(player, bet):
    player.add_winnings(bet * 2)

def cleanup(player, dealer, deck):
    for _ in range(len(player.hand)):
        deck.add_card(player.hand.pop())
    for _ in range(len(dealer.hand)):
        deck.add_card(dealer.hand.pop())
    deck.shuffle()

if __name__ == '__main__':
    run()
