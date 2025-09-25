import os

def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else: 
        _ = os.system('clear')

list_of_list_of_naturals = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [9, 1, 8, 9, 9, 7, 2, 1, 6, 8],
    [1, 3, 2, 2, 8, 6, 5, 9, 6, 7],
    [3, 8, 2, 8, 6, 7, 7, 3, 1, 9],
    [4, 8, 8, 8, 5, 1, 10, 3, 1, 7],
    [1, 3, 7, 2, 2, 1, 5, 1, 9, 9],
    [10, 2, 2, 1, 3, 5, 10, 5, 10, 1],
    [1, 6, 1, 5, 1, 1, 1, 4, 7, 3],
    [1, 3, 7, 1, 10, 5, 9, 2, 5, 7],
    [4, 7, 6, 5, 2, 9, 2, 1, 2, 1],
    [5, 3, 1, 8, 5, 7, 1, 8, 8, 7],
    [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
]
def find_first_duplicate(list_of_naturals):
    numbers_checked = set()
    first_duplicate = -1


    for natural in list_of_naturals:
        if natural in numbers_checked:
            first_duplicate = natural
            return first_duplicate
        
        numbers_checked.add(natural)

    return first_duplicate

for list_ in list_of_list_of_naturals:
    print(find_first_duplicate(list_))