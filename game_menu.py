class GameMenu:
  def __init__(self):
    self.__menu_command_descriptions = {
      '1': 'Продолжить игру',
      '2': 'Начать новую игру',
      '3': 'Сохранить игру',
      '4': 'Загрузить игру',
      '5': 'Настройки',
      '6': 'Выход из игры'
    }

    self.__menu_command_names_to_command_codes = {
      '1': 1,
      'continue': 1,
      '2': 2,
      'restart': 2,
      '3': 3,
      'save': 3,
      '4': 4,
      'load': 4,
      '5': 5,
      'settings': 5,
      '6': 6,
      'exit': 6,
    }

  def get_menu_command_code_by_command_name(self, menu_comand_name):
    return self.__menu_command_names_to_command_codes[menu_comand_name]

  def show_game_menu(self):
    print('====== Game Menu ======')
    for key, value in self.__menu_command_descriptions.items():
      print(f'{key}. {value}')

  def is_menu_command_name_correct(self, menu_command_name):
    return menu_command_name in self.__menu_command_names_to_command_codes.keys()
  
  def get_menu_command_code_by_command_name(self, menu_command_name):
    return self.__menu_command_names_to_command_codes[menu_command_name]

  def game_menu_main(self, menu_command_name):    
    if not self.is_menu_command_name_correct(menu_command_name):
      return (-1, 'Введен неверный пункт меню')
    
    menu_command_code = self.get_menu_command_code_by_command_name(menu_command_name)
    print(f'{menu_command_code = }')
    print('Введенный пункт меню: ')
    if menu_command_code == 1:
      print('Продолжаем игру.')
    elif menu_command_code == 2:
      print('Начинаем новую игру.')
    elif menu_command_code == 3:
      print('Сохраняю текущую игру.')
    elif menu_command_code == 4:
      print('Загружаю игру.')
    elif menu_command_code == 5:
      print('Настраиваем игру.')
    elif menu_command_code == 6:
      print('Выходим из игры.')

    return (0, 'Ok.')


if __name__ == '__main__':
  game_menu = GameMenu()

  game_menu.show_game_menu()
  menu_command_name = input('> ')
  # game_menu.game_menu_main(menu_command_name)1

  while menu_command_name != 'exit':
    responde_code, responde_msg = game_menu.game_menu_main(menu_command_name)
    input('\nPress enter to coutinue.')
    game_menu.show_game_menu()    
    print(f'{responde_msg=}')
    menu_command_name = input('> ')