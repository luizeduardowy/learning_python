def product(*args):
    result = 1
    for number in args:
        result *= number
    return result
numbers_input = input('Enter numbers separated by spaces:')
try:
    numbers = [int(num) for num in numbers_input.split()]
    print('The product is:', product(*numbers))
except ValueError:
    print('Please enter valid integers.')