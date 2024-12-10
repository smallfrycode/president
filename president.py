"""A program which can play the card game President."""

import re
import sys
from argparse import ArgumentParser
from random import choice


SUITS = ["Hearts", "Diamonds", "Spades", "Clubs"]
ROLES = ["President", "Vice President", "Neutral 1", "Neutral 2", "Neutral 3", "Vice Trash", "Trash"]
CARD_VALUES = ["3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A", "2"]


class Card:
    """Represents a card with a rank and suit and provides methods to compare cards.
    
    Attributes: 
        rank (str): The rank of the card (e.g 1, 2, 3, ..., Q, K, A).
        suit (str): The suit of the card (e.g Spades, Hearts, Diamonds, Clubs).
    """
    def __init__(self, rank, suit):
        """
        Primary Author: Ireland2004
        Techniques Demonstrated: N/A
        
        Initializes a card with a given rank and suit.
        
        Raises:
            ValueError: If the suit or rank is invalid.
            
        Side effects:
            Creates attributes: rank, suit.
        """
        if suit not in SUITS:
            raise ValueError("Invalid suit input")
        if rank not in CARD_VALUES:
            raise ValueError("Invalid rank input")

        self.rank = rank
        self.suit = suit
    
    def __gt__(self, other):
        """
        Primary Author: Ireland2004
        Techniques Demonstrated: Magic methods
        
        Compares card objects and checks to see if self > other.
        
        Args:
            other (Card): the card object we want to compare.
            
        Returns:
            bool: True if self > other, False otherwise.
        """
        return CARD_VALUES.index(self.rank) > CARD_VALUES.index(other.rank)
    
    def __eq__(self, other):
        """
        Primary Author: smallfrycode
        Techniques Demonstrated: N/A
        
        Compares card objects and checks if they are the same.
        
        Args:
            other (Card): the card object we want to compare.
            
        Returns:
            bool: True if 2 card objects are the same, False otherwise.
        """
        return self.rank == other.rank and self.suit == other.suit

    def validate(self, play, last_played):
        """
        Primary Author: Ireland2004
        Techniques Demonstrated: Generator expressions
        
        Validates a player's move in the card game.
        
        Args:
            play (list of Cards): The cards the player chose to play.
            last_played (list of Cards or None): The last cards that were played.
        
        Returns:
            bool: True if the move is valid, False if the move is invalid.
        """
        if last_played is None:
            if len(play) > 4 or len(play) < 0:
                return False
        else:
            if len(play) != len(last_played):
                return False
            first_rank = play[0].rank
            if not all(card.rank == first_rank for card in play):
                return False
            if not all(card > last_played[0] for card in play):
                return False

        return True
    
class Player:
    """Represents the player.
    
    Attributes:
        name (str): name of the player.
        hand (list): player's cards.
        role (str or None): player's role.
    """
    def __init__(self, name, hand):
        """
        Primary Author: smallfrycode
        Techniques Demonstrated: N/A
        
        Initializes a player.
        
        Args:
            name (str): the name of the player.
            hand (list): the player's hand, where each item is a card object.
            
        Side effects:
            Creates attributes: name, hand, role.
        """
        self.name = name
        self.hand = hand
        self.role = None
        
    def turn(self):
        """
        Primary Author: smallfrycode
        Techniques Demonstrated: N/A
        
        Returns a NotImplementedError because computer/player hasn't been established yet.
        """
        return NotImplementedError

