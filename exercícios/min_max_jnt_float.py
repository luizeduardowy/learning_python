lista = []
i = 0
import os
def clear():
    if os.name ==  'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')
while i < 5:
    numero = input(f'Insira um número ({i + 1}/5): ')

    try:
        numero = float(numero)
        lista.append(numero)
        i += 1
    except ValueError:
        print('Por favor insira um número')

clear()
print(f'Dos números {lista}, {max(lista)} é o maior e\n{min(lista)} é o menor')