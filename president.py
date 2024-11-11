"""A program which can play the card game President."""
import argparse

unique_ranks = {"ace": 14, "king": 13, "queen": 12, "jack": 11}
valid_ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10]
valid_suits = ["hearts", "diamonds", "spades", "clubs"]
ROLES = ["President", "Vice President", "Neutral", "Vice Trash", "Trash"]

class Cards:
    """Represents a card with a rank and suit and provides methods to compare cards.
    
    Attributes: 
        rank (str or int): The rank of the card (either a face card or a numeric value).
        suit (str): The suit of the card.
    """
    def __init__(self, rank, suit):
        """Initializes a card with a given rank and suit.
        
        Raises:
            ValueError: If the suit or rank is invalid.
        """
        if suit not in valid_suits:
            raise ValueError("Invalid suit input")
        if rank not in unique_ranks and rank not in valid_ranks:
            raise ValueError("Invalid rank input")
        
        self.rank = rank
        self.suit = suit
        self.rank_value = unique_ranks.get(rank, rank)
        
    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
    def __lt__(self, other):   
        return self.rank_value < other.rank_value
    
    def __ge__(self, other):
        return self.rank_value >= other.rank_value

def valid_play(current_played, last_played, player):
    """Validates a player's move in the card game. 
    ***I wanted to include this function to illustrate how it will work in the final game***
    
    Args:
        current_played (Cards): The card the player chose to play.
        last_played (Cards): The last card that was played.
        player (str): The player's name.
    
    Returns: 
        str: A message about the outcome of the player's move.
    """
    if len(current_played) != len(last_played):
        return f"{player}, you must play {len(last_played)} card(s) to match the previous play"
    
    current_suit = list(current_played)[0].suit
    if not all(card.suit == current_suit for card in current_played):
        return f"{player}, all cards must be of the same suit"
    if not all(card.rank_value > max(card.rank_value for card in last_played) for card in current_played):
        return f"{player}, your cards are not all greater than the last played cards"
    if len(current_played) > 4:
        return f"{player}, you cannot place more than 4 cards of a kind!"
    
    count = len(current_played)
    rank = list(current_played)[0].rank
    suit = list(current_played)[0].suit
    card_text = f"{count} {rank} of {suit}" if count > 1 else f"an {rank} of {suit}"
    
    return f"{player} played {card_text}"

class HumanPlayer(Player):
    """
    Represents the human player in the card game.
    Inherits from the Player class and allows for human interaction during each turn.
    Prompts the user to play a valid card or skip their turn.
    """
    
    def __init__(self, name, hand):
        """
        Initializes a HumanPlayer instance.
        Parameters:
        - name (str): The name of the player.
        - hand (list of int): A list representing the player's hand, where each item is a card value.
        
        The constructor calls the initializer of the parent Player class.
        """
        super().__init__(name, hand)
    
    def take_turn(self, game_state):
        """
        Prompts the human player to select a card to play or skip their turn.
        
        - game_state: Info about the last card played and whose turn it is.
        
        Returns:
        - The chosen card or 'skip' if the player decides not to play.
        """
        
        last_played = game_state.get_last_card_played()
        last_play_size = len(last_played) if last_played != "skip" else 1  # Minimum set size
        
        # Find sets of playable cards of the same rank larger than or equal to the last played set
        playable_sets = [
            {card for card in self.hand if card.rank_value == value} 
            for value in set(card.rank_value for card in self.hand)
            if len([card for card in self.hand if card.rank_value == value]) >= last_play_size and 
               (not last_played or max([card.rank_value for card in self.hand if card.rank_value == value]) > max(card.rank_value for card in last_played))
        ]
        
        if playable_sets:
            while True:
                # Ask player for input
                choice = input("Enter the ranks of cards you want to play (e.g., '3 3 3') or type 'pass' to pass: ")
                
                if choice.strip().lower() == "pass":
                    return "skip"
                
                try:
                    selected_ranks = list(map(int, choice.split()))
                    selected_cards = {card for card in self.hand if card.rank_value in selected_ranks}
                    
                    # Check if the chosen set matches any playable set
                    if selected_cards in playable_sets and len(selected_cards) == last_play_size:
                        for card in selected_cards:
                            self.hand.remove(card)
                        return selected_cards
                    else:
                        print("Invalid selection. Ensure your set matches the size and rank requirements.")
                except ValueError:
                    print("Invalid input. Please enter numeric card ranks separated by spaces.")
        # Automatically skip if no playable sets
        return "skip"
        
