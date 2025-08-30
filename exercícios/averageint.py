numeros_str = input('Insira a quantidade de números a inserir: ')
i = 0
lista = []
media = 0
sou_quase_inutil = 0
import os
def clear():
    if os.name ==  'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

try:
    numeros = int(numeros_str)
    if numeros == 0 or not(len(numeros_str)):
        print('Por favor insira um número inteiro positivo')
        sou_quase_inutil = 1

    else:
        media /= numeros
    numeros = int(numeros)

    while i < numeros:
        try:
            numero = input(f'Insira um número ({i+1}/{numeros}): ')
            numero = int(numero)
            lista.append(numero)
            media += numero
            i += 1
        
        except (ValueError, TypeError):
            if sou_quase_inutil == 0:
                print('Por favor insira um número inteiro')
            
    media /= numeros
    clear()
    print(f'Dos números {lista}, a média deles é {media}')

except (ValueError):
    if sou_quase_inutil == 0:
        print('Por favor insira um número inteiro')