class HumanPlayer(Player):
    """Represents the human player.
    
    Attributes:
        name (str): the player's name.
        hand (list): the player's hand.
        role (str or None): the player's role.
    """
    
    def __init__(self, name, hand):
        """
        Primary Author: andychen47
        Techniques Demonstrated: super()
        
        Initializes a HumanPlayer instance.
        
        Args:
        - name (str): The name of the player.
        - hand (list): A list representing the player's hand, where each item is a card object.
        
        The constructor calls the initializer of its parent class, Player.
        """
        super().__init__(name, hand)
    
    def turn(self, state):
        """
        Primary Author: andychen47
        Techniques Demonstrated: N/A
        
        Prompts the human player to select a card to play or skip their turn.
        
        Args:
            state (GameState): Info about the current state of the game.
            
        Side effects:
            prompts the user for an input.
            
        Raises:
            a ValueError if invalid input is given by player (i.e re-prompts the player for an input).
        
        Returns:
            The chosen card or None if the player decides to pass.
        """
        print(state)
        
        # Ask player for input
        choice = input("Enter the card values you want to play followed by first letter of suit (e.g., 'JH, JD, JS') or type 'pass' to pass: ").strip().upper()
        
        if choice == "PASS":
            return None
        
        def convert(value):
            """
            Primary Author: smallfrycode
            Techniques Demonstrated: Regular expressions
            
            converts a card typed from the terminal into a Card object.
            
            Args:
                value (str): the user's input
                
            Returns:
                a Card object.
                
            Raises:
                a ValueError if no valid card found.
            """
            regEx = r"""(?x)
                ^
                (?P<rank>\d+|J|Q|K|A)
                (?P<suit>D|S|H|C)$
            """
            match = re.search(regEx, value)
            if match:
                for suit in SUITS:
                    if suit[0] == match.group("suit"):
                        return Card(match.group("rank"), suit)
            raise ValueError
        
        try:
            selected = [convert(card) for card in choice.split(", ")]
            valid_cards = 0
            for card in selected:
                for hand_card in self.hand:
                    if card == hand_card:
                        valid_cards += 1
            if valid_cards == len(selected):
                return selected
            # attempt again if player did not put in cards they have in hand
            return self.turn(state)
        except ValueError:
            return self.turn(state)
        
class ComputerPlayer(Player):
    """Represents a computer player in the card game.
    
    Attributes:
        name (str): The player's name.
        hand (list): The player's hand, where each item is a card object.
    """
    def __init__(self, name, hand):
        """
        Primary Author: duckwookwon
        Techniques Demonstrated: N/A
        
        Initializes the computer player with a name and starting hand.
        
        Args:
            name (str): The player's name.
            hand (list): The player's hand, where each item is a card object.
            
        The constructor calls the initializer of the parent class, Player.
        """
        super().__init__(name, hand)

    def turn(self, state):
        """
        Primary Author: duckwookwon
        Techniques Demonstrated: use of a key function (min(); lambda)
        
        Chooses cards to play based on the last cards played.
        
        Args:
            state (GameState): Info about the current state of the game.
        
        Returns:
            list or None: A list of cards to play or None if no valid play.
        """
        last_played = state.last_played
        last_play_size = len(last_played) if last_played else 1

        def valid(card_rank):
            """
            Primary Author: duckwookwon
            Techniques Demonstrated: List comprehensions
            
            Finds a valid list of cards of the same rank to play, validated by the Card class.
            
            Args:
                card_rank (str): The rank of the card to use for forming a list.
            
            Returns:
                list or None: A valid list of cards if available, None otherwise.
            """
            group = [c for c in self.hand if c.rank == card_rank]
            # Check if the group is large enough and valid to match the last played list
            if len(group) >= last_play_size:
                play = group[:last_play_size]
                if group[0].validate(last_played=last_played, play=play):
                    return play
            return None

        # Find all valid card lists without creating duplicates
        playable_options = [
            valid_play for value in CARD_VALUES if (valid_play := valid(value))
        ]

        if playable_options:
            # Choose the list with the lowest card values
            selected_play = min(playable_options, key=lambda x: CARD_VALUES.index(next(iter(x)).rank))
            return selected_play
        else:
            return None

