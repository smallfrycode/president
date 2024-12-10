# President
A card game played with a standard deck of 52 cards.



## Using The Program
### Creating the Environment
To set up the environment, change your directory to where the file is and type the following in your terminal:

Windows: `python president.py [names] -c [number]`

Mac: `python3 president.py [names] -c [number]`

In `[names]` you will write the names of each human player you wish to add separated by a space (e.g `Mark, Bob, John`). If you wish to add computers, you must use the `-c` flag and write the amount of computer players you wish to add as an integer in place of `[numbers]` (e.g `2`). If you don't wish to have computer players, write `0` in `[numbers]` or don't include `-c [number]`.

### Playing The Game
Once the environment has been created, you will be prompted with your hand as well as other relevant information to the game. The game will tell you who's hand is being displayed and list you that player's cards in ascending order by rank. To play a card you must type the card's rank followed by the first letter of the suit capitalized (e.g `JS` or `5H`). To play pairs, you can separate these inputs with a ',' (e.g `JS, 5H`). If you can't or don't wish to play, type `pass` into the terminal to skip your turn.

The `Table` shows what was last played, if you see nothing in the table then you can play any of your cards. If there is a card/pair of cards on the table, you must play a card/pair of cards of a higher rank. The pair count of your play must be the same as what is on the table (i.e Table: `5H, 5S` - must play - `6D, 6H` - or higher rank). Suit doesn't matter.

Once the game has concluded you will be shown a results screen with each player's earned roles as well as a play again prompt. To play again you must type `yes`, any other input will tell the program to close.



## Overview of Code
### Card Class
The goal of this class is to represent a playing card.
#### Card.\_\_init__(rank, suit)
The goal of this method is to initialize a card object with a suit and rank.
- `rank` (str): the rank of the card
- `suit` (str): the card's suit

