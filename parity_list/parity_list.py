i = 0
lista = []
par = 0
impar = 0
while i <= 9:
    numero = input('Escreva um número inteiro: ')
    try:
        numero = int(numero)
        i += 1
        lista.append(numero)
        if numero % 2 == 0:
            par += 1
        else:
            impar += 1
    except (TypeError, ValueError):
        print('Por favor escreva um número inteiro')
if par == 1:
    print(f'Dos números: {lista}, {par} deles é par e {impar} são ínpares')
elif impar == 1:
    print(f'Dos números: {lista}, {par} deles são pares e {impar} deles é ínpar')
else:
    print(f'Dos números: {lista}, {par} deles são pares e {impar} deles são ínpares')