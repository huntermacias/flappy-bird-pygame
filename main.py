import pygame
from game import Game


game = Game()

# menu screen
game.display_menu()

game.run()

# set gamover to true
game.gameover = True   

# add score to databaseun
game.add_score_to_database(game.name, game.bird.score)

# game over screen
game.display_gamover_screen()