import random

class DominionCard:
    def __init__(self, name, card_type, cost, actions=None, buys=None, coins=None, vp=None):
        self.name = name
        self.card_type = card_type
        self.cost = cost
        self.actions = actions or 0
        self.buys = buys or 0
        self.coins = coins or 0
        self.vp = vp or 0

    def __str__(self):
        return f"{self.name} ({self.card_type}) - Cost: {self.cost}, Actions: {self.actions}, Buys: {self.buys}, Coins: {self.coins}, VP: {self.vp}"

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
        num_to_draw = 5
        if len(self.deck) < num_to_draw:
            self.shuffle_discard_into_deck()
        self.hand = self.deck[:num_to_draw]
        self.deck = self.deck[num_to_draw:]

    def shuffle_discard_into_deck(self):
        random.shuffle(self.discard_pile)
        self.deck += self.discard_pile
        self.discard_pile = []

    def play_action_card(self, card):
        self.actions -= 1
        self.coins += card.coins
        self.buys += card.buys
        self.draw_hand()

    def buy_card(self, card, supply):
        if card.cost <= self.coins and card.name in supply and supply[card.name] > 0:
            self.coins -= card.cost
            self.buys -= 1
            self.discard_pile.append(card)
            supply[card.name] -= 1
            return True
        return False

    def end_turn(self):
        self.discard_pile += self.hand
        self.hand = []
        self.actions = 1
        self.buys = 1
        self.coins = 0

class DominionGame:
    def __init__(self, players, kingdom_cards):
        self.players = [DominionPlayer(player) for player in players]
        self.supply = self.setup_supply(kingdom_cards)

    def setup_supply(self, kingdom_cards):
        supply = {}
        for card in kingdom_cards:
            supply[card.name] = card
        return supply

    def play(self):
        game_over = False
        while not game_over:
            for player in self.players:
                print(f"\n{player.name}'s turn:")
                player.draw_hand()

                while player.actions > 0 or player.buys > 0:
                    print(f"\n{player.name}'s hand: {[card.name for card in player.hand]}")
                    print(f"Available actions: {player.actions}, Available buys: {player.buys}, Available coins: {player.coins}")

                    action_card = input("Play an action card (or 'skip'): ")
                    if action_card.lower() == 'skip':
                        break

                    if action_card in [card.name for card in player.hand if card.card_type == 'Action']:
                        player.play_action_card(self.supply[action_card])

                while player.buys > 0:
                    print(f"\n{player.name}'s hand: {[card.name for card in player.hand]}")
                    print(f"Available buys: {player.buys}, Available coins: {player.coins}")

                    buy_card = input("Buy a card (or 'skip'): ")
                    if buy_card.lower() == 'skip':
                        break

                    if buy_card in self.supply and player.buy_card(self.supply[buy_card], self.supply):
                        print(f"{player.name} bought {buy_card}.")

                player.end_turn()

                if self.is_game_over():
                    game_over = True
                    break

    def is_game_over(self):
        # Add conditions for game over (e.g., Province pile is empty)
        return False

if __name__ == "__main__":
    # Define Kingdom Cards for the game
    kingdom_cards = [
        DominionCard("Smithy", "Action", 4, actions=3),
        DominionCard("Village", "Action", 3, actions=2, buys=1),
        # Add more kingdom cards as needed
    ]

    players = ["Player1", "Player2"]  # Add more players as needed
    dominion_game = DominionGame(players, kingdom_cards)
    dominion_game.play()
