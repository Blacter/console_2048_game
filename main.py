import game2048 as g  
# Game2048.

print('Welcom to 2048 game. Enter "help" for instruction.')
input('Press enter to coutinue.')


game = g.Game2048()
game.show_score()
game.show_game_field()
user_input = input('> ')

while user_input != 'exit':
  code, msg = game.game_2048_main(user_input)  
  game.show_score()
  game.show_game_field()
  print(msg)
  user_input = input('> ')

