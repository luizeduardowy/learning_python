qtd_coluna = input('Escreva a quantidade de colunas de uma tabela: ')
qtd_linha = input('Escreva a quantidade de linhas de uma tabela: ')
linha = 1
coluna = 1
try:
    qtd_coluna = int(qtd_coluna)
    qtd_linha = int(qtd_linha)
    while linha <= int(qtd_linha):
        coluna = 1
        while coluna <= (qtd_coluna):
            print(f'{linha=} {coluna=}')
            coluna += 1
        linha +=1
    print('Acabou')
except ValueError:
    print('Erro - Insira dois números inteiros')