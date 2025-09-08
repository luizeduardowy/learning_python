import cmath
sol1 = None
sol2 = None
while sol1 is None and sol2 is None:
    try:
        a = float(input('Enter a(the quadratic formula is the following: x = -b (+ or -) sqrt(b^2 - 4ac)\n                                                    --------------------------\n                                                                2a): '))
        b = float(input('Enter b(the quadratic formula is the following: x = -b (+ or -) sqrt(b^2 - 4ac)\n                                                    --------------------------\n                                                                2a): '))
        c = float(input('Enter c(the quadratic formula is the following: x = -b (+ or -) sqrt(b^2 - 4ac)\n                                                    --------------------------\n                                                                2a): '))
        d = (b**2) - (4*a*c)
        sol1 = (-b-(cmath.sqrt(d)))/(2*a)
        sol2 = (-b+(cmath.sqrt(d)))/(2*a)
        print(f'The solutions are {sol1} and {sol2}')
    except ValueError:
        print('Please insert valid inputs')
        continue