#### Card.\_\_gt__(other)
The goal of this method is to compare the ranks of two cards and see if self > other (typically the player's card(s) and the card(s) last played). It will return True if self.rank > other.rank and False otherwise.
- `other` (Card): the card object you are comparing with

#### Card.\_\_eq__(other)
The goal of this method is to compare the ranks and suits of two cards and see if they are the same (typically the player's card(s) and the card(s) last played). It will return True if the ranks and suits of both cards are the same, otherwise it will return False.
- `other` (Card): the card object you are comparing with

#### Card.validate(play, last_played)
The goal of this method is to compare a play trying to be made with the last play which was made. To validate a play it does the following:
- compares the number of card(s) the player wants to play to the number of card(s) previously placed (must be same)
- checks the ranks of each card in a player's play and compares it with the cards previously placed (must be >)
- checks if all player's cards are of the same rank in the case that multiple cards are placed
If all requirements above are met then it will return True, otherwise False.


### Player Class
The goal of this class is to represent the player.
##### Player.\_\_init__(name, hand)
The goal of this method is to initialize a player object.
- `name` (str): the player's name
- `hand` (list): all of the cards the player has

##### Player.turn(state)
This returns a NotImplementedError because this method isn't implemented unless a HumanPlayer or ComputerPlayer is created.

#### HumanPlayer(Player)
The goal of the HumanPlayer class is to represent a human-controlled player, inheriting from the Player class.
##### HumanPlayer.\_\_init__(name, hand)
The goal of this method is to initialize a human player [see Player initialization](#player__init__name-hand).

##### HumanPlayer.turn(state)
This method allows the user to make decisions about which cards to play or to pass their turn. Input is validated through a helper function (`convert()`) that parses card strings into `Card` objects using regular expressions, ensuring ranks and suits are valid and that the selected cards are in the player’s hand. If the input is invalid or mismatched, the player is re-prompted until a valid input is provided. Once a valid input is given, the method returns `None` if the player passes or a list of their chosen cards.

#### ComputerPlayer(Player)
The goal of the ComputerPlayer class is to represent a computer-controlled player, inheriting from the Player class.
##### ComputerPlayer.\_\_init__(name, hand)
The goal of this method is to initialize a computer player [see Player initialization](#player__init__name-hand).

##### ComputerPlayer.turn(state)
This method allows the computer to make decisions about which cards to play or to pass their turn. Based on what is currently on the table, it will search for the cards of the lowest rank and play them first. In order to help determine which cards it can play, it uses a helper function (`valid()`) which uses a list comprehension to create pairs of every card it has. If the pair size is greater than what was last played, then it slices off what isn't needed. A play will be returned if the computer finds one, otherwise it will return `None` to pass.
```
group = [c for c in self.hand if c.rank == card_rank] # card_rank is based on what value is provided when iterating through the CARD_VALUES constant list (provides all card ranks)
if len(group) >= last_play_size:
    play = group[:last_play_size] # slice off what isn't needed
```


### GameState Class
Provides information on the current state of the game.
#### GameState.__init__(players, last_played, current_player)
The goal of this method is to initialize the GameState class and create the necessary attributes to represent the state of the game visually.
- `players` (list): a collection of all the players as a list
- `last_played` (set): the last card(s) which were played as a set
- `current_player` (Player): the person who is currently playing
- `out` (list): all the players who have emptied their hand

#### GameState.\_\_str__()
The goal of this method is the show an informal representation of the state of the game. It will create a string representing the players of the game with their corresponding roles. Then it will create a string representing the last card(s) that were played on the table. Then it will create a string representing the hand of the current player. A helper function is used to help grab the unicode for card suits (`find_unicode()`). Lastly, it will return a string representing all of this information (players with their corresponding roles, last hand played, and current player's hand).

#### GameState.results()
The goal of this method is to return the results of the game in a string that shows each persons name and their corresponding role. 


### Game Class
The skeleton of the program, sets up the game environment and controls the game.
#### Game.\_\_init__(players)
The goal of this method is to create the necessary attributes in order for the game to function.
- `deck` (list): a collection of all the cards in the deck
- `players` (list): a collection of all the players
- `out` (list): a collection of all the players who have emptied their hand
- `roles_left` (list): a list of all the available roles which can be won during the game
- `current_player` (Player): the person who is currently playing
- `last_played` (list or None): the last card(s) which were played

#### Game.shuffle()
The goal of this method is to shuffle the deck of cards. It will first create a temporary list of unshuffled cards using the `Card` class ([see documentation above](#card-class)) to create Card objects. Afterwards the `choice()` function from the `random` python module is used to choose a random card from the list of unshuffled cards. This chosen card is than appended to `Game.deck` and removed from the unshuffled cards list.

#### Game.deal()
The goal of this method is to deal out all the cards evenly from the deck to each player's hand. A while loop is used to continue dealing out all the cards until the deck is empty and variables `max_index` and `index` are used to iterate through the players. The variable `index` starts at 1 in order to follow the "left-of-the-dealer" rule and cards are added + removed using `pop()`. After all cards are dealt, the method then organizes a player's card in ascending order (by card rank) using the `sorted()` and `lambda` functions.

#### Game.create_roles()
The goal of this method is to set up the possible roles players can win. This is dependent on the amount of players who are currently playing. A dictionary is made with numbers to organize the list of roles and help choose what is appropriate.
```
self.roles_left = {
    4: ["President", "Vice President", "Vice Trash", "Trash"],
    5: ["President", "Vice President", "Neutral 1", "Vice Trash", "Trash"],
    6: ["President", "Vice President", "Neutral 1", "Neutral 2", "Vice Trash", "Trash"],
    7: ROLES.copy()
}[player_count]
```

#### Game.last_card_bomb(last_play)
The goal of this method is to help determine if a player's final play was a bomb (i.e 2). It will loop through the list, `last_play`, which was the play made by the previous player who completed their turn. If a bomb was played then it returns True, otherwise it returns False.

#### Game.state()
The goal of this method is to grab the current state of the game. It returns a GameState object ([see documentation above](#gamestate-class)).

#### Game.play(first_game)
The goal of this method is to run the actual game. It first checks to make sure that a game hasn't been played yet (i.e `first_game = True`). If a game was previously played, then it will sort player's based on their roles and reset `Game.out` and `Game.last_played`. The game will then run the `shuffle()`, `deal()`, and `create_roles()` methods in order to set up the environment. From here the game will continue to play until 1 player is left.

When iterating through each player, the game will keep track of how many skips were made. If no one is able to play, the `skip_count` is used to help reset the table and let the last player who completed their turn to play anything of their choosing. After this, the game will ask for a response (`player.turn(Game.state())` -> [see documentation for player](#player-class)) and determine if it is valid:
- `None` -> player has skipped
- `Card.rank = 2` (must be played prior to other cards) -> player has played a bomb
- `Card.validate(Game.last_played, response) = True` -> valid play made
- None of the above -> invalid play, prompts user for a response again

If a valid play is made, the game will remove any cards from the player's hand if any were played. If a 2 was played and the player still has a hand, the player will have the ability to go again.
```
if player.hand:
    continue
valid_response = True # this is not executed because the player still has a hand
```

If a 2 was the last card played, then the lowest role available will be given, otherwise the highest role available will be given. The player will then be removed from the `Game.players` list and added to the `Game.out` list.

Once the game has concluded, the last player will be removed from the `Game.players` list, added to the `Game.out` list, given the last role available, and the `GameState.results()` method will be called in order to retrieve and display the results of the game.


### main(players, computers)
This function sets up and starts the card game, managing both human and computer players while ensuring the total player count is between 4-7 players.

It takes the list of human player names (`players`) and the number of computer players (`computers`), adjusting the counts if needed. The game runs in a loop, calling `Game.play()` and tracking whether a game was previously played. After each round, the user is prompted to play again with the loop continuing until the user opts out.


### parse_args(arglist)
The goal of this function is to parse command line arguments.

It utilizes the `ArgumentParser()` class (from the `argparse` module) and adds 2 arguments, `players` as well as `--computers` with the `add_argument()` method. The `players` argument is the list of player names [human players](#humanplayerplayer) whereas the `--computers` argument keeps track of how many computer players should be added [see ComputerPlayer class](#computerplayerplayer). While you must add at least 1 human player, adding computers is optional and can be added by using the `-c` flag followed by the number of computers you want to add as an integer. This function returns a namespace by using the `parse_args(arglist)` method. The parameter `arglist` is created by using `sys.argv` to grab the command line arguments.



## Authors
Contributors of this project:
- smallfrycode
- duckwookwon
- kayetubal
- Ireland2004
- andychen47 (some commits were made by his other account: Iamold21)



### Contribution Details
| Method/Function                     | Primary Author | Techniques Demonstrated               |
| ---------------                     | -------------- | -----------------------               |
| `Card.__init__()`                   | Ireland2004    | N/A                                   |
| `Card.__gt__()`                     | Ireland2004    | Magic methods                         |
| `Card.__eq__()`                     | smallfrycode   | N/A                                   |
| `Card.validate()`                   | Ireland2004    | Keyword Arguments                     |
| `Player.__init__()`                 | smallfrycode   | N/A                                   |
| `Player.turn()`                     | smallfrycode   | N/A                                   |
| `HumanPlayer(Player).__init__()`    | andychen47     | N/A                                   |
| `HumanPlayer(Player).turn()`        | andychen47     | List comprehension                    |
| `convert()` (helper function)       | smallfrycode   | Regular expressions                   |
| `ComputerPlayer(Player).__init__()` | duckwookwon    | super()                               |
| `ComputerPlayer(Player).turn()`     | duckwookwon    | Use of a key function (min(); lambda) |
| `valid()` (helper function)         | duckwookwon    | N/A                                   |
| `GameState.__init__()`              | kayetubal      | N/A                                   |
| `GameState.__str()__`               | kayetubal      | f-string containing expressions       |
| `find_unicode()` (helper function)  | kayetubal      | Conditional expression                |
| `GameState.results()`               | smallfrycode   | N/A                                   |
| `Game.__init__()`                   | smallfrycode   | N/A                                   |
| `Game.shuffle()`                    | smallfrycode   | N/A                                   |
| `Game.deal()`                       | smallfrycode   | N/A                                   |
| `Game.create_roles()`               | smallfrycode   | N/A                                   |
| `Game.last_card_bomb()`             | smallfrycode   | N/A                                   |
| `Game.state()`                      | smallfrycode   | N/A                                   |
| `Game.play()`                       | smallfrycode   | Composition of two custom classes     |
| `main()`                            | andychen47     | N/A                                   |
| `parse_args()`                      | andychen47     | ArgumentParser() class                |



## License
This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the LICENSE file for details.



## Acknowledgements
- python random module
    - [see Game.shuffle() method](#gameshuffle)
    - https://docs.python.org/3/library/random.html
    - Author: Python
- python argparse module
    - [see parse_args function](#parse_argsarglist)
    - https://docs.python.org/3/library/argparse.html
    - Author: Python
- python sys module
    - [see parse_args function](#parse_argsarglist)
    - https://docs.python.org/3/library/sys.html
    - Author: Python
- python re module
    - [see HumanPlayer.turn() method](#humanplayerturnstate)
    - https://docs.python.org/3/library/re.html
    - Author: Python
- President Rules
    - https://bicyclecards.com/how-to-play/presidents
    - Author: BicycleCards
    - some rules which aren't included above came from our variation (e.g 2's being bombs)
