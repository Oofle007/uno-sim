import random
import statistics


class Player:
    def __init__(self):
        self.cards = []


class Card:
    def __init__(self, color=None, number=None, special_description=None):
        self.color = color
        self.number = number
        self.special_description = special_description


deck = []


def adding_special_cards_deck(special_value, colors, repeat_amount):
    for i in range(repeat_amount):
        color_index = 0
        for j in range(4):
            deck.append(Card(color=colors[color_index], special_description=special_value))
            color_index += 1


def create_deck():
    # Link to deck can be found here: https://commons.wikimedia.org/wiki/File:UNO_cards_deck.svg
    colors = ["Red", "Yellow", "Green", "Blue"]
    color_index = 0  # color_index keeps track of the current index of the colors list I'm iterating through
    for i in range(4):  # Adding 0s to the deck
        deck.append(Card(colors[color_index], 0))
        color_index += 1
    # Adding all normal color/number cards
    for j in range(2):  # Theres two of each card in the deck except for 0 cards
        color_index = 0
        for k in range(4):  # Theres 4 colors
            adding_number = 1
            for i in range(9):  # Adding each number of color
                deck.append(Card(colors[color_index], adding_number))
                adding_number += 1
            color_index += 1
    # Adding all special cards (skip, reverse, +2, wild, and +4)
    adding_special_cards_deck("skip", colors, 2)
    adding_special_cards_deck("reverse", colors, 2)
    adding_special_cards_deck("+2", colors, 2)
    adding_special_cards_deck("wild", colors, 1)
    adding_special_cards_deck("+4", colors, 1)
    random.shuffle(deck)  # Shuffling the deck


def find_playable_cards(current_player=None, cc=None, single_card=None):
    playable_cards = []
    # Finding playable cards
    if current_player:
        for c in current_player.cards:
            if c.color is cc.color and cc.color is not None:
                playable_cards.append(c)
                continue
            if c.number is cc.number and cc.number is not None:
                playable_cards.append(c)
                continue
            if c.special_description is cc.special_description and c.special_description is not None:
                playable_cards.append(c)
                continue
            if c.special_description == "wild" or c.special_description == "+4":
                playable_cards.append(c)
                continue
        return playable_cards
    else:
        if single_card.color is cc.color and cc.color is not None:
            playable_cards.append(single_card)
        if single_card.number is cc.number and cc.number is not None:
            playable_cards.append(single_card)
        if single_card.special_description is cc.special_description and single_card.special_description is not None:
            playable_cards.append(single_card)
        if single_card.special_description == "wild" or single_card.special_description == "+4":
            playable_cards.append(single_card)
        return len(playable_cards) == 0