class GameState:
    """Provide information on the current state of the game.
    
    Attributes: 
        - players (list): A collection of all the players
        - last_played (list or None): The last card(s) that were played
        - current_player (Player): The person who is currently playing
        - out (list): all the players who have emptied their hand
    """
    
    def __init__(self, players, last_played, current_player, out):
        """
        Primary Author: kayetubal
        Techniques Demonstrated: N/A
        
        Initializes the GameState class.
        
        Args:
            - players (list): A collection of all the players as a list
            - last_played (list): The last card(s) which were played
            - current_player (Player): The person who is currently playing
            - out (list): all the players who have emptied their hand
            
        Side effects:
            Creates attributes: players, last_played, current_player, out
        """
        self.players = players
        self.last_played = last_played
        self.current_player = current_player
        self.out = out
        
    def __str__(self):
        """
        Primary Author: kayetubal
        Techniques Demonstrated: f-string containing expressions
        
        Shows an informal representation of the GameState.
        
        Returns:
            str: a string showing the current state of the game.
        """
        def find_unicode(suit):
            """
            Primary Author: kayetubal
            Techniques Demonstrated: Conditional expressions
            
            Determines the unicode depending on the suit of the card.
            
            Args:
                suit (str): The suit of the card.
            
            Returns:
                str: Unicode representation of the suit of the card. 
            """
            symbol = "\u2660" if suit == "Spades" else "\u2665" if \
                suit == "Hearts" else "\u2666" if suit == "Diamonds" \
                else "\u2663"
            return symbol
        
        # create a string representing the players of the game and their roles
        players_rep = "Current Players:\n"
        for player in self.players:
            players_rep += f"- {player.name} ({player.role})\n"

        # create string representing the last card(s) played on the table
        table_rep = ""
        if self.last_played:
            for card in self.last_played:
                table_rep += card.rank + find_unicode(card.suit)
                if card != self.last_played[-1]:
                    table_rep += ", "
        
        # create a string representing the hand of the current player 
        hand_rep = ""
        for card in self.current_player.hand:
            hand_rep += card.rank + find_unicode(card.suit)
            if card != self.current_player.hand[-1]:
                    hand_rep += ", "
            
        return f"\n{players_rep} \nTable: {table_rep} \n{self.current_player.name}'s Hand: {hand_rep}"
    
    def results(self):
        """
        Primary Author: smallfrycode
        Techniques Demonstrated: N/A
        
        Returns the results of the game.
        
        Returns:
            str: a string containing all result data of the game.
        """
        roles = ""
        for player in self.out:
            roles += f"{player.name}: {player.role}\n"
        return roles
    
class Game:
    """The game's main system.
    
    Attributes:
        - deck (list): a collection of all the cards in the deck
        - players (list): a collection of all the players
        - out (list): a collection of all the players who have emptied their hand
        - roles_left (list): a list of all the available roles which can be won during the game
        - current_player (Player): the person who is currently playing
        - last_played (list or None): the last card(s) which were played
    """
    def __init__(self, players):
        """
        Primary Author: smallfrycode
        Techniques Demonstrated: N/A
        
        Initializes the game.
        
        Args:
            players (list): a list of all player objects.
            
        Side effects:
            Creates attributes: deck, players, roles_left, out, current_player, last_played.
        """
        self.deck = []
        self.players = players
        self.roles_left = ROLES.copy()
        self.out = []
        self.current_player = None
        self.last_played = None    
        
    def shuffle(self):
        """
        Primary Author: smallfrycode
        Techniques Demonstrated: N/A
        
        Shuffles all the cards in the deck.
        
        Side effects:
            Changes the deck attribute of Game.
        """
        # add cards to deck
        unshuffled_deck = []
        for value in CARD_VALUES:
            for suit in SUITS:
                unshuffled_deck.append(Card(value, suit))
        
        # shuffle the deck
        while unshuffled_deck:
            chosen_card = choice(unshuffled_deck)
            self.deck.append(chosen_card)
            unshuffled_deck.remove(chosen_card)
        
    def deal(self):
        """
        Primary Author: smallfrycode
        Techniques Demonstrated: N/A
        
        Deals all the cards from deck to players.
        
        Side effects:
            - Changes the deck attribute of Game
            - Changes hand attributes of players
        """
        max_index = len(self.players) - 1
        index = 1
        while self.deck:
            player = self.players[index]
            index = index + 1 if index < max_index else 0
            player.hand.append(self.deck.pop())
            
        # organize player's cards
        for player in self.players:
            player.hand = sorted(player.hand, key=lambda card: CARD_VALUES.index(card.rank))
            
    def create_roles(self):
        """
        Primary Author: smallfrycode
        Techniques Demonstrated: N/A
        
        Creates the possible roles players can win.
        
        Side effects:
            Changes roles_left attribute of Game.
        """
        player_count = len(self.players)
        self.roles_left = {
            4: ["President", "Vice President", "Vice Trash", "Trash"],
            5: ["President", "Vice President", "Neutral 1", "Vice Trash", "Trash"],
            6: ["President", "Vice President", "Neutral 1", "Neutral 2", "Vice Trash", "Trash"],
            7: ROLES.copy()
        }[player_count]
        
    def last_card_bomb(self, last_play):
        """
        Primary Author: smallfrycode
        Techniques Demonstrated: N/A
        
        Checks to see if a player last played a bomb card.
        
        Returns:
            bool: True if last_play contains a Card object with the rank of 2, False otherwise.
        """
        for card in last_play:
            if card.rank == "2":
                return True
        return False
    
    def state(self):
        """
        Primary Author: smallfrycode
        Techniques Demonstrated: N/A
        
        Grabs the state of the game.
        
        Returns:
            a GameState object.
        """
        return GameState(self.players, self.last_played, self.current_player, self.out)
    
    def play(self, first_game):
        """
        Primary Author: smallfrycode
        Techniques Demonstrated: Composition of two custom classes
        
        Starts and progresses through the game.
        
        Args:
            first_game (bool): whether games have been previously played before while the program was running.
            
        Side effects:
            - Changes attributes of the Game Class, GameState Class, and Player Class
            - Prints results of the game as well as the game state
        """
        # order players by roles if not the first game
        if not first_game:
            self.players = sorted(self.out, key=lambda player: ROLES.index(player.role))
            self.out = []
            self.last_played = None
            
        # shuffle and deal cards
        self.shuffle()
        self.deal()
        
        # set up possible roles players can win (changes depending on amount of players)
        self.create_roles()
            
        # begin actual game
        skip_count = 0
        turn = 0
        while len(self.players) > 1:
            # start the game
            player = self.players[turn % len(self.players)]
            self.current_player = player
            # continue until valid response
            valid_response = False
            response = None
            while not valid_response:
                # check to make sure someone can play, if no one can reset
                if skip_count >= (len(self.players) - 1):
                    skip_count = 0
                    self.last_played = None
                    turn += (len(self.players) - 1)
                    break
                
                # response must be a list of card objects
                response = player.turn(self.state())
                if response is None:
                    valid_response = True
                    skip_count += 1
                    print(f"{player.name} has skipped their turn.")
                elif response[0].rank == CARD_VALUES[-1]:
                    skip_count = 0
                    self.last_played = None
                    for card in response:
                        player.hand.remove(card)
                    if player.hand: # player goes again if they don't have an empty hand
                        continue
                    valid_response = True
                elif response[0].validate(last_played=self.last_played, play=response):
                    self.last_played = response
                    for card in response:
                        player.hand.remove(card)
                    skip_count = 0
                    valid_response = True
                else:
                    print(f"Sorry {player.name}, that is not a valid play.")
            # add player to out list and give them proper role
            if not player.hand:
                if response and self.last_card_bomb(response):
                    player.role = self.roles_left.pop()
                else:
                    player.role = self.roles_left.pop(0)
                self.out.append(player)
                self.players.remove(player)
                print(f"{player.name} has emptied their hand and became {player.role}")
            # stop the game when one player is left
            if len(self.players) <= 1:
                break
            
            # iterate through list of players
            turn += 1
        
        last_player = self.players.pop()
        last_player.role = self.roles_left.pop()
        self.out.append(last_player)
        print(f"\nPresident has concluded, here are the results:\n{self.state().results()}")

