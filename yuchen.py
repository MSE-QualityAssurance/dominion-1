import random

class DominionCard:
    def __init__(self, name, card_type, cost, actions=0, buys=0, coins=0, vp=0, draw=0):
        self.name = name
        self.card_type = card_type
        self.cost = cost
        self.actions = actions
        self.buys = buys
        self.coins = coins
        self.vp = vp
        self.draw = draw

    def __str__(self):
        return f"{self.name} ({self.card_type}) - Cost: {self.cost}, Actions: {self.actions}, Buys: {self.buys}, Coins: {self.coins}, VP: {self.vp}, Draw: {self.draw}"

class DominionPlayer:
    def __init__(self, name):
        self.name = name
        self.deck = self.initialize_deck()
        self.hand = []
        self.discard_pile = []
        self.actions = 1
        self.buys = 1
        self.coins = 0

    def initialize_deck(self):
        starting_deck = [DominionCard("Copper", "Treasure", 0, coins=1) for _ in range(7)]
        starting_deck += [DominionCard("Estate", "Victory", 2, vp=1) for _ in range(3)]
        random.shuffle(starting_deck)
        return starting_deck

    def draw_hand(self):
        while len(self.hand) < 5:
            self.draw_card()

    def draw_card(self):
        if len(self.deck) == 0 and len(self.discard_pile) > 0:
            self.shuffle_discard_into_deck()
        if len(self.deck) > 0:
            self.hand.append(self.deck.pop(0))

    def shuffle_discard_into_deck(self):
        self.deck = self.discard_pile
        random.shuffle(self.deck)
        self.discard_pile = []

    def play_action_card(self, card):
        if self.actions <= 0:
            print(f"No actions available to play {card.name}.")
            return False
        if card not in self.hand:
            print(f"{card.name} is not in your hand.")
            return False
        self.actions -= 1
        self.coins += card.coins
        self.buys += card.buys
        for _ in range(card.draw):
            self.draw_card()
        self.hand.remove(card)
        self.discard_pile.append(card)
        print(f"Played {card.name}.")
        return True

    def buy_card(self, card, supply):
        if self.buys <= 0:
            print("No buys available.")
            return False
        if card.cost > self.coins:
            print(f"Not enough coins to buy {card.name}.")
            return False
        if supply[card.name] <= 0:
            print(f"{card.name} is not available in the supply.")
            return False
        self.coins -= card.cost
        self.buys -= 1
        self.discard_pile.append(card)
        supply[card.name] -= 1
        print(f"Bought {card.name}.")
        return True

    def end_turn(self):
        self.discard_pile += self.hand
        self.hand = []
        self.actions = 1
        self.buys = 1
        self.coins = 0
        self.draw_hand()

class DominionGame:
    def __init__(self, players, kingdom_cards):
        self.players = [DominionPlayer(player) for player in players]
        self.supply = self.setup_supply(kingdom_cards)
        self.game_over = False

    def setup_supply(self, kingdom_cards):
        supply = {card.name: 10 for card in kingdom_cards}  # Assuming 10 copies of each kingdom card
        # Add basic cards
        supply.update({"Copper": 60, "Silver": 40, "Gold": 30, "Estate": 24, "Duchy": 12, "Province": 12})
        return supply

    def play(self):
        while not self.game_over:
            for player in self.players:
                print(f"\n{player.name}'s turn:")
                player.draw_hand()