def play_one_game(no_players):
    players = [Player() for i in range(no_players)]
    create_deck()
    # Dealing out cards
    for _ in range(7):  # Number of cards
        for player in players:  # Will give each player a card
            player.cards.append(deck[0])
            del deck[0]
            if len(deck) == 0:
                create_deck()
    no_turns = 0
    current_player_index = 0
    cc = deck[0]  # Current card
    del deck[0]
    stop = False
    direction = "right"
    while cc.special_description:
        cc = deck[0]
        del deck[0]
        if len(deck) == 0:
            create_deck()
    while not stop:
        current_player = players[current_player_index]  # Setting current player
        playable_cards = find_playable_cards(current_player, cc)
        # Defining the value of each playable card (how good it is)
        if len(playable_cards) > 0:  # Can I play a card?
            playable_card_values = []  # Keeps track of how good each card is
            # 0 number value = -100 (GET RID OF IT!)
            # +2 cards = 0.1 (just barely better than a zero card
            # Random card (just a color and number) = 1 (Value will decrease as we have more of that color in hand)
            # Special not wild or +4 or +2 = 5
            # Wild or +4 = 6
            for c in playable_cards:
                if c.number == 0:  # 0 number
                    playable_card_values.append(-100)
                    continue
                if not c.special_description:  # Random card
                    value = 1
                    for k in current_player.cards:
                        if k.color == c.color:
                            value *= 1.1
                    value -= 1
                    playable_card_values.append(value)
                    continue
                if c.special_description:
                    if c.special_description != "wild" and c.special_description != "+4" and c.special_description != "+2":
                        playable_card_values.append(5)
                        continue
                    elif c.special_description == "+2":
                        playable_card_values.append(0.1)
                        continue
                    else:
                        playable_card_values.append(6)
                        continue
            cc = playable_cards[playable_card_values.index(min(playable_card_values))]  # Playing the card
            del current_player.cards[current_player.cards.index(cc)]
            if len(current_player.cards) == 0:  # If game is over:
                break
            # Doing all special cards
            if cc.special_description == "skip":  # Skip
                if direction == "right":
                    current_player_index += 1
                    if current_player_index >= no_players:
                        current_player_index = 0
                if direction == "left":
                    current_player_index -= 1
                    if current_player_index < 0:
                        current_player_index = no_players - 1
            elif cc.special_description == "reverse":  # Reverse
                if direction == "right":
                    direction = "left"
                else:
                    direction = "right"
            elif cc.special_description == "wild":  # Wild
                # Choosing the card you have the most of
                cc = Card(color=statistics.mode([card.color for card in current_player.cards]))
            elif cc.special_description == "+4":  # +4
                cc = Card(color=statistics.mode([card.color for card in current_player.cards]))
                # Finding the next player
                temp_current_player_index = current_player_index
                if direction == "right":
                    temp_current_player_index += 1
                    if temp_current_player_index > no_players - 1:
                        temp_current_player_index = 0
                if direction == "left":
                    temp_current_player_index -= 1
                    if temp_current_player_index < 0:
                        temp_current_player_index = no_players - 1
                if len(deck) == 0:
                    create_deck()
                for i in range(4):  # Giving next player 4 cards
                    players[temp_current_player_index].cards.append(deck[0])
                    del deck[0]
                    if len(deck) == 0:
                        create_deck()
                # Skips the next player
                if direction == "right":
                    current_player_index += 1
                    if current_player_index >= no_players:
                        current_player_index = 0
                if direction == "left":
                    current_player_index -= 1
                    if current_player_index < 0:
                        current_player_index = no_players - 1
            elif cc.special_description == "+2":  # +2
                temp_current_player_index = current_player_index
                if direction == "right":
                    temp_current_player_index += 1
                    if temp_current_player_index > no_players - 1:
                        temp_current_player_index = 0
                if direction == "left":
                    temp_current_player_index -= 1
                    if temp_current_player_index < 0:
                        temp_current_player_index = no_players - 1
                if len(deck) == 0:
                    create_deck()
                for i in range(2):
                    players[temp_current_player_index].cards.append(deck[0])
                    del deck[0]
                    if len(deck) == 0:
                        create_deck()
                # Skips the next player
                if direction == "right":
                    current_player_index += 1
                    if current_player_index >= no_players:
                        current_player_index = 0
                if direction == "left":
                    current_player_index -= 1
                    if current_player_index < 0:
                        current_player_index = no_players - 1
        else:  # You don't have a card to play
            no_times_drew = 1
            if len(deck) == 0:
                create_deck()
            while find_playable_cards(cc=cc, single_card=deck[0]):  # While you can't play the card you drew
                no_times_drew += 1
                current_player.cards.append(deck[0])
                del deck[0]
                if len(deck) == 0:
                    create_deck()
            cc = deck[0]  # Playing the card
            del deck[0]
            if len(deck) == 0:
                create_deck()
        no_turns += 1
        # Changing player index
        if direction == "right":
            current_player_index += 1
            if current_player_index >= no_players:
                current_player_index = 0
        if direction == "left":
            current_player_index -= 1
            if current_player_index < 0:
                current_player_index = no_players-1
    return no_turns


def simulate(no_players, no_games):
    all_games = []
    for game in range(no_games):
        all_games.append(play_one_game(no_players))
    return "Average Number Of Turns: {}".format(round(statistics.mean(all_games)))


create_deck()
print(simulate(4, 100))

# This project follows the official UNO game rules (Which means no stacking +2/+4s), and is optimised to play the
# theoretical best move.
