lista = []
lista_opcao = ['a', 'i', 'l', 'b']

import os

def clear():
    if os.name ==  'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')
        
while True:
    opcao = input('Selecione uma opção \n[a]pagar [i]nserir [l]istar [b]reak(sair do programa): ').lower()
        
    if opcao in lista_opcao:
        if opcao == 'l':
            if len(lista) == 0:
                clear()
                print('Sua lista não tem items')
                
            else:
                clear()
                for i, item in enumerate(lista):
                    print(f'{i} - {item}')
                    
        elif opcao == 'i':
            clear
            inserir = input('Insira um valor: ')
            if len(inserir) == 0:
                clear()
                print('Você não inseriu um valor')
            else:
                lista.append(inserir)

        elif opcao == 'a':
            if not lista:
                print('Não tem nada para apagar')
                continue
            try:
                apagar_str = input('Qual valor você quer apagar(escreva o indice do valor):')
                apagar = int(apagar_str)
                if 0 <= apagar < len(lista):
                    valor_removido = lista.pop(apagar)
                    print(f'O valor {valor_removido} foi removido com sucesso')
                else:
                    print('Por favor escreva um indice válido')
            except ValueError:
                print('Por favor escreva um número correspondente ao indice do valor')
        
        elif opcao == 'b':
            break

    else:
        clear()
        print('Por favor selecione uma opção válida')
print('Saiu do programa com sucesso')