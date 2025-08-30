nome = input('Insira seu primeiro nome: ')
try:
    float(nome) == nome
    print('O seu nome não é válido')
except ValueError:
    if (nome):
        if len(nome) > 0 and len(nome) <= 4:
            print('Seu nome é curto')
        elif len(nome) >= 5 and len(nome) <= 6:
            print('Seu nome é normal')
        elif len(nome) >= 7 and len(nome) <= 8:
            print('Seu nome é grande')
        elif len(nome) > 8:
            print('Seu nome é muito grande')
    elif len(nome) <= 0:
        print('O seu nome não é válido')