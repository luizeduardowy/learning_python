# The print function is a function used to write almost anything
print("Hello World!")
print(1234567890)
print(3.14159265358979323846260338327950288419716939937510582097494459230781640628620898628034825342117067, end="\n\n")


# It's also  possible to mess with the separator between multiple arguments in print and the end of print
print(end="-3,-2,-1,0,")
print(1, 2, 3, 4, 5, 6, sep=",", end="\n\n")


# There are several types of values, such as numbers (int, float, complex(precisa da função complex(r, i), with "r" and "i" being real numbers)), bool(True or False), strings(str), sequences(list, tuple, range()), sets(set and frozenset), dictionaries(dict), and more. (see https://docs.python.org/3.13/library/stdtypes.html# for more details)

print("1" + f" is a {type(1)}") # int
print("3.141592653589793238462643" + f" is a {type(3.141592653589793238462643)}") # float
print("2 + 1i" + f" is a {type(complex(2, 1))}") # complex (Actually uses j instead of i, but you get the point)
print("True" + f" is a {type(True)}") # bool
print("Hello World!" + f" is a {type("Hello World!")}") # str
print("[1, 2]" + f" is a {type([1, 2])}") # list
print("(1, 2)" + f" is a {type((1, 2))}") # tuple
print(f"range(3) ou {range(3)}" + f" is a {type(range(3))}") # range (starts at 0)
print("{'any type', 'any type'}" + f" is a {type({'any type', 'any type'})}") # set
print("{'key': 'value'}" + f" is a {type({'key': 'value'})}") # dict