class ComputerPlayer(Player):
    """Represents a computer player in the card game.
    
    Automates choosing cards to play during the game.
    
    Attributes:
        name (str): The player's name.
        hand (list of Card): The player's current cards.
    """
    def __init__(self, name, hand):
        """Initializes the computer player with a name and starting hand.
        
        Args:
            name (str): The player's name.
            hand (list of Card): The player's current cards.
        """
        super().__init__(name, hand)

    def take_turn(self, last_played):
        """Chooses cards to play based on the last cards played.
        
        Args:
            last_played (set): The last cards that were played in the game.
        
        Returns:
            set: A set of cards to play, or 'skip' if no valid play.
        
        Effects:
            - Updates the player's hand by removing played cards.
            - Returns the selected card set or a skip action.
        """
        last_play_size = len(last_played)

        def valid_num(card):
            """Finds a valid set of cards of the same rank to play, validated by the Card class.
            
            Args:
                card (int): The value of the card to use for forming a set.
            
            Returns:
                set or None: A valid set of cards if available, None otherwise.
            """
            group = list({c for c in self.hand if c.value == card.value})[:last_play_size]

            # Check if the group is large enough and valid to match the last played set
            if len(group) == last_play_size:
                if Card.validate(last_played=last_played, play=set(group)):
                    return set(group)
            
            return None

        # Define a constant list of card values to iterate over
        CARD_VALUES = sorted(set(c.value for c in self.hand))

        # Find all valid card sets without creating duplicates
        playable_options = [
            valid_set for card in self.hand if (valid_set := valid_num(card))
        ]

        if playable_options:
            # Choose the set with the lowest card values
            selected_set = min(playable_options, key=lambda x: min(card.value for card in x))

            # Remove chosen cards from the hand
            for card in selected_set:
                self.hand.remove(card)
            
            return selected_set
        else:
            return "skip"

