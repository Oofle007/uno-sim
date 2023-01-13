import random
import statistics


class Player:
    def __init__(self, multipliers, random_card_choosing=False):
        self.cards = []
        self.multipliers = multipliers
        self.random_choosing = random_card_choosing


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
    attributes = ['color', 'number', 'special_description']
    if current_player:
        for c in current_player.cards:  # Iterates over all of the current player's cards
            for i in range(0, len(attributes)):  # Iterates through all attributes
                i = attributes[i]
                if getattr(c, i) is getattr(cc, i) and getattr(cc, i) is not None:
                    playable_cards.append(c)
                    continue
        return playable_cards
    else:
        for i in range(0, len(attributes)):  # Iterates through all attributes
            i = attributes[i]
            if getattr(single_card, i) is getattr(cc, i) and getattr(single_card, i) is not None:
                playable_cards.append(single_card)
                continue
        return len(playable_cards) == 0


def play_one_game(no_players, players, random_ai):
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
    if len(deck) == 0:
        create_deck()
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
            if current_player.random_choosing:
                playable_card_values = []  # Keeps track of how good each card is
                # V2 COST MULTIPLIERS:
                # most_color = FIND HOW MANY OF THAT COLOR APPEAR IN HAND
                # Random Card: (ratio_in_deck + most_color) * MULTIPLIER
                # Special Card: (ratio_in_deck + next_player_amount_cards + most_color) * MULTIPLIER
                # Wild: DON'T PLAY IT
                # +4: (ratio_in_deck + next_player_amount_cards) * MULTIPLIER
                for c in playable_cards:

                    if not c.special_description:  # Random card
                        ratio_in_deck = 0  # work in progress
                        most_color = [c.color for c in current_player.cards].count(statistics.mode([card.color for card in current_player.cards]))
                        playable_card_values.append((ratio_in_deck + most_color) * current_player.multipliers[0])
                        continue

                    elif c.special_description == "wild":
                        playable_card_values.append(current_player.multipliers[1])

                    elif c.special_description == "reverse":
                        temp_current_player_index = current_player_index
                        if direction == "right":
                            temp_current_player_index += 1
                            if temp_current_player_index > no_players - 1:
                                temp_current_player_index = 0
                        else:
                            temp_current_player_index -= 1
                            if temp_current_player_index < 0:
                                temp_current_player_index = no_players - 1
                        next_player_cards = len(players[temp_current_player_index].cards)
                        playable_card_values.append(next_player_cards * current_player.multipliers[2])

                    elif c.special_description == "skip":
                        temp_current_player_index = current_player_index
                        if direction == "right":
                            temp_current_player_index += 1
                            if temp_current_player_index > no_players - 1:
                                temp_current_player_index = 0
                        else:
                            temp_current_player_index -= 1
                            if temp_current_player_index < 0:
                                temp_current_player_index = no_players - 1
                        next_player_cards = len(players[temp_current_player_index].cards)
                        playable_card_values.append(next_player_cards * current_player.multipliers[3])

                    elif c.special_description == "+2":
                        temp_current_player_index = current_player_index
                        if direction == "right":
                            temp_current_player_index += 1
                            if temp_current_player_index > no_players - 1:
                                temp_current_player_index = 0
                        else:
                            temp_current_player_index -= 1
                            if temp_current_player_index < 0:
                                temp_current_player_index = no_players - 1
                        next_player_cards = len(players[temp_current_player_index].cards)
                        playable_card_values.append(next_player_cards * current_player.multipliers[4])

                    elif c.special_description == "+4":
                        playable_card_values.append(current_player.multipliers[5])

                cc = playable_cards[playable_card_values.index(min(playable_card_values))]  # Playing the card
            else:
                cc = playable_cards[random.randint(0, len(playable_cards)-1)]  # Playing the card
            del current_player.cards[current_player.cards.index(cc)]
            if len(current_player.cards) == 0:  # If game is over:
                break

            # Playing special card
            if cc.special_description == "skip":  # Skip
                if direction == "right":
                    current_player_index += 1
                    if current_player_index >= no_players:
                        current_player_index = 0
                else:
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
                else:
                    temp_current_player_index -= 1
                    if temp_current_player_index < 0:
                        temp_current_player_index = no_players - 1
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
                else:
                    current_player_index -= 1
                    if current_player_index < 0:
                        current_player_index = no_players - 1
            elif cc.special_description == "+2":  # +2
                temp_current_player_index = current_player_index
                if direction == "right":
                    temp_current_player_index += 1
                    if temp_current_player_index > no_players - 1:
                        temp_current_player_index = 0
                else:
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
                else:
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
        else:
            current_player_index -= 1
            if current_player_index < 0:
                current_player_index = no_players-1

    for i in players:
        if i.random_choosing:
            if players[current_player_index].random_choosing:
                return "Random Won!"
            else:
                return "AI Won!"
    return no_turns, players[current_player_index].multipliers


def simulate(no_players, no_games, random_choosing):
    all_games = []
    for game in range(no_games):
        if not random_choosing:
            players = [Player(multipliers=[1.750000000000001, -0.4500000000000003, -2.589999999999989, -3.48999999999997, -0.5500000000000005, -0.9100000000000009]) for i in range(no_players)]
        else:
            players = [Player(multipliers=[1.750000000000001, -0.4500000000000003, -2.589999999999989, -3.48999999999997, -0.5500000000000005, -0.9100000000000009]) for i in range(no_players-1)]
            players.append(Player(multipliers=[0, 0, 0, 0, 0, 0], random_card_choosing=True))
        all_games.append(play_one_game(no_players, players, False)[0])
        print(play_one_game(no_players, players, False))


def find_multipliers(no_players, generations):
    random_card = 0
    wild = 0
    reverse = 0
    skip = 0
    plus2 = 0
    plus4 = 0
    game_winning_multipliers = None
    for generation in range(generations):
        players = [Player(multipliers=[random_card, wild, reverse, skip, plus2, plus4]) for i in range(no_players)]
        game_winning_multipliers = play_one_game(no_players, players, False)[1]
        random_card = game_winning_multipliers[0] + [-0.01, 0.01][random.randint(0, 1)]
        wild = game_winning_multipliers[1] + [-0.01, 0.01][random.randint(0, 1)]
        reverse = game_winning_multipliers[2] + [-0.01, 0.01][random.randint(0, 1)]
        skip = game_winning_multipliers[3] + [-0.01, 0.01][random.randint(0, 1)]
        plus2 = game_winning_multipliers[4] + [-0.01, 0.01][random.randint(0, 1)]
        plus4 = game_winning_multipliers[5] + [-0.01, 0.01][random.randint(0, 1)]
        print("Generation: {}  {}%".format(generation+1, generation/generations * 100))
    return game_winning_multipliers


print(simulate(2, 1, True))
# print(find_multipliers(10000, 100000))

# This project follows the official UNO game rules (Which means no stacking +2/+4s), and is optimised to play the
# theoretical best move.
