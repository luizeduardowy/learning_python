cpf = 0
while cpf != None:
    cpf_input = input('Insira os 9 primeiros números de um cpf(Ex: 123.456.789): ')

    if len(cpf_input) == 11:
        cpf_split = (cpf_input.split('.'))

        if len(cpf_split) == 3 and len(cpf_split[0]) == 3 and len(cpf_split[1]) == 3 and len(cpf_split[2]) == 3:
            cpf_joined = cpf_split[0] + cpf_split[1] + cpf_split[2]
        
        else:
            print('Por favor insira um cpf válido')
            continue

        if len(cpf_joined) == 9:

            try:
                
                cpf_int = int(cpf_joined)

                cpf_list = list(cpf_joined)
                cpf_list2 = int(cpf_list[0]) * 10 + int(cpf_list[1]) * 9 + int(cpf_list[2]) * 8 + int(cpf_list[3]) * 7 + int(cpf_list[4]) * 6 + int(cpf_list[5]) * 5 + int(cpf_list[6]) * 4 + int(cpf_list[7]) * 3 + int(cpf_list[8]) * 2
                cpf_list3 = cpf_list2 * 10
                cpf_list4 = cpf_list3 % 11

                if cpf_list4 <= 9:
                    cpf_final = str(list(cpf_input).append('-' + cpf_list4))

                else:
                    cpf_final = str(list(cpf_input).append('-0'))
        
            except ValueError:
                print('Por favor insira um cpf válido')
                continue

        else:
            print('Por favor insira um cpf válido')
            continue
    else:
        print('Por favor insira um cpf válido')
        continue
print(f'O seu cpf é {cpf_final}')