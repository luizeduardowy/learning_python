import json
import numpy as np
import random
import copy
import math
import os

def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else: 
        _ = os.system('clear')

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
    'exp': exp,
    'exp_needed': exp_needed,
    'inventory': inventory
}
def random_enemy(level):
    enemy = {}
    if level == 1:
        enemy['name'] = random.choice(['slime'])
    elif 2 <= level <= 5:
        enemy['name'] = random.choice(['slime', 'zombie'])
    else:
        enemy['name'] = random.choice(['slime', 'zombie', 'demon eye'])
    enemy['level'] = max(1, round(level * random.uniform(0.85, 1.15)))
    enemy['max_health'] = round(random.randint(7, 11) + round(enemy['level'] ** 1.16) - math.sqrt(math.sqrt(enemy['level'] - enemy['level'] * 0.25)))
    enemy['health'] = copy.deepcopy(enemy['max_health'])

    if enemy['name'] == 'slime':
        enemy_damage_range = random.uniform(1.5, 2)
    elif enemy['name'] == 'demon eye':
        enemy_damage_range = random.uniform(2, 2.25)
    elif enemy['name'] == 'zombie':
        enemy_damage_range = random.uniform(2.25, 2.5)
    enemy['damage'] = round(random.uniform(0.85, 1.25)) * round(math.sqrt(level**1.21) * enemy_damage_range)
    return {
        'name': enemy['name'],
        'level': enemy['level'],
        'max_health': enemy['max_health'],
        'health': enemy['health'],
        'damage': enemy['damage'],
    }



enemy = random_enemy(level)
enemy_health_using = {'health': enemy['health']}


def use_weapon(weapon):
    clear()
    print(f'{name} decides to attack {enemy['name']} with a {weapon}')
    enemy_health_using['health'] -= player_damage_dealt
    print(f'{player['name']} dealt {player_damage_dealt} damage!')

def use_potion(potion):
    global health
    clear()
    if health >= max_health or health + potions_list[potion] > max_health + (potions_list[potion])/2:
        health += (potions_list[potion])/2
        print(f'You are already at your maximum state but the {potion} changes your health temporarily')
    elif health <= 0:
        print('You died')
    else:
        health += potions_list[potion]
    player['health'] = health
    print(f'{name} decides to use {potion}')
    inventory.remove(potion)
    
    

def enemy_appear():
    global enemy, enemy_health_using
    enemy = random_enemy(level)
    enemy_health_using = {'health': enemy['health']}
    
    print(f'A {enemy['name']} has appeared. What will you do?')
    print(f"{enemy['name'].capitalize()}´s health: {enemy_health_using["health"]}")
    print(f"{enemy['name'].capitalize()}´s level: {enemy['level']}")
    print(f'Options: ')

print(f'A {enemy['name']} has appeared. What will you do?')
print(f'{enemy['name'].capitalize()}´s health: {enemy_health_using["health"]}')
print(f'{enemy['name'].capitalize()}´s level: {enemy['level']}')
print(f'Options: ')
while True:
    if health > max_health:
        health = max_health
    elif health <= 0:
        print('You died')
        exit()
    if enemy_health_using['health'] > enemy['max_health']:
        enemy_health_using['health'] = enemy['max_health']
    elif enemy_health_using['health'] <= 0:
        print('You have defeated the enemy')
        if enemy['name'] == 'slime':
            exp += round(random.uniform(0.25, 0.4) * exp_needed * math.sqrt(enemy['level']))
            inventory.append('mushroom')
            print('You got a mushroom!')
            
        elif enemy['name'] == 'demon eye':
            exp += round(random.uniform(0.35, 0.55) * exp_needed * math.sqrt(enemy['level'] ** 1.05))
            
        elif enemy['name'] == 'zombie':
            exp += round(random.uniform(0.50, 0.75) * exp_needed * math.sqrt(enemy['level'] ** 1.15))
        while exp >= exp_needed:
            exp -= exp_needed
            level += 1
            exp_needed = 9 + round(math.sqrt(level**np.e))
            max_health = 9 + round(level ** 1.15) - math.sqrt(math.sqrt(level - level*(np.e/10)))
            health = max_health
            damage = round(random.uniform(1, 1.25) * math.sqrt(level**1.2))
            print(f'You leveled up! You are now level {level}.')
        print(f'Exp: {exp}/{exp_needed}({round((exp/exp_needed)* 1000) / 10}%)')
        player['level'] = level
        player['exp'] = exp
        player['exp_needed'] = exp_needed
        player['max_health'] = max_health
        player['health'] = health
        player['damage'] = damage
        player['inventory'] = inventory
        enemy_appear()

    options = set(inventory)
    enemy_damage_dealt = copy.deepcopy(enemy['damage'])
    player_damage_dealt = copy.deepcopy(player['damage'])

    for option in options:
        
        if option in weapon_list:
            if option == 'stick':
                print(f'Poke the {enemy['name']} with your mighty... stick?(why)')
            elif option == 'wooden_sword':
                print(f'Attack the {enemy['name']} with your wooden sword(still just a fancy stick)')
            elif option == 'copper_sword':
                print(f'Attack the {enemy['name']} with your copper sword')
            elif option == 'iron_sword':
                 print(f'Slice the {enemy['name']} with your iron sword')
        elif option in potions_list:
            if option == 'mushroom':
                print(f'Eat a mushroom(I don`t recommend doing that)')
            elif option == 'lesser_healing_potion':
                print(f'Drink a lesser healing potion')
            elif option == 'healing_potion':
                print(f'Drink a healing potion')
            elif option == 'super_healing_potion':
                print(f'Drink a super healing potion("Legend says only those who are worthy of drinking this can survive it")')
    item_chosen = input('Insert your choice here: ')    
        
        
    if item_chosen in weapon_list:
        if item_chosen in inventory:
            item_chosen_replace = item_chosen.replace('_', ' ')
            use_weapon(item_chosen_replace)
            print(f'{enemy['name'].capitalize()}´s health is now {enemy_health_using["health"]}')
        else:
            print('Please insert a valid option')
    elif item_chosen in potions_list:
        if item_chosen in inventory:
            item_chosen_replace = item_chosen.replace('_', ' ')
            use_potion(item_chosen_replace)
        else:
            print('Please insert a valid option')
            continue
    
    print(f'What will you do?')
    print(f'{enemy['name'].capitalize()}´s health: {enemy_health_using["health"]}')
    print(f'{enemy['name'].capitalize()}´s level: {enemy['level']}')
    print(f'Options: ')