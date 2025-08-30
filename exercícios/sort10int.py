i = 0
lista = []
lista_sorted = lista

import os
def clear():
    if os.name ==  'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

while i < 10:
    numero_str = input(f'Insira um número inteiro ({i+1}/10): ')
    try:
        numero = int(numero_str)
        lista.append(numero)
        lista_sorted = lista
        i += 1
    except ValueError:
        print('Por favor insira um número inteiro')

lista_sorted = sorted(lista)
lista_sorted_reverse = sorted(lista, reverse = True)
clear()

lista_str = ', '.join(map(str, lista))
lista_sorted_str = ', '.join(map(str, lista_sorted))
lista_sorted_reverse_str = ', '.join(map(str, lista_sorted_reverse))

print(f'Números inseridos:  {lista_str}')
print(f'Números ordenados:  {lista_sorted_str}')
print(f'Números em ordem inversa:  {lista_sorted_reverse_str}')