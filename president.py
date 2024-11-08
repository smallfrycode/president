class GameState:
    """ Provide information on the current state of the game.
    
    Attributes:
        players (list): list of players 
    """
    
    def __init__(self, players):
        self.players = players 
    
    def display_players(self):
        print("Current Players")
        for player in self.players:
            print(f"- {player} ({player.role})")
            
    def display_table(self):
        print(f"Table: {self.last_played}")
        
    def display_hand(self):
        print(f"Hand: {self.hand}")
    