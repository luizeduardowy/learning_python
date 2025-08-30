nome = input('Insira seu nome: ')
idade = input('Insira sua idade: ')
if not nome or not idade:
    print('Desculpe, você deixou um (ou mais) lugar(es) vazio(s)')
else:
    if nome and idade:
        print(f'Seu nome é {nome}')
        print(f'Seu nome invertido é {nome[::-1]}')
    if ' ' in nome:
        print('Seu nome tem espaço')
    elif ' ' not in nome:
        print('Seu nome não tem espaço')
    if nome and idade:
        print(f'Seu nome tem {len(nome)} letras')
        print(f'A primeira letra do seu nome é {nome[0]}')
        print(f'A última letra do seu nome é {nome[-1]}')
