import decimal
import math

def rounder(number, ndigits):
    number = round(number, ndigits)
    number = str(number)
    if len(number) < ndigits + 2:
        while len(number) < ndigits + 2:
            number = number + "0"
    return number

divisor = 0.05
counter = 0
print("Graph of 1 /(n)")
print("@ = 0.05 units")
while divisor < 5:
    graph_bar = "@"
    graph_bar_size = graph_bar * round((round(1 / (divisor), 2)) / 0.05)
    if len(graph_bar_size) > 55:
        graph_bar_size = graph_bar * 55
    if round(divisor * 20) % 5 == 0:
        
        print(f"n = {rounder(divisor, 2)}|{graph_bar_size}")
    else:
        print(f"\t|{graph_bar_size}")
    divisor += 0.05