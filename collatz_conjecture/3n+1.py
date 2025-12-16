import copy
import time
import math
import os
def clearscreen():
    if os.name == 'nt':
        _ = os.system('cls')
    else: 
        _ = os.system('clear')
number = int(input("Insert any positive integer to start: "))
variable = copy.deepcopy(number)
endlist = {1, 2, 4}
anotherlist = set()
steps = 0
speed = float(input("Insert the speed of the calculation: "))
while steps <= round(int(number) ** 2) and variable <= round(int(number) ** 3.33333):
    if variable in endlist:
        clearscreen()
        print(f"{variable} was already used, so onto the next number:")
        print()
        endlist.add(number)
        for n in anotherlist:
            endlist.add(n)
        anotherlist.clear()
        number += 1
        variable = copy.deepcopy(number)
        print(f"{number}")
        print()
        steps = 0
        
        time.sleep(0.375 / (math.sqrt(speed ** 0.2)))
    if variable % 2 == 0:
        print(f"{variable} is even, so divide it by 2")
        variable /= 2
        variable = int(variable)
        print(f"You get {variable}")
        anotherlist.add(variable)
        print()
    elif variable % 2 == 1:
        print(f"{variable} is odd, so multiply it by 3 and add 1")
        variable = (variable * 3) + 1
        print(f"You get {variable}")
        anotherlist.add(variable)
        print()
    steps += 1
    time.sleep(1/speed)
print("If you are seeing this message, the Collatz Conjecture is probably true or there is another loop")