numero = input('Insira um número inteiro: ')
try:
    int(numero) == numero
    if int(numero) % 2 == 0:
        print('O número ' + numero + ' é par')
    elif int(numero) % 2 == 1:
        print('O número ' + numero + ' é ímpar')
except ValueError:
    print('O seu número não é inteiro.')