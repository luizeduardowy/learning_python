numer = None
while numer == None:
    try:
        entrada = input('Digite um número: ')
        entrada_float = float(entrada)

        def multiplicar(num_cal):

            def duplicar():
                return num_cal * 2
            
            def triplicar():
                return num_cal * 3
            
            def quadruplicar():
                return num_cal * 4
        
            return [duplicar, triplicar, quadruplicar]
        numer = multiplicar(entrada_float)
        duplicar, triplicar, quadruplicar = numer

        print(f'O seu numero duplicado é {duplicar()}')
        print(f'O seu numero triplicado é {triplicar()}')
        print(f'O seu numero quadruplicado é {quadruplicar()}')
    except ValueError:
        print('Por favor insira um número válido')
        continue