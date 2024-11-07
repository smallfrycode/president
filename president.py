class GameState:
    """ Provide information on the current state of the game.
    
    Attributes:
        last_play (list): List representing the last card or set of cards played in the pile. 
        role (str): Role of the player whose turn it is. 
    """
    
    def __init__(self, last_play, role):
        self.last_play = last_play
        self.role = role 
    
    def compare(self, other):
        """ Compares if the card or set being played is valid."""
        
        if len(self.last_play) == len(self.)