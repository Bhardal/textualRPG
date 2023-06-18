from jdr_basic import *


difficulty = input("In which difficulty do you wish to play ? : ")
try:
    difficulty = int(difficulty)
except:
    difficulty = 1

nb = input("How many will you be in this adventure ? (up to 4) : ")
try:
    nb = int(nb)
except:
    nb = 1

players = [None, None, None, None]
playernames = [None, None, None, None]
for i in range(nb):
    playernames[i] = input("The character's name : ")
    players[i] = Creature(playernames[i])



game = Game(players[0], difficulty, players[1], players[2], players[3])

game.Start()
for _ in range(12):
    game.NewArea()