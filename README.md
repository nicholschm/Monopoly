This program emulates the board game 'Monopoly'. It creates a class RealEstateGame, through which the
entire game can be played. The rules are as follows: Each player starts at space 0 ('GO'), with a
specified amount of money. Players take turns 'rolling' a six-sided die, and move around the board
(25 spaces including GO). Each time a player 'circles' the board (either passes or lands on GO) they
receive a specified amount of money. Each space (other than GO) has a 'Property' available for purchase,
with an accompanying 'Rent'. The purchase price is equal to 5x the Rent. If a player purchases the
property, each subsequent player who lands on that property must pay the 'Owner' Rent. If a player cannot
afford the Rent, the player sends their remaining funds to the Owner, loses all their purchased
properties, and is no longer involved in the game. The game is over when there is only 1 player remaining
with a non-zero account balance.
