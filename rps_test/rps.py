import random
import os

def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else: 
        _ = os.system('clear')

user_input = None
bot_input = None
result = None
n_of_games = 0
list_of_games = dict()
games_won = 0
games_lost = 0
games_drawn = 0
difficulty = 0.333333333333
draw_bias = 0.5375

def rps(uinput, binput):
    if uinput == 'rock':
        if binput == 'rock':
            return 'draw'
        elif binput == 'paper':
            return 'bot wins'
        elif binput == 'scissors':
            return 'user wins'
        else:
            return None
    elif uinput == 'paper':
        if binput == 'rock':
            return 'user wins'
        elif binput == 'paper':
            return 'draw'
        elif binput == 'scissors':
            return 'bot wins'
        else:
            return None
    elif uinput == 'scissors':
        if binput == 'rock':
            return 'bot wins'
        elif binput == 'paper':
            return 'user wins'
        elif binput == 'scissors':
            return 'draw'
        else:
            return None
        
while True:
    try: 
        random0_1 = random.uniform(0, 1)
        user_input = (input('Choose rock, paper or scissors or write exit to leave the game: ').lower()).replace(' ', '')
        if user_input == 'exit':
            break
        if difficulty > 0.999999:
            difficulty = 0.999999
        if difficulty >= random0_1: # Bot wins the game
            if user_input == 'rock':
                bot_input = 'paper'
            elif user_input == 'paper':
                bot_input = 'scissors'
            elif user_input == 'scissors':
                bot_input = 'rock'
            else:
                raise NameError
            result = rps(user_input, bot_input)
        elif random0_1 > difficulty and random0_1 <= difficulty + (draw_bias *(1 - difficulty)): # The game is a draw
            if user_input == 'rock':
                bot_input = 'rock'
            elif user_input == 'paper':
                bot_input = 'paper'
            elif user_input == 'scissors':
                bot_input == 'scissors'
            else:
                raise NameError
            result = rps(user_input, bot_input)
        else: # User wins the game
            if user_input == 'rock':
                bot_input = 'scissors'
            elif user_input == 'paper':
                bot_input = 'rock'
            elif user_input == 'scissors':
                bot_input = 'paper'
            else:
                raise NameError
            result = rps(user_input, bot_input)
        clear()
        print(f'You chose {user_input}')
        print(f'The bot chose {bot_input}')

        if result == 'user wins':
            print()
            print('You won!')
            print()
            difficulty += 0.01
            n_of_games += 1
            list_of_games[f'Game {n_of_games}'] = 1
        elif result == 'draw':
            print()
            print('It´s a draw.')
            print()
            difficulty += 0.005
            n_of_games += 1
            list_of_games[f'Game {n_of_games}'] = 0
        elif result == 'bot wins':
            print()
            print('The bot won.')
            print()
            n_of_games += 1
            list_of_games[f'Game {n_of_games}'] = -1
        else:
            raise NameError
        

    except NameError:
        print('Please pick a valid option')
        continue
    
# Statistics for how much the bot got better every 10 rounds:



if len(list_of_games) < 10:
    for game_number, game_state in list_of_games:
        if game_state == 1:
            games_won += 1
        elif game_state == 0:
            games_drawn += 1
        elif game_state == -1:
            games_lost += 1
    print(f'Of the {n_of_games} games that you played, you won {games_won} of them')
    print(f'Of the {n_of_games} games that you played, {games_drawn} of them were a draw')
    print(f'Of the {n_of_games} games that you played, you lost {games_lost} of them')