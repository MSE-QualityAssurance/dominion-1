import random


class DominionCard:
    def __init__(
        self, name, card_type, cost, actions=None, buys=None, coins=None, vp=None
    ):
        """
        Represents a Dominion card with various attributes.

        Parameters:
        - name (str): The name of the card.
        - card_type (str): The type of the card (e.g., "Action", "Treasure", "Victory").
        - cost (int): The cost of the card in coins.
        - actions (int): The number of additional actions the card provides.
        - buys (int): The number of additional buys the card provides.
        - coins (int): The number of additional coins the card provides.
        - vp (int): The number of Victory Points the card is worth (for Victory cards).

        Note: Some parameters default to None and are optional for certain card types.
        """
        self.name = name
        self.card_type = card_type
        self.cost = cost
        self.actions = actions or 0
        self.buys = buys or 0
        self.coins = coins or 0
        self.vp = vp or 0

    def __str__(self):
        """
        String representation of the card, including its name, type, and attributes.
        """
        return f"{self.name} ({self.card_type}) - Cost: {self.cost}, Actions: {self.actions}, Buys: {self.buys}, Coins: {self.coins}, VP: {self.vp}"


class DominionPlayer:
    def __init__(self, name):
        """
        Represents a player in the Dominion game.

        Parameters:
        - name (str): The name of the player.
        """
        self.name = name
        self.deck = self.initialize_deck()
        self.hand = []
        self.discard_pile = []
        self.actions = 1
        self.buys = 1
        self.coins = 0

    def initialize_deck(self):
        """
        Initializes the player's deck with the starting cards (Copper and Estate).
        """
        starting_deck = [
            DominionCard("Copper", "Treasure", 0, coins=1) for _ in range(7)
        ]
        starting_deck += [DominionCard("Estate", "Victory", 2, vp=1) for _ in range(3)]
        random.shuffle(starting_deck)
        return starting_deck

    def draw_hand(self):
        """
        Draws a hand of 5 cards from the player's deck, shuffling the discard pile if necessary.
        """
        num_to_draw = 5
        if len(self.deck) < num_to_draw:
            self.shuffle_discard_into_deck()
        self.hand = self.deck[:num_to_draw]
        self.deck = self.deck[num_to_draw:]

    def shuffle_discard_into_deck(self):
        """
        Shuffles the discard pile into the deck.
        """
        random.shuffle(self.discard_pile)
        self.deck += self.discard_pile
        self.discard_pile = []

    def play_action_card(self, card):
        """
        Plays an action card, resolving its effects.

        Parameters:
        - card (DominionCard): The action card to be played.
        """
        self.actions -= 1
        self.coins += card.coins
        self.buys += card.buys
        self.draw_hand()

    def buy_card(self, card, supply):
        """
        Buys a card from the supply, adding it to the player's discard pile.

        Parameters:
        - card (DominionCard): The card to be bought.
        - supply (dict): The supply of available cards.

        Returns:
        - bool: True if the card was successfully bought, False otherwise.
        """
        if card.cost <= self.coins and card.name in supply and supply[card.name] > 0:
            self.coins -= card.cost
            self.buys -= 1
            self.discard_pile.append(card)
            supply[card.name] -= 1
            return True
        return False

    def end_turn(self):
        """
        Ends the player's turn, moving cards from the hand to the discard pile and resetting turn attributes.
        """
        self.discard_pile += self.hand
        self.hand = []
        self.actions = 1
        self.buys = 1
        self.coins = 0