def main(players, computers):
    """
    Primary Author: andychen47
    Techniques Demonstrated: N/A
    
    Sets up and starts the card game President with human and computer players (max players = len(ROLES)).
    
    Args:
        players (list): list of human player names.
        computers (int): number of computer players.
        
    Side effects:
        Creates Player objects, a Game object, and prompts user for input.
    """
    
    max_players = len(ROLES)
    min_players = max_players - 3
    total_requested_players = len(players) + computers

    # Adjust player count if exceeding maximum
    if total_requested_players > max_players:
        if len(players) >= max_players:
            players = players[:max_players]
            computers = 0
        else:
            computers = max_players - len(players)
    elif total_requested_players < min_players:
        computers = min_players - len(players)

    total_players = []

    # Add human players from command-line arguments
    for name in players:
        total_players.append(HumanPlayer(name=name, hand=[]))

    # Add computer players
    for i in range(computers):
        total_players.append(ComputerPlayer(name=f"Computer {i + 1}", hand=[]))

    # Initialize the game instance
    game = Game(total_players)
    
    # Start the game
    first_game = True
    while True:
        game.play(first_game)
        first_game = False  # Only the first round is marked as `first_game`
        play_again = input("Play another round? (yes/no): ").strip().lower()
        if play_again != 'yes':
            break
        
def parse_args(arglist):
    """
    Primary Author: andychen47
    Techniques Demonstrated: ArgumentParser() class
    
    Parses arguments in the terminal.
    
    Args:
        arglist (list): arguments from the terminal.
    
    Returns:
        a namespace of human players and amount of computers.
    """
    parser = ArgumentParser(description="President card game.")
    parser.add_argument('players', nargs='+', help='List of human player names')
    parser.add_argument('-c', '--computers', type=int, help='Number of computer players', default=0)
    return parser.parse_args(arglist)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.players, args.computers)