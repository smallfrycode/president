import argparse
"""A program which can play the card game President."""
ROLES = ["President", "Vice President", "Neutral", "Vice Trash", "Trash"]
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
        
        last_card = game_state.get_last_card_played()
        playable_cards = [card for card in self.hand if card > last_card]
        
        if playable_cards:
            while True:
                # Ask player for input
                choice = input("Enter the card you want to play or type 'pass' to pass: ")
                
                if choice == "pass":
                    return "pass"
                
                # Checks if the chosen card is valid
                try:
                    selected_card = int(choice)
                    if selected_card in playable_cards:
                        self.hand.remove(selected_card)
                        return selected_card
                except ValueError:
                    pass  # Ignore invalid input; the player will be prompted again
        # Automatically skip if no playable cards
        return "pass"
        
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
                card (Card): The card to use for forming a set.
            
            Returns:
                set or None: A valid set of cards if available, None otherwise.
            """
            group = {c for c in self.hand if c.value == card.value}

            # Check if the group is large enough to match the last played set
            if len(group) >= last_play_size:
                if card.validate(last_played=last_played, play=group):
                    return group if last_play_size == 1 else set(list(group)[:last_play_size])
            
            return None

        # Find all valid card sets
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
        players (list): a collection of all the players as a list
        last_played (set): the last card(s) that were played.
        current_player (Player): the person who is currently playing as a Player object.
    """
    
    def __init__(self, players, last_played, current_player):
        """ Initializes the GameState class.
        
        Args:
            players (list): a collection of all the players as a list
            last_played (set): the last card(s) which were played as a set
            current_player (Player): the person who is currently playing as a Player object
        """
        self.players = players
        self.last_played = last_played
        self.current_player = current_player
        
    def __str__(self):
        def find_unicode(suit):
            """ Determines the unicode depending on the suit of the card."""
            symbol = "\u2660" if suit == "Spades" else "\u2665" if \
                suit == "Hearts" else "\u2666" if suit == "Diamonds" \
                else "\u2663"
            return symbol
        
        players_rep = "Current Players:\n"
        for player in self.players:
            players_rep += f"- {player.name} ({player.role})\n"
    
        table_rep = ""
        for card in self.last_played:
            table_rep += card.rank + find_unicode(card.suit)
            
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
    main()