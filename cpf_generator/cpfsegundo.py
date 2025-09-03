cpf = 0
while cpf == 0:
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
                

                cpf_list = list(cpf_joined)
                cpf_list2 = sum((int(cpf_list[i])) * (10 - i) for i in range(9))
                cpf_list3 = cpf_list2 * 10
                cpf_list4 = cpf_list3 % 11
                cpf_subfinal = cpf_list4 if cpf_list4 < 10 else 0

                cpf_input = cpf_joined + str(cpf_subfinal)
                cpf_list_2 = list(cpf_input)

                cpf_list2_2 = sum(int(cpf_list_2[i]) * (11-i) for i in range(10))
                cpf_list3_2 = cpf_list2_2 * 10
                cpf_list4_2 = cpf_list3_2 % 11
                cpf2 = cpf_list4_2 if cpf_list4_2 < 10 else 0
                cpf_input += str(cpf2)
                
                cpf_final = f'{cpf_split[0]}.{cpf_split[1]}.{cpf_split[2]}-{cpf_subfinal}{cpf2}'
                print(f'O seu CPF é válido\nCPF completo: {cpf_final}')
                cpf = cpf_final

            except ValueError:
                print('Por favor insira um cpf válido')
                continue

        else:
            print('Por favor insira um cpf válido')
            continue
    else:
        print('Por favor insira um cpf válido')
        continue