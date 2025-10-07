import copy
products = [
    {'name': 'Product 5', 'price': 10.00},
    {'name': 'Product 1', 'price': 22.32},
    {'name': 'Product 2', 'price': 10.11},
    {'name': 'Product 3', 'price': 105.87},
    {'name': 'Product 4', 'price': 69.90},
]
new_products = []

for dictionary in products:
    new_products.append(copy.deepcopy(dictionary))

for dictionary in new_products:
    for key, value in dictionary.items():
        if key == 'price':
            value += round(0.1 * value, ndigits=2) if key == 'price' else 'do nothing'
            dictionary['price'] = round(value, ndigits=2) if key == 'price' else 'do nothing'

print('New Products(adjusted for inflation): ')
print(' ')
for dictionary in new_products:
    print(f'Product: {dictionary['name']}   Price: {dictionary['price']}')
    print(' ')

products_sorted_by_name = list()
for dictionary in products:
    products_sorted_by_name.append(copy.deepcopy(dictionary))
    products_sorted_by_name = sorted(products_sorted_by_name, key=lambda item: item['name'], reverse=True)
print('Products sorted by name(in reverse):')
print(' ')

for dictionary in products_sorted_by_name:
    print(f'Product: {dictionary['name']}   Price: {dictionary['price']}')
    print(' ')

products_sorted_by_price = list()
for dictionary in products:
    products_sorted_by_price.append(copy.deepcopy(dictionary))
    products_sorted_by_price = sorted(products_sorted_by_price, key=lambda item: item['price'])
print('Products sorted by price: ')
print(' ')
for dictionary in products_sorted_by_price:
    print(f'Product: {dictionary['name']}   Price: {dictionary['price']}')
    print(' ')