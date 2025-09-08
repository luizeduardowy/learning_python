def parity(numbers):
    return "even" if sum(numbers) % 2 == 0 else "odd"
number_input = input('Enter a number: ')
number = None
while number == None:
    try:
        number = int(number_input)
        print(f'The number {number} is {parity([number])}.')
    except ValueError:
        print('Please enter a valid integer.')