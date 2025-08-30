nome = input('Insira seu nome: ')
altura = input('Insira sua altura: ')
peso = input('Insira seu peso: ')


try:
    imc = float(peso) / (float(altura) * float(altura))
    imc2 = f'{imc:.2f}'
    print('O/A ' + nome + ' tem ' + str(altura) + ' de altura,')
    print('pesa ' + str(peso) + ' quilos e seu IMC é')
    print(imc2)
except ZeroDivisionError:
    print('Error - Height not valid \n please insert a valid height')
except ValueError:
    if not isinstance(altura, int) or not isinstance(altura, float) or altura == 0:
        print('Error - Height not valid \n please insert a valid height')
    elif not isinstance(peso, int) or not isinstance(peso, float):
        print('Error - Weight not valid \n please insert a valid weight')
if bool(nome) == False:
    print('Error - Name not valid \n please insert a valid name')