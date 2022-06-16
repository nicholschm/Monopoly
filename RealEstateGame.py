# Author: Nicholas Schmidt
# GitHub username: nicholschm
# Date: 05/23/2022
# Description: This program emulates the board game 'Monopoly'. It creates a class RealEstateGame, through which the
#              entire game can be played. The rules are as follows: Each player starts at space 0 ('GO'), with a
#              specified amount of money. Players take turns 'rolling' a six-sided die, and move around the board
#              (25 spaces including GO). Each time a player 'circles' the board (either passes or lands on GO) they
#              receive a specified amount of money. Each space (other than GO) has a 'Property' available for purchase,
#              with an accompanying 'Rent'. The purchase price is equal to 5x the Rent. If a player purchases the
#              property, each subsequent player who lands on that property must pay the 'Owner' Rent. If a player cannot
#              afford the Rent, the player sends their remaining funds to the Owner, loses all their purchased
#              properties, and is no longer involved in the game. The game is over when there is only 1 player remaining
#              with a non-zero account balance.

class RealEstateGame:
    """This class takes no parameters. It initializes 3 private data members: spaces (empty dict), players (empty dict),
    and in_game (empty list). 'spaces' utilizes the method 'create_spaces' to create 25 board spaces, each with a unique
    name and 24 of which will have an accompanying 'Rent' (space 0 'GO' cannot be purchased). 'players' utilizes the
    method create_player, which will store the players' names, account balances, current position, and owned properties.
    'in_game' keeps track of which players are currently still involved in the game (as they go bankrupt,
    they are removed)."""

    def __init__(self):
        self._spaces = dict()
        self._players = dict()
        self._in_game = list()

    def create_spaces(self, go_amount, array_of_rents):
        """This method takes 2 parameters: go_amount and array_of_rents. 'go_amount' will be the amount of money each
        player will receive when they either land on or pass the GO space. 'array_of_rents' is a list of 24 integers
        which will be assigned to each space respective to their positioning in the list, beginning with space 1."""

        space_indexes = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
        self._spaces[0] = {'Name of Property':'GO', 'Rent':go_amount}

        # After initializing the GO space, each subsequent board space is added to the self._spaces dictionary, with the
        # key as the index of the space (0-24) and the value a dictionary with keys 'Name of Property' and 'Rent'.
        for index in space_indexes:
            self._spaces[index] = {'Name of Property': index, 'Rent':array_of_rents[index-1]}

        list_of_names = ['1st Street', '2nd Avenue', '3rd Block', '4th Road', '5th Place', '6th Square', '7th Street',
                         '8th Avenue', '9th Block', '10th Road', '11th Place', '12th Square', '13th Street',
                         '14th Avenue', '15th Block', '16th Road', '17th Place', '18th Square', '19th Street',
                         '20th Avenue', '21st Block', '22nd Road', '23rd Place', '24th Square']

        # Updates 'Name of Property' value for each space in the dictionary with the previously determined unique names.
        for name in space_indexes:
            self._spaces[name]['Name of Property'] = list_of_names[name-1]

        # Adds a new key:value pair to each space in the dictionary ('Purchase Price' : Rent * 5)
        for price in self._spaces:
            self._spaces[price]['Purchase Price'] = self._spaces[price]['Rent'] * 5

        # Adds a new key:value pair to each space in the dictionary ('Owner' : None). Each space's owner is initialized
        # to None. When purchased, the value is updated. If the owner bankrupts, the owner reverts to None.
        for owner in self._spaces:
            self._spaces[owner]['Owner'] = None

    def players_in_game(self):
        """This method takes no parameters, and returns the list of players' names currently active in the game."""

        return self._in_game

    def get_owned_properties(self, player_name):
        """This method takes one parameter, player_name, and returns a list of properties owned by a player, if any.
         The values of the list will be the indexes of the space/property owned."""

        return self._players[player_name]['Owned Properties']

    def get_property_name(self, position):
        """This method takes one parameter, position, and returns the name of the property located at that space/index
        as a string."""

        if position < 0 or position > 24:
            return "Invalid Board Space"
        else:
            return self._spaces[position]['Name of Property']

    def create_player(self, player_name, account_balance):
        """This method takes two parameters, player_name and account_balance. As each player is created, a dictionary
        entry is created for that player, with the key being the player name and the values being: 'Account Balance',
        'Position', and 'Owned Properties'. 'account_balance' should be the total starting balance for each player. Each
        player will start at position 0, and their owned properties list will be empty. The players' names will be added
        to the self._in_game list, and will remain until their account balances are 0."""

        player_dict = {player_name:{'Account Balance':account_balance, 'Position':0, 'Owned Properties':list()}}
        self._players.update(player_dict)
        self._in_game.append(player_name)

    def get_player_account_balance(self, player_name):
        """This method takes one parameter, player_name, and returns that player's account balance."""

        return self._players[player_name]['Account Balance']

    def get_player_current_position(self, player_name):
        """This method takes one parameter, player_name, and returns the player's current position (space) on the board
        as an integer."""

        return self._players[player_name]['Position']

    def buy_space(self, player_name):
        """This method takes one parameter, player_name. If a player attempts to buy a property that is already owned,
        False is returned. Otherwise, assuming the player has sufficient funds, the player will become the owner, and
        this method will return True. The space index of the property is added to the player's owned properties list."""

        current_position = self._players[player_name]['Position']
        if self._spaces[current_position]['Owner'] is not None:
            return False
        elif current_position == 0:
            return False
        else:
            # First check to ensure the player has sufficient funds to make the purchase.
            if self._players[player_name]['Account Balance'] > self._spaces[current_position]['Purchase Price']:
                self._players[player_name]['Account Balance'] -= self._spaces[current_position]['Purchase Price']
                self._spaces[current_position]['Owner'] = player_name
                self._players[player_name]['Owned Properties'].append(self._players[player_name]['Position'])
                return True
            else:
                return False

    def move_player(self, player_name, spaces):
        """This method takes two parameters, player_name and spaces. 'spaces' will be the number of spaces the player
        will move for their current turn, and must be an integer between 1 and 6 (inclusive). If the player passes or
        lands on GO, they will receive bonus funds equal to the initialized go_amount. If a player lands on a space with
        no owner and has sufficient funds, the player can purchase the property. If the player lands on a property that
        is already owned, that player must pay the owner the associated Rent. If the player cannot afford the rent,
        their remaining account balance is sent to the owner, and they are removed from the game."""
        if self._players[player_name]['Account Balance'] == 0:
            return

        if spaces < 1 or spaces > 6:
            return 'Invalid Move'

        # If player passes or lands on GO:
        if self._players[player_name]['Position'] + spaces > 24:
            self._players[player_name]['Account Balance'] += self._spaces[0]['Rent']
            self._players[player_name]['Position'] = self._players[player_name]['Position'] + spaces - 25
            current_position = self._players[player_name]['Position']
            if self._players[player_name]['Position'] == 0:
                return

            # If player passes but does not land on GO:
            if self._spaces[current_position]['Owner'] is not None:

                # If player has sufficient funds to pay Rent
                payee = self._spaces[current_position]['Owner']
                if self._players[player_name]['Account Balance'] >= self._spaces[current_position]['Rent']:
                    self._players[player_name]['Account Balance'] -= self._spaces[current_position]['Rent']
                    self._players[payee]['Account Balance'] += self._spaces[current_position]['Rent']

                #If player does not have sufficient funds to pay Rent
                else:
                    self._players[payee]['Account Balance'] += self._players[player_name]['Account Balance']
                    self._players[player_name]['Account Balance'] = 0
                    self._in_game.remove(player_name)
                    for property in self._players[player_name]['Owned Properties']:
                        self._spaces[property]['Owner'] = None

        # If player moves and does not pass or land on GO
        else:
            self._players[player_name]['Position'] = self._players[player_name]['Position'] + spaces
            current_position = self._players[player_name]['Position']

            # If the property the player moved to is already owned
            if self._spaces[current_position]['Owner'] is not None:
                payee = self._spaces[current_position]['Owner']

                # If the player has sufficient funds to pay the rent
                if self._players[player_name]['Account Balance'] > self._spaces[current_position]['Rent']:
                    self._players[player_name]['Account Balance'] -= self._spaces[current_position]['Rent']
                    self._players[payee]['Account Balance'] += self._spaces[current_position]['Rent']

                # If the player does not have sufficient funds to pay the rent
                else:
                    self._players[payee]['Account Balance'] += self._players[player_name]['Account Balance']
                    self._players[player_name]['Account Balance'] = 0
                    self._in_game.remove(player_name)
                    for property in self._players[player_name]['Owned Properties']:
                        self._spaces[property]['Owner'] = None

    def check_game_over(self):
        """This method takes no parameters. At any point during the game, this method can be called. If there is more
        than 1 player remaining in the game, an empty string will be returned. However, if there is only one player
        remaining then that player is the winner, and their name is returned as a string."""

        if len(self._in_game) > 1:
            return ""
        else:
            return self._in_game[0]


# game = RealEstateGame()
# rents = [100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,290,300,310,320,330]
# game.create_spaces(0, rents)
# game.create_player('Geralt', 1500)
# game.create_player('Barry', 1500)
# print(game.get_owned_properties('Geralt'))
# print(game.players_in_game())
# print(game.get_property_name(20))
# game.move_player('Barry', 1)
# print(game.buy_space('Barry'))
# game.move_player('Barry', 1)
# game.buy_space('Barry')
# game.move_player('Geralt', 3)
# game.buy_space('Geralt')
# game.move_player('Geralt', 1)
# game.buy_space('Geralt')
# game.move_player('Barry', 1)
# game.move_player('Barry', 1)
# game.move_player('Barry', 6)
# game.move_player('Barry', 6)
# game.move_player('Barry', 6)
# game.move_player('Barry', 6)
# print(game.get_player_account_balance('Barry'))
# print(game.check_game_over())
# game.move_player('Barry', 1)
# print(game.get_player_account_balance('Barry'))
# print(game.check_game_over())
