i = 0
lista = []
soma = 0
import os
def clear():
    if os.name ==  'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')
while i <= 9:
    numero = input(f'Insira um número inteiro ({i + 1}/10): ')
    try:
        numero = int(numero)
        soma += numero
        lista.append(numero)
        i += 1
    except (TypeError, ValueError):
        print('Por favor escreva um número inteiro')
clear()
print(f'A soma dos números {lista} é igual a {soma}')