class DominionGame:
    def __init__(self, players, num_kingdom_cards=10):
        """
        Represents a Dominion game with a supply of cards and a list of players.

        Parameters:
        - players (list): A list of DominionPlayer objects.
        - num_kingdom_cards (int): The number of different Action cards to use in the game.
        """
        self.players = players
        self.num_players = len(players)
        self.supply = self.initialize_supply(num_kingdom_cards)
        self.trash = []
        self.turn = 0
        self.game_over = False

    def initialize_supply(self, num_kingdom_cards):
        """
        Initializes the supply of cards for the game, using the base set and a random selection of Action cards.

        Parameters:
        - num_kingdom_cards (int): The number of different Action cards to use in the game.

        Returns:
        - dict: A dictionary mapping card names to the number of copies available in the supply.
        """
        supply = {}
        # Add the basic cards (Copper, Silver, Gold, Estate, Duchy, Province, Curse)
        supply["Copper"] = 60 - (self.num_players * 7)
        supply["Silver"] = 40
        supply["Gold"] = 30
        if self.num_players == 2:
            supply["Estate"] = 8
            supply["Duchy"] = 8
            supply["Province"] = 8
            supply["Curse"] = 10
        elif self.num_players == 3:
            supply["Estate"] = 12
            supply["Duchy"] = 12
            supply["Province"] = 12
            supply["Curse"] = 20
        elif self.num_players == 4:
            supply["Estate"] = 12
            supply["Duchy"] = 12
            supply["Province"] = 12
            supply["Curse"] = 30
        else:
            raise ValueError("Invalid number of players")

        # Add a random selection of Action cards from the base set
        base_action_cards = [
            DominionCard("Cellar", "Action", 2, actions=1),
            DominionCard("Chapel", "Action", 2),
            DominionCard("Moat", "Action-Reaction", 2, coins=2),
            DominionCard("Harbinger", "Action", 3, actions=1, coins=1),
            DominionCard("Merchant", "Action", 3, actions=1, coins=1),
            DominionCard("Vassal", "Action", 3, coins=2),
            DominionCard("Village", "Action", 3, actions=2, coins=1),
            DominionCard("Workshop", "Action", 3),
            DominionCard("Bureaucrat", "Action-Attack", 4),
            DominionCard("Gardens", "Victory", 4),
            DominionCard("Militia", "Action-Attack", 4, coins=2),
            DominionCard("Moneylender", "Action", 4),
            DominionCard("Poacher", "Action", 4, actions=1, coins=1),
            DominionCard("Remodel", "Action", 4),
            DominionCard("Smithy", "Action", 4, coins=3),
            DominionCard("Throne Room", "Action", 4),
            DominionCard("Bandit", "Action-Attack", 5),
            DominionCard("Council Room", "Action", 5, buys=1, coins=4),
            DominionCard("Festival", "Action", 5, actions=2, buys=1, coins=2),
            DominionCard("Laboratory", "Action", 5, actions=1, coins=2),
            DominionCard("Library", "Action", 5),
            DominionCard("Market", "Action", 5, actions=1, buys=1, coins=1),
            DominionCard("Mine", "Action", 5),
            DominionCard("Sentry", "Action", 5, actions=1, coins=1),
            DominionCard("Witch", "Action-Attack", 5, coins=2),
            DominionCard("Artisan", "Action", 6),
        ]
        random.shuffle(base_action_cards)
        selected_action_cards = base_action_cards[:num_kingdom_cards]
        for card in selected_action_cards:
            supply[card.name] = 10

        return supply

    def get_card_by_name(self, name):
        """
        Returns a DominionCard object by its name, or None if not found.

        Parameters:
        - name (str): The name of the card.

        Returns:
        - DominionCard or None: The card object or None if not found.
        """
        for card in self.supply.keys():
            if card == name:
                return DominionCard(
                    card,
                    self.supply[card].card_type,
                    self.supply[card].cost,
                    self.supply[card].actions,
                    self.supply[card].buys,
                    self.supply[card].coins,
                    self.supply[card].vp,
                )
        return None

    def get_current_player(self):
        """
        Returns the current player based on the turn number.

        Returns:
        - DominionPlayer: The current player object.
        """
        return self.players[self.turn % self.num_players]

    def start_game(self):
        """
        Starts the game by drawing a hand for each player and printing the supply.
        """
        for player in self.players:
            player.draw_hand()
        print("The game has started. Here is the supply of cards:")
        for card, count in self.supply.items():
            print(f"{card}: {count}")
        print()

    def play_turn(self):
        """
        Plays a turn for the current player, allowing them to play Action cards, buy cards, and end their turn.
        """
        player = self.get_current_player()
        print(f"It is {player.name}'s turn.")
        print(f"Your hand: {', '.join(card.name for card in player.hand)}")
        print(f"Actions: {player.actions}, Buys: {player.buys}, Coins: {player.coins}")
        print()

        # Action phase: the player can play one Action card per action
        while player.actions > 0:
            action_card = input(
                "Enter the name of an Action card you want to play, or 'skip' to skip the action phase: "
            )
            if action_card == "skip":
                break
            else:
                card = self.get_card_by_name(action_card)
                if (
                    card is not None
                    and card.card_type.startswith("Action")
                    and card in player.hand
                ):
                    player.play_action_card(card)
                    print(f"You played {card.name}.")
                    print(
                        f"Actions: {player.actions}, Buys: {player.buys}, Coins: {player.coins}"
                    )
                    print()
                else:
                    print(
                        "Invalid card. Please enter a valid Action card from your hand."
                    )
                    print()

        # Buy phase: the player can buy one card per buy
        while player.buys > 0:
            buy_card = input(
                "Enter the name of a card you want to buy, or 'skip' to skip the buy phase: "
            )
            if buy_card == "skip":
                break
            else:
                card = self.get_card_by_name(buy_card)
                if card is not None and player.buy_card(card, self.supply):
                    print(f"You bought {card.name}.")
                    print(f"Buys: {player.buys}, Coins: {player.coins}")
                    print()
                else:
                    print(
                        "Invalid card. Please enter a valid card from the supply that you can afford."
                    )
                    print()

        # End phase: the player discards their hand and draws a new one
        player.end_turn()
        player.draw_hand()
        print(f"You ended your turn.")
        print()

        # Check if the game is over
        self.check_game_over()

        # Increment the turn number
        self.turn += 1

    def check_game_over(self):
        """
        Checks if the game is over by counting the empty piles in the supply and the availability of Province cards.

        Sets the game_over attribute to True if the game is over, and prints the winner and their score.
        """
        empty_piles = 0
        for card, count in self.supply.items():
            if count == 0:
                empty_piles += 1
                if card == "Province":
                    # The game is over if all Province cards are gone
                    self.game_over = True
                    break
        # The game is also over if three or more piles are empty
        if empty_piles >= 3:
            self.game_over = True

        if self.game_over:
            print("The game is over.")
            # Calculate the scores for each player
            scores = {}
            for player in self.players:
                score = 0
                # Count the Victory Points in the player's deck, hand, and discard pile
                for card in player.deck + player.hand + player.discard_pile:
                    if card.card_type == "Victory" or card.card_type == "Curse":
                        score += card.vp
                    # Special case for Gardens: worth 1 VP per 10 cards in the deck
                    if card.name == "Gardens":
                        score += (
                            len(player.deck)
                            + len(player.hand)
                            + len(player.discard_pile)
                        ) // 10
                scores[player.name] = score

            # Find the winner
            max_score = max(scores.values())
            winners = [player for player, score in scores.items() if score == max_score]
            if len(winners) == 1:
                # There is a single winner
                winner = winners[0]
                print(f"The winner is {winner} with {max_score} points.")
            else:
                # There is a tie
                print(
                    f"There is a tie between {', '.join(winners)} with {max_score} points each."
                )


if __name__ == "__main__":
    player_names = ["Alice", "Bob", "Charlie", "David"]

    # Create a list of player objects
    players = [DominionPlayer(name) for name in player_names]

    # Create a game object with four players and ten kingdom cards
    game = DominionGame(players, 10)

    # Start the game
    game.start_game()

    # Play the game until it is over
    while not game.game_over:
        game.play_turn()
