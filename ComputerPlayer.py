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
