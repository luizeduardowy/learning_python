fibonacci = None
import os
def clear():
    if os.name ==  'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

while fibonacci == None:
    fibonacci = None
    lista = [0, 1]
    proximo = lista[-1] + lista[-2]
    fibonacci_str = input('Quantos números da sequência Fibonacci você quer visualizar: ')

    try:
        fibonacci = int(fibonacci_str)
        if fibonacci <= 2:
            clear()
            print('Por favor insira um número inteiro maior que 2')
            continue

        while len(lista) < fibonacci:
            lista.append(proximo)
            proximo = lista[-1] + lista[-2]
            clear()
            print(f'Calculando({(len(lista))}/{fibonacci})...')

    except ValueError:
        clear()
        print('Por favor insira um número inteiro')
        continue

    print(f'Os primeiros {fibonacci} números da sequência Fibonacci são {lista}')