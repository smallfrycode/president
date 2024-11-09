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
        
        # Show the player's hand and the last card played
        print(f"\n{self.name}'s turn. Last card played: {last_card}")
        print(f"Your hand: {self.hand}")
        
        # Filter cards that can be played based on the last card
        playable_cards = [card for card in self.hand if card > last_card]
        
        if playable_cards:
            print(f"Playable cards: {playable_cards}")
            
            while True:
                # Ask player for input
                choice = input("Enter the card you want to play or type 'pass' to pass: ")
                
                if choice == "pass":
                    print(f"{self.name} skips their turn.")
                    return "pass"
                
                # Checks if the chosen card is valid
                try:
                    selected_card = int(choice)
                    if selected_card in playable_cards:
                        self.hand.remove(selected_card)
                        print(f"{self.name} plays {selected_card}")
                        return selected_card
                    else:
                        print("Invalid choice. Please select a playable card or 'pass'.")
                except ValueError:
                    print("Invalid input. Please enter a valid card or 'pass'.")
        
        else:
            print(f"No playable cards. {self.name} skips their turn.")
            return "pass"
        
class ComputerPlayer(Player):
    def __init__(self, name, hand):
        super().__init__(name, hand) 
    
    def take_turn(self, game_state):
        """
        Decides what card to play based on the last card on the table.
        
        - game_state: Info about the last card played and whose turn it is.
        
        Returns:
        - The chosen card if it can play one, or 'skip' if no valid move.
        """
        
        last_card = game_state.get_last_card_played() 
        
       
        playable_cards = []
        
        for card in self.hand:
            if card > last_card:
                playable_cards.append(card)

        if playable_cards:
            
            playable_cards.sort()
            selected_card = playable_cards[0]              
         
            self.hand.remove(selected_card)
            print(f"{self.name} plays {selected_card}")
            return selected_card
        else:
            print(f"{self.name} skips their turn.")
            return "skip"


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
                    valid_cards = {r for r in response if r.is_valid_play(self.last_played)}
                    if len(valid_cards) == len(response):
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