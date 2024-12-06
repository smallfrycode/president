# President
A card game played with a standard deck of 52 cards.

## Description
--description goes here--

## Overview of Code
### Card Class
--Card Class info goes here--

### Player Class
--Player Class info goes here (talk about HumanPlayer and ComputerPlayer child classes under this)--

### GameState Class
--GameState Class info goes here--

### Game Class
The skeleton of the program, sets up the game environment and controls the game.

#### Game.__init__(players)
The goal of this method is to create the necessary attributes in order for the game to function.
- deck (list): a collection of all the cards in the deck
- players (list): a collection of all the players
- out (list): a collection of all the players who have emptied their hand
- roles_left (list): a list of all the available roles which can be won during the game
- current_player (Player): the person who is currently playing
- last_played (list or None): the last card(s) which were played

#### Game.shuffle()
The goal of this method is to shuffle the deck of cards. It will first create a temporary list of unshuffled cards using the `Card` class ([see documentation above](#card-class)) to create Card objects. Afterwards the `choice()` function from the `random` python module is used to choose a random card from the list of unshuffled cards. This chosen card is than appended to `Game.deck` and removed from the unshuffled cards list.

#### Game.deal()
The goal of this method is to deal out all the cards evenly from the deck, to each player's hand. A while loop is used to continue dealing out all the cards until the deck is empty and variables `max_index` and `index` are used to iterate through the players. The variable `index` starts at 1 in order to follow the "left-of-the-dealer" rule and cards are added + removed using `pop()`. After all cards are dealt, the method then organizes a player's card in ascending order (by card rank) using the `sorted()` and `lambda` functions.

#### Game.create_roles()
The goal of this method is to set up the possible roles player's can win. This is dependent on the amount of players who are currently playing. A dictionary is made with numbers to organize the list of roles and help choose what is appropriate.
```
self.roles_left = {
    2: ["President", "Trash"],
    3: ["President", "Neutral 1", "Trash"],
    4: ["President", "Vice President", "Vice Trash", "Trash"],
    5: ["President", "Vice President", "Neutral 1", "Vice Trash", "Trash"],
    6: ["President", "Vice President", "Neutral 1", "Neutral 2", "Vice Trash", "Trash"],
    7: ROLES.copy()
}[player_count]
```

#### Game.last_card_bomb(last_play)
The goal of this method is to help determine if a player's final play was a bomb (i.e 2). It will loop through the list, `last_play`, which was the play made by the previous player who completed their turn. If a bomb was played then it returns True, otherwise it returns False.

#### Game.state()
The goal of this method is to grab the current state of the game. It returns an informal representation of a GameState object ([see documentation above](#gamestate-class)).

#### Game.play(first_game)
The goal of this method is to run the actual game. It first checks to make sure that a game hasn't been played yet (i.e `first_game = True`). If a game was previously played, then it will sort player's based on their roles and reset `Game.out` and `Game.last_played`. The game will then run the `shuffle()`, `deal()`, and `create_roles()` methods in order to set up the environment. From here the game will continue to play until 1 player is left.

When iterating through each player, the game will keep track of how many skips were made. If no one is able to play, the `skip_count` is used to help reset the table and let the last player who completed their turn to play anything of their choosing. After this, the game will ask for a response (`player.turn(Game.state())` -> [see documentation for player](#player-class)) and determine if it is valid:
- None -> player has skipped
- `Card.rank = 2` (must be played prior to other cards) -> player has played a bomb
- `Card.validate(Game.last_played, response) = True` -> valid play made
- None of the above -> invalid play, prompts user for a response again

If a valid play is made, the game will remove any cards from the player's hand if any were played. If a 2 was played and the player still has a hand, then the thread will continue and let the player go again.
```
if player.hand:
    continue
valid_response = True # this is not executed because the player still has a hand
```

If a 2 was the last card played, then the lowest role available will be given, otherwise the highest role available will be given. The player will then be removed from the `Game.players` list and added to the `Game.out` list.

Once the game has concluded, the last player will be removed from the `Game.players` list, added to the `Game.out` list, given the last role available, and the `GameState.results()` method will be called in order to retrieve and display the results of the game.

### main(players, computers)
--main() function info goes here--

### parse_args(arglist)
--parse_args() function info goes here--

## Authors
Contributors of this project:
- smallfrycode
- duckwookwon
- kayetubal
- Ireland2004
- andychen47 (some commits were made by his other account: Iamold21)

### Contribution Details
| Method/Function | Primary Author | Techniques Demonstrated |
| --------------- | -------------- | ----------------------- |
|     insert      |      rows      |          below          |

## License
This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the LICENSE file for details.

## Acknowledgements
- python random module [see Game.shuffle() method](#gameshuffle)
- python arparse module
- python sys module
- python re module