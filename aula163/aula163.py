def soma(x, y):
    return f'{x} + {y} = {x + y}'


def multiplica(x, y):
    return f'{x} * {y} = {x * y}'


def criar_funcao(funcao, x):
    def interno(y):
        return funcao(x, y)
    return interno

soma_input = input('Insira um número para somar com 5: ')
multiplica_input = input('Insira um número para multiplicar por 10: ')
soma_com_cinco = criar_funcao(soma, 5,)
multiplica_por_dez = criar_funcao(multiplica, 10,)
print(soma_com_cinco, float(soma_input))
print()
print(multiplica_por_dez, float(multiplica_input))