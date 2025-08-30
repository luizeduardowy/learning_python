numero = None
import os

def clear():
    if os.name ==  'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

while numero == None:

    numero = None
    fibonacci10 = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    numero_str = input('Insira um número inteiro: ')

    try:
        numero = int(numero_str)

        if numero in fibonacci10:
            print(f'O número {numero} é um dos primeiros\ndez números da sequência Fibonacci')
        else:
            print(f'O número {numero} não é um dos primeiros\ndez números da sequência Fibonacci ')

    except ValueError:
        clear()
        print('Por favor insira um número inteiro')
        continue