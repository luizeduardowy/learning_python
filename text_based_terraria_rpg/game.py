import json
import numpy as np
import random
import copy
import math

weapon_list = {
    'stick': random.randint(2, 4),
    'wooden_sword': random.randint(3, 6),
    'copper_sword': random.randint(5, 9),
    'iron_sword': random.randint(6, 10)
}
potions_list = {
    'mushroom': 5,
    'lesser_healing_potion': 10,
    'healing_potion': 25,
    'greater_healing_potion': 50,
    'super_healing_potion': 100,
}

name = input('Insert your character´s name: ')
level = 1
exp = 0
exp_needed = 9 + (math.sqrt(level**np.e))
max_health = 9 + round(level ** 1.15) - math.sqrt(math.sqrt(level - level*(np.e/10)))
health = copy.deepcopy(max_health)
damage = round(random.uniform(1, 1.25) * (math.sqrt(level**1.2)))
inventory = ['stick']

player = {
    'name': name,
    'max_health': max_health,
    'health': health,
    'level': level,
    'damage': damage,
    'inventory': inventory
}

enemy = {
    'name': random.choice(
        ['slime'] if level == 1 else
        (['slime', 'zombie'] if 2 <= level <= 5   else ['slime', 'zombie', 'demon eye'] )),

}

enemy_name = random.choice(
        ['slime'] if level == 1 else
        (['slime', 'zombie'] if 2 <= level <= 5   else ['slime', 'zombie', 'demon eye'] ))
enemy_level = round(level * random.uniform(0.85, 1.15))
enemy_max_health = round(random.randint(7, 11) + round(enemy_level ** 1.16) - math.sqrt(math.sqrt(enemy_level - enemy_level*0.25)))
enemy_health = copy.deepcopy(enemy_max_health)

if enemy['name'] == 'slime':
    enemy_damage_range = random.uniform(1.5, 2)
elif enemy['name'] == 'demon eye':
    enemy_damage_range = random.uniform(2, 2.25)
elif enemy['name'] == 'zombie':
    enemy_damage_range = random.uniform(2.25, 2.5)
enemy_damage = round(random.uniform(0.85, 1.25)) * (math.sqrt(level**1.21) * enemy_damage_range)



enemy = {
    'name': enemy_name,
    'level': enemy_level,
    'max_health': enemy_max_health,
    'health': enemy_health,
    'damage': enemy_damage,
}

enemy_health_using = {'health': copy.deepcopy(enemy_health)}

def use_weapon(weapon):
            print(f'{name} decides to attack {enemy_name_using} with a {weapon}')
            enemy_health_using['health'] -= player_damage_dealt

def use_potion(potion):
     print


while True:
    if health > max_health:
        health = max_health
    elif health <= 0:
        print('You died')

    options = set(inventory)
    enemy_damage_dealt = copy.deepcopy(enemy_damage)
    player_damage_dealt = copy.deepcopy(damage)
    # enemy_name_using is the enemy_name being used right now
    enemy_name_using = copy.deepcopy(enemy_name)
    enemy_name_using_capitalize = enemy_name_using.capitalize()

    print(f'A {enemy_name_using} has appeared. What will you do?')
    print(f'{enemy_name_using_capitalize}´s health: {enemy_health_using["health"]}')
    print(f'Options: ')
    for option in options:
        
        if option in weapon_list:
            if option == 'stick':
                print(f'Poke the {enemy_name_using} with your mighty... stick?(why)')
            elif option == 'wooden_sword':
                print(f'Attack the {enemy_name_using} with your wooden sword(still just a fancy stick)')
            elif option == 'copper_sword':
                print(f'Attack the {enemy_name_using} with your copper sword')
            elif option == 'iron':
                 ...
        elif option in potions_list:
            ...
        item_chosen = input('Insert your choice here: ')
        if item_chosen in weapon_list:
            if item_chosen in inventory:
                item_chosen_replace = item_chosen.replace('_', ' ')
                use_weapon(item_chosen_replace)
                print(f'Enemy health is now: {enemy_health_using['health']}')
            else:
                print('Please insert a valid option')