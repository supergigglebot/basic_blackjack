import random

suits = ('Hearts','Diamonds','Spades','Clubs')

ranks = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')

class Card:

    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit

    def __repr__(self):
        return self.__str__()

class Deck:

    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit,rank)
                self.all_cards.append(created_card)

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal(self):
        return self.all_cards.pop()

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def score(self):
        return self.value

    def add_card(self,card):
        self.cards.append(card)

        if card.rank == 'Ace':
            self.aces += 1
            self.value += 11
        elif card.rank in ['Jack','Queen','King']:
            self.value += 10
        else:
            card_values = {'Two':2, 'Three':3, 'Four':4, 'Five':5,
                           'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10}
            self.value += card_values[card.rank]

        self.adjust_for_ace()

    def adjust_for_ace(self):
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

class Player(Hand):
    def __init__(self,name):
        Hand.__init__(self)
        self.name = name

    def __str__(self):
        cards_as_strings = ', '.join(str(card) for card in self.cards)
        return f'Your Hand:\n{cards_as_strings}\nValue: {self.value}'

class Dealer(Hand):
    def __init__(self, name):
        Hand.__init__(self)
        self.name = name

    def __str__(self):
        return f'Dealer Hand:\n{self.cards[0]} and one face-down card.'

    def fullhand(self):
        cards_as_strings = ', '.join(str(card) for card in self.cards)
        return f'Dealer Had:\n{cards_as_strings}\nValue: {self.value}\n'

class Chips:
    def __init__(self,total=100):
        self.total = total

    def win(self,amount):
        self.total += amount
        return self.total

    def lose(self,amount):
        self.total -= amount
        return self.total

    def bet(self):
        if self.total == 0:
            print("Here are 5 courtesy chips on the house.")
            self.total += 5
        bet_obtained = False
        while not bet_obtained:
            while True:
                try:
                    amount = int(input("How much would you like to bet? "))
                except:
                    print("Invalid input. Please try again.")
                else:
                    break

            if amount > self.total:
                print("Insufficient Chips!")
                continue

            else:
                return amount

    def __str__(self):
        return f"You have {self.total} chips."

def play_again():
    while True:
        req = input("Would you like to play again? y/n ")
        if req == 'y':
            return True
        elif req == 'n':
            return False
        elif req == 'housemode':
            house = int(input("Welcome, Casino owner. How many chips would you like to add to your account?: "))
            return house
        else:
            print('Please input y or n')

def player_turn():
        cont = input("Would you like to Hit or Stand? (please type h or s) ")
        if cont.lower() in ('h', 's'):
            return cont
        else:
            print("That is not an option. Please enter H or S. ")

# Rough Gameplay Logic
bankroll = Chips(100)

game_on = True
print("Let's play Blackjack!\n")

while game_on:
    player_one = Player("Player One")
    dlr = Dealer("Dealer")
    blackjack_deck = Deck()
    dealerwin = False
    blackjack_deck.shuffle()

    for i in range(2):
        dlr.add_card(blackjack_deck.deal())
        player_one.add_card(blackjack_deck.deal())

    print(f"{dlr}\n\n{player_one}\n\n{bankroll}")

    current_bet = bankroll.bet()

    while True:
        choice = player_turn()
        if choice == 's':
            break

        elif choice == 'h':
            player_one.add_card(blackjack_deck.deal())
            print(player_one)

        if player_one.score() > 21:
            print("You went bust!\n")
            bankroll.lose(current_bet)
            dealerwin = True

    if not dealerwin:
        while True:
            if dlr.score() < 17:
                dlr.add_card(blackjack_deck.deal())
            else:
                break
            if dlr.score() > 21:
                print("Dealer went bust! You win!\n")
                bankroll.win(current_bet)
                break

    if player_one.score() <= 21 and dlr.score() <= 21:
        if player_one.score() > dlr.score():
            print("\nYou beat the dealer!\n")
            bankroll.win(current_bet)
        elif dlr.score() > player_one.score():
            print("\nDealer Won!\n")
            bankroll.lose(current_bet)
        elif dlr.score() == player_one.score():
            print("\nIt's a push!\n")
        else:
            print("Something just happened.")

    print(dlr.fullhand())

    replay = play_again()
    if replay == True:
        continue
    elif type(replay) == int:
        bankroll.win(replay)
        continue
    else:
        game_on = False

print("Thanks for playing!")