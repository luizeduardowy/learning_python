nome = input('Insira seu nome: ')
tamanho_nome = len(nome)
letra = 0
novo_nome = ''
while letra < tamanho_nome:
    novo_nome += '*' + nome[letra]
    letra += 1
print(novo_nome + '*')