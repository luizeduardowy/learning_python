hora = input('Que horas são(Ex: 14.53): ')
try:
    float(hora) == hora
    if float(hora) >= 7 and float(hora) < 12:
        print('Bom dia')
    elif float(hora) >= 12 and float(hora) < 18:
        print('Boa tarde')
    elif (float(hora) >= 18 and float(hora) <= 24) or (float(hora) >= 0 and float(hora) < 7):
        print('Boa noite')
    elif (float(hora)) > 24 or (float(hora)) < 0:
        print('Insira uma hora válida')
except ValueError:
    print('Insira uma hora válida')