class GameState:
    """ Provide information on the current state of the game.
    
    Attributes: 
        players (list): A collection of all the players as a list
        last_played (set): The last card(s) that were played.
        current_player (Player): The person who is currently playing as a Player object.
    """
    
    def __init__(self, players, last_played, current_player):
        """ Initializes the GameState class.
        
        Args:
            players (list): A collection of all the players as a list.
            last_played (set): The last card(s) which were played as a set.
            current_player (Player): The person who is currently playing as a Player object.
        """
        self.players = players
        self.last_played = last_played
        self.current_player = current_player
        
    def __str__(self):
        def find_unicode(suit):
            """ Determines the unicode depending on the suit of the card.
            
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
        for card in self.last_played:
            table_rep += card.rank + find_unicode(card.suit)
        
        # create a string representing the hand of the current player 
        hand_rep = ""
        for card in self.current_player.hand:
            hand_rep += card.rank + find_unicode(card.suit)
            
        return f"{players_rep} \nTable: {table_rep} \nYour Hand: {hand_rep}"
    
class Game:
    """The game's main system.
    
    Attributes:
        deck (list): a collection of all the cards in the deck as a list
        players (list): a collection of all the players as a list
        out (list): a collection of all the players who have emptied their hand as a list
        roles_left (list): a list of all the available roles which can be won during the game
        current_player (Player): the person who is currently playing as a Player object
        last_played (set): the last card(s) which were played as a set
    """
    def __init__(self, players):
        self.deck = []
        self.players = players
        self.roles_left = ROLES.copy()
        self.out = []
        self.current_player = None
        self.last_played = None
    
    def play(self, first_game):
        """Starts and progresses through the game.
        
        Args:
            first_game (bool): whether games have been previously played before while the program was running as a boolean
            
        Side effects:
            - Changes attributes of the Game Class, GameState Class, and Player Class
            - Prints results of the game as well as the game state
        """
        # shuffle and deal cards
        self.shuffle()
        self.deal()
        
        # set up possible roles players can win (changes depending on amount of players)
        self.create_roles()
        
        # order players by roles if not the first game
        if not first_game:
            self.players = sorted(self.players, key=lambda player: ROLES.index(player.role))
            
        # begin actual game
        while len(self.players) > 0:
            # start the game
            for player in self.players:
                self.current_player = player
                # continue until valid response
                valid_response = False
                while not valid_response:
                    # response must be a set of card objects
                    response = player.turn(self.state())
                    if list(response)[0].validate(last_played=self.last_played, play=response):
                        cards_to_remove = {(card.name, card.suit) for card in response}
                        self.last_played = response
                        player.hand = player.hand - cards_to_remove
                        valid_response = True
                    elif response == "skip":
                        valid_response = True
                        print(f"{player.name} has skipped their turn.")
                    else:
                        print(f"Sorry {player.name}, that is not a valid play.")
                # add player to out list and give them proper role
                if not player.hand:
                    if self.last_card_bomb(player.last_play):
                        player.role = self.roles_left.pop()
                    else:
                        player.role = self.roles_left.pop(0)
                    self.out.append(player)
                    print(f"{player.name} has emptied their hand and became {player.role}")
                # stop the game when one player is left
                if len(self.players) <= 0:
                    break
            # remove players who are out
            self.players = [player for player in self.players if not player in self.out]
        print(self.state().table)

def main():
    """
    Sets up and starts the card game President with human and computer players,
    with a maximum of players (matching the number of available roles).
    """
    parser = argparse.ArgumentParser(description="Play President card game.")
    parser.add_argument('--players', nargs='+', help='List of human player names', required=True)
    parser.add_argument('--computers', type=int, help='Number of computer players', default=0)
    parser.add_argument("-p", "--player", type=str, required=True, help="The player's name")
    parser.add_argument("-r", "--rank", type=str, required=True, help="The rank of the card(s) (e.g., ace, king)")
    parser.add_argument("-s", "--suit", type=str, required=True, help="The suit of the card(s) (e.g., hearts)")
    parser.add_argument("-n", "--number", type=int, default=1, help="Number of cards being played")
    args = parser.parse_args()

    max_players = len(ROLES)
    total_requested_players = len(args.players) + args.computers

    # Adjust player count if exceeding maximum
    if total_requested_players > max_players:
        if args.computers > 0:
            args.computers = max(0, args.computers - (total_requested_players - max_players))
        if len(args.players) > max_players - args.computers:
            args.players = args.players[:max_players - args.computers]

    players = []

    # Add human players from command-line arguments
    for name in args.players:
        players.append(HumanPlayer(name=name, hand=set()))

    # Add computer players
    for i in range(args.computers):
        players.append(ComputerPlayer(name=f"Computer {i + 1}", hand=set()))

    # Initialize the game instance
    game = Game(players)
    
    # Start the game
    first_game = True
    while True:
        game.play(first_game)
        first_game = False  # Only the first round is marked as `first_game`
        play_again = input("Play another round? (yes/no): ").strip().lower()
        if play_again != 'yes':
            break

if __name__ == "__main__":
    args = parser(sys.argv[1:])
    current_played = {Cards(args.rank, args.suit) for _ in range(args.number)}
    last_played = {Cards("king", args.suit) for _ in range(args.number)}
    print(valid_play(current_played, last_played, args.player))