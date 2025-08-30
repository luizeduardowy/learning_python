cpf = 0
while cpf != None:
    cpf_str = input('Insira os 9 primeiros números de um cpf(Ex: 123.456.789): ')

    if len(cpf_str) == 11:
        cpf_str = (cpf_str.split('.'))

        if len(cpf_str) == 3 and len(cpf_str[0]) == 3 and len(cpf_str[1]) == 3 and len(cpf_str[2]) == 3:
            cpf_str = cpf_str[0] + cpf_str[1] + cpf_str[2]
        
        else:
            print('Por favor insira um cpf válido')
        if len(cpf_str) == 9:

            try:
                
                cpf = int(cpf_str)

                cpf_list = list(cpf_str)
                cpf_list2 = cpf_list[0] * 10 + cpf_list[1] * 9 + cpf_list[2] * 8 + cpf_list[3] * 7 + cpf_list[4] * 6 + cpf_list[5] * 5 + cpf_list[6] * 4 + cpf_list[7] * 3 + cpf_list[8] * 2
                cpf_list3 = cpf_list2 * 10
                cpf_list4 = cpf_list3 % 11

                if cpf_list4 <= 9:
                    ...
            except:
                ...