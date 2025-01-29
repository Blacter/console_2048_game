from copy import deepcopy
from random import randint
import pickle
import os

class Game2048:

  def __init__(self, game_data = None):
    self.__game_field = [[0]*4 for i in range(4)]
    self.__game_score = 0
    self.__game_field_size = 4

    self.__prev_game_field_state = None
    self.__prev_game_score = 0

    self.__prev_move_code = -1
    self.__action_name_to_action_code = {
      'up': 0,
      'w': 0,
      'left': 1,
      'a': 1,
      'down': 2,
      's': 2,
      'right': 3,
      'd': 3,
      'back': 4,
      'b': 4,
      'menu': 5,
      'show menu': 5,
      'help': 6,
      'show action names': 6,
      'restart': 7,
      'load': 8,
      'save': 9,

    }

    self.__action_code_descriptions = {
      0: 'make move up',
      1: 'make move right',
      2: 'make move down',
      3: 'make move left',

      4: 'make move back',
      5: 'show menu',
      6: 'show action names and their description',
      7: 'restart the game',
      8: 'load the game',
      9: 'save the game',
    }

    self.set_new_value_on_game_field()

  def show_action_names(self):
    """Print action names, which can be used by user."""
    # action_codes = list(set(self.__action_name_to_action_code.values()))
    # action_codes.sort()

    prev_action_code = None
    width_for_action_name = max(map(len, self.__action_name_to_action_code.keys()))
    # print(f'{width_for_action_name=}')
    
    for action_name, action_code in self.__action_name_to_action_code.items():
      if prev_action_code is not None and prev_action_code != action_code:
        print()
      print(f'{action_name :.<{width_for_action_name}}: {self.__action_code_descriptions[action_code]}')
      prev_action_code = action_code

  @property
  def game_field(self, field: list[list[int]]) -> None:
    return deepcopy(field)  

  @game_field.setter
  def game_field(self, field) -> list[list[int]]:
    if len(field) != self.__game_field_size:
      print('Ошибка: неверный размер поля игры по вертикали.')

    for length in (len(row) for row in field):
      if length != 4:
        print('Ошибка: неверный размер поля игры по горизонтали.')
        break

    for row in field:
      for cell in row:
        if not isinstance(cell, int):
          print('Ошибка: неверный тип значения в ячейке поля игры.')

    self.__game_field = deepcopy(field)

  def get_line(self, direction_code, line_number) -> list[int]:
    """Get line of the game field and return in form of list."""
    line = []
    if direction_code == 0: # Up.
      for j in range(self.__game_field_size):
        line.append(self.__game_field[j][line_number])        
    elif direction_code == 1: # Left.
     line = self.__game_field[line_number][:]
    elif direction_code == 2: # Down
      for j in range(self.__game_field_size):
        line.append(self.__game_field[j][line_number])
      line.reverse()
    elif direction_code == 3: # Right
      line = self.__game_field[line_number][:]
      line.reverse()
    return line    

  def show_game_field(self) -> None:
    """Print game field."""
    max_cell = 0
    for row in self.__game_field:
      for cell in row:
        if max_cell < cell:
          max_cell = cell
    
    cell_width = len(str(max_cell))
    for row in self.__game_field:
      for cell in row:
        print(str(cell).rjust(cell_width), end=' ')
      print()
    
  def show_score(self) -> None:
    """Print game score."""
    print(f'game score = {self.__game_score}')

  def is_action_name_correct(self, action_name):
    '''Check the action name.'''
    return action_name in self.__action_name_to_action_code
    
  def get_action_code_by_action_name(self, action_name):
    ''' Get action code corresponding to the action name.'''
    if action_name in self.__action_name_to_action_code:
      return self.__action_name_to_action_code[action_name]
    else:
      return -1
  
  def save_data_for_move_back(self, current_action_code): # field, score, current_action.
    '''Save data in object attributes.'''
    self.__prev_game_field_state = deepcopy(self.__game_field)
    self.__prev_game_score = self.__game_score
    self.__prev_move_code = current_action_code

  def sum_line(self, line) -> int:
    r"""Get the "line sum" according to the 2048 game rules
    and return sum of points earned in this line"""
    i = 0
    score_to_add = 0
    first_not_zero_idx = -1
    state = 0 # 0 - find_firts_not_zero, 1 - find_second_not_zero. 2 - compare values.
    while i < self.__game_field_size:
      if state == 0 and line[i] != 0:
        first_not_zero_idx = i
        state = 1
      elif state == 1 and line[first_not_zero_idx] == line[i]:
        line[first_not_zero_idx] += line[i]
        score_to_add += line[first_not_zero_idx]
        line[i] = 0
        first_not_zero_idx += 1
        state = 1
      elif state == 1 and line[i] != 0:
        first_not_zero_idx = i
        state = 1
      i += 1
    return score_to_add

  def shift_line(self, line):
    """Shift line according to 2048 game rules."""
    zero_idx = -1
    state = 0 # 0 - поиск нулевого элемента. 1 - поиск не нулевого элемента
    i = 0
    while i < self.__game_field_size:
      if state == 0 and line[i] == 0:
        zero_idx = i
        state = 1
      elif state == 1 and line[i] != 0:
        line[zero_idx] = line[i]
        line[i] = 0
        zero_idx += 1        
      i += 1

  def save_line(self, direction_code, line_number, line):
    if direction_code == 0:
      for j in range(self.__game_field_size):
        self.__game_field[j][line_number] = line[j]
    elif direction_code == 1:
      for j  in range(self.__game_field_size):
        self.__game_field[line_number][j] = line[j]
    elif direction_code == 2:
      for j in range(self.__game_field_size):
        self.__game_field[self.__game_field_size-j-1][line_number] = line[j]
    elif direction_code == 3:
      for j in range(self.__game_field_size):
        self.__game_field[line_number][self.__game_field_size-j-1] = line[j]

  def generate_new_value_for_cell(self) -> int:
    a = randint(0, 3)
    if a == 3:
      return 4
    else:
      return 2

  def get_free_cells_count(self) -> int:
    free_cells_count = 0

    for row in self.__game_field:
      for cell in row:
        if cell == 0:
          free_cells_count += 1

    return free_cells_count

  def get_coords_by_number(self, num: int):
    return num // self.__game_field_size, num % self.__game_field_size

  def get_number_by_coords(self, coords) -> int:
    return self.__game_field_size*coords[0] + coords[1]

  def set_new_value_on_game_field(self):
    """Set new value on the game field."""
    free_cells_count = self.get_free_cells_count()

    if free_cells_count == 0:
      return

    cell_number_to_insert_value = randint(0, free_cells_count-1)
    zero_value_cells_passed = 0
    i = 0
    j, k = 0, 0
    while zero_value_cells_passed < cell_number_to_insert_value or i < self.__game_field_size ** 2 and self.__game_field[j][k] != 0:
      if self.__game_field[j][k] == 0:        
        zero_value_cells_passed += 1
      i += 1
      j, k = self.get_coords_by_number(i)
    self.__game_field[j][k] = self.generate_new_value_for_cell()

  def make_move(self, direction_code):
    """Make move in the direction."""
    for line_number in range(self.__game_field_size):
      line = self.get_line(direction_code, line_number)

      self.__game_score += self.sum_line(line)
      self.shift_line(line)

      self.save_line(direction_code, line_number, line)
    self.set_new_value_on_game_field()

  def is_opportunity_to_move_back(self):
    """Check the opportunity to make move back."""
    return self.__prev_move_code != -1 and self.__prev_move_code != 4

  def save_last_move_code(self, current_move_code):
    """Save last move code in object's attribute."""
    self.__prev_move_code = current_move_code

  def do_move_back(self):
    """Make move back."""
    self.__game_score = self.__prev_game_score 
    self.__game_field = deepcopy(self.__prev_game_field_state)

  def game_2048_main(self, action_name: str):   
    """Do the game action."""
    def is_game_over():
      """Check ability to make move."""
      return not any(directions_to_go.values()) 

    def is_opportunity_to_make_move():
      """Return all possible directions to go."""
      return directions_to_go[current_action_code]

    if not self.is_action_name_correct(action_name):
      return (-1, 'wrong action name')
    
    current_action_code = self.get_action_code_by_action_name(action_name)

    if 0 <= current_action_code <= 3:
      # Do step forward.
      directions_to_go = self.get_directions_to_move()
      # print(f'{directions_to_go = }')
      if is_game_over():
        return (1, 'end of the game')
      
      if not is_opportunity_to_make_move():
        return (0, 'Ход ' + action_name +' невозможен')

      self.save_data_for_move_back(current_action_code) # field, score, current_action

      self.make_move(current_action_code)

      return (0, f'last move: {action_name}')

    elif current_action_code == 4:

      if not self.is_opportunity_to_move_back():
        return (0, 'Ход назад невозможен.')
      
      self.do_move_back()
      self.save_last_move_code(current_action_code)

    elif current_action_code == 5:
      return (0, 'Тут должно быть меню.')
    elif current_action_code == 6:
      self.show_action_names()
    elif current_action_code == 7:
      self.start_new_game()
    elif current_action_code == 8:
      if self.load_game('user_data/saved_games/game_file_01.bin'):
        return (0, 'Game loaded succefully.')
      else:
        return (-1, 'Failed to load saved game.')
    elif current_action_code == 9:
      self.save_game('user_data/saved_games/game_file_01.bin')
      return(0, 'Game saved succefully.')
    else:
      return (0, 'Unknown action.')

    return (0, '-')

  def can_line_be_shifted(self, line):    
    """Check if line can be shifted according to 2048 game rules."""
    is_zero = False
    is_not_zero = False
    for cell in line:      
      if not is_zero and cell == 0:
        is_zero = True        
      elif is_zero and cell != 0:
        is_not_zero = True        
        break

    return is_zero and is_not_zero

  def can_line_be_summed(self, line):
    """Check if line can be summed according to 2048 game rules."""
    not_zero_cell = -1
    res = False
    for cell in line:
      if cell != 0 and not_zero_cell == -1:
        not_zero_cell = cell
      elif cell != 0 and not_zero_cell == cell:
        res = True
        break
      elif cell != 0:
        not_zero_cell = cell
    return res  

  def can_make_move_in_direction(self, direction_code: str) -> bool:
    """Check the ability to go in the direction."""
    can_be_moved_in_direction = False
    for line_number in range(self.__game_field_size):
      line = self.get_line(direction_code, line_number)
      if self.can_line_be_shifted(line) or self.can_line_be_summed(line):
        can_be_moved_in_direction = True
        break
    return can_be_moved_in_direction
    
  def get_directions_to_move(self):
    """Get directions to move."""
    directions_to_move = {
      0: False, # up
      1: False, # left
      2: False, # down
      3: False, # right
    }

    for direction in directions_to_move.keys():
      directions_to_move[direction] = self.can_make_move_in_direction(direction)

    return directions_to_move

  def is_game_over(self, directions_to_go) -> bool:
    """Check if game is over."""
    return not any(directions_to_go.values())

  def start_new_game(self):
    """Start new game"""
    self.__game_field = [[0]*4 for i in range(4)]
    self.__game_score = 0
    self.__game_field_size = 4

    self.__prev_game_field_state = None
    self.__prev_game_score = 0

    self.__prev_move_code = -1

    self.set_new_value_on_game_field()

  def load_game(self, file_name: str) -> bool:
    r"""Load game state from a file "file_name"."""
    if not os.path.isfile("user_data/saved_games/game_file_01.bin"):
      return False

    with open(file_name, 'rb') as f:
      game_data = pickle.load(f)

    self.__game_field = deepcopy(game_data['game_field'])
    self.__game_score = game_data['game_score']
    self.__game_field_size = game_data['game_field_size']
    self.__prev_game_field_state = deepcopy(game_data['prev_game_field_state'])
    self.__prev_game_score = game_data['prev_game_score']    
    self.__prev_move_code = game_data['prev_move_code']

    return True

    # print('Loading game ... (not implemented yet.)')
    # print(game_data)

  def save_game(self, file_name: str):
    r"""Save game state in a file "file_name"."""

    game_data_to_save: dict = {}
    # Сохраняем данные в файл.
    game_data_to_save['game_field'] = self.__game_field
    game_data_to_save['game_score'] = self.__game_score
    game_data_to_save['game_field_size'] = self.__game_field_size
    game_data_to_save['prev_game_field_state'] = self.__prev_game_field_state
    game_data_to_save['prev_game_score'] = self.__prev_game_score
    game_data_to_save['prev_move_code'] = self.__prev_move_code

    if not os.path.isdir('user_data'):
      os.mkdir('user_data')
      os.mkdir('user_data/saved_games')

    if not os.path.isdir('user_data/saved_games'):
      os.mkdir('user_data/saved_games')

    with open(file_name, 'wb') as f:
      pickle.dump(game_data_to_save, f) 
    

if __name__ == '__main__':
  game = Game2048()
  game.show_score()
  game.show_game_field()
  print('Начало игры, введите help для вывода команд управления')
  user_input = input('> ')

  while user_input != 'exit':
    code, msg = game.game_2048_main(user_input)  
    game.show_score()
    game.show_game_field()
    print(code, msg)
    user_input = input('> ')
