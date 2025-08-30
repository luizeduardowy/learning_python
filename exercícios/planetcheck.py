i = 0
while i != None:
	i_str = input('Insira um número inteiro de 1-8: ')
	planetas = ['Mercúrio', 'Vênus', 'Terra', 'Marte', 'Júpiter', 'Saturno', 'Urano', 'Netuno']
	#               0          1        2        3         4          5         6        7
	material = ['rochoso', 'rochoso', 'rochoso', 'rochoso', 'gasoso', 'gasoso', 'gasoso', 'gasoso']
	            #   0          1          2          3          4         5         6         7
	habitavel = ['não é', 'não é', 'é', 'não é', 'não é', 'não é', 'não é', 'não é']

	try:
		i = int(i_str)
		if i >= 1 and i <= 8:
			print(f'O planeta {planetas[i-1]} é {material[i-1]} e {habitavel[i-1]} habitável')
			i = None
		else:
			print('Por favor insira um número entre 1 e 8')
			continue
	except ValueError:
		print('Por favor insira um número inteiro')