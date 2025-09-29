import json
import numpy as np
import random
import copy
import math
from clear import clear

weapon_list = {
    'stick': random.uniform(1.25, 1.625),
    'wooden_sword': random.uniform(1.3125, 2.25),
    'copper_sword': random.uniform(2.25, 3),
    'zombie_arm': random.uniform(3, 4.25),
    'iron_sword': random.uniform(4.5, 5.75),
    'diamond_sword': random.uniform(6.125, 7.5),
}
potions_list = {
    'mushroom': 5,
    'lesser_healing_potion': 10,
    'healing_potion': 25,
    'greater_healing_potion': 50,
    'super_healing_potion': 100,
}
materials_list = {
    'copper_bar': 'copper_bar',
    'iron_bar': 'iron_bar',
    'diamond': 'diamond',
}

name = input('Insert your character´s name: ')
level = 1
exp = 0
exp_needed = 9 + (math.sqrt(level**np.e))
max_health = round(10 + (level ** 1.15) - round(math.sqrt(math.sqrt(level - level*(np.e/9)))))
health = copy.deepcopy(max_health)
damage = round(random.uniform(0.850, 1.1825) * (math.sqrt(level**1.2)))
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
        enemy['name'] = random.choice(['slime', 'demon eye'])
    else:
        enemy['name'] = random.choice(['slime', 'demon eye', 'zombie'])
    enemy['level'] = max(1, round(level * random.uniform(0.85, 1.15)))
    enemy['max_health'] = round(random.randint(5, 8) + round(enemy['level'] ** 1.16) - math.sqrt(math.sqrt(enemy['level'] - enemy['level'] * 0.25)))
    enemy['health'] = copy.deepcopy(enemy['max_health'])

    if enemy['name'] == 'slime':
        enemy_damage_range = random.uniform(1, 1.25)
    elif enemy['name'] == 'demon eye':
        enemy_damage_range = random.uniform(1.125, 1.5)
    elif enemy['name'] == 'zombie':
        enemy_damage_range = random.uniform(1.375, 1.875)
    enemy['damage'] = round(round(random.uniform(0.75, 1)) * round(math.sqrt(level**1.21) * enemy_damage_range))
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
    print('')

def use_potion(potion):
    global health
    clear()
    if health >= max_health or health + potions_list[potion] > max_health:
        health = max_health
    elif health <= 0:
        print('You died 🪦')
    else:
        health += potions_list[potion]
    player['health'] = health
    print(f'{name} decides to use {potion}')
    print(f'{player['name']}´s health is now {player['health']}/{player["max_health"]}({round((player['health']/player["max_health"])*1000)/10}%)')
    inventory.remove(potion)
    print(' ')

def enemy_attack(enemy_):
    player['health'] -= round(enemy['damage'])
    if enemy_ == 'slime':
        print(f'Slime decides to attack {player['name']} by hopping onto him/her')
    elif enemy_ == 'demon eye':
        print(f'Demon eye decides to attack {player['name']} by hitting him/her')
    elif enemy_ == 'zombie':
        print(f'Zombie decides to attack {player['name']}by biting him/her')
    print(f'{enemy["name"].capitalize()} dealt {enemy['damage']} damage')
    print(' ')
    print(f'{player['name']}´s health is now {player['health']}/{player['max_health']}({round((player['health']/player['max_health'])*1000)/10}%)')
    print(' ')
    
    

def enemy_appear():
    global enemy, enemy_health_using
    enemy = random_enemy(level)
    enemy_health_using = {'health': enemy['health']}
    
    print(f'A {enemy['name']} has appeared. What will you do?')
    print(f"{enemy['name'].capitalize()}´s health: {enemy_health_using["health"]}")
    print(f"{enemy['name'].capitalize()}´s level: {enemy['level']}")
    print(' ')
    print(f'{player['name']}´s health is now {player['health']}/{player['max_health']}({round((player['health']/player['max_health'])*1000)/10}%)')
    
    print(' ')
    print(f'Options: ')
    print(' ')

def enemy_die():
    if enemy_health_using['health'] > enemy['max_health']:
        enemy_health_using['health'] = enemy['max_health']
    elif enemy_health_using['health'] <= 0:
        clear()
        print('You have defeated the enemy')
        print(' ')
        if enemy['name'] == 'slime':
            exp_gained_slime = round(random.uniform(0.25, 0.4) * exp_needed * math.sqrt(enemy['level']))
            exp += exp_gained_slime
            inventory.append('mushroom')
            print('You got a mushroom!')
            if random.uniform(0, 1) <= 0.3333:
                inventory.append('stick')
                print('You got a stick!')
                if inventory.count('stick') >= 2:
                    if inventory.count('wooden_sword') < 1:
                        if input('Do you want to use your 2 sticks to make a wooden sword(one of\nthe sticks is conserved in the process)(type anything for yes(spaces count)\nand press enter for no)? '):
                            inventory.remove('stick')
                            inventory.append('wooden_sword')
                            print('-1 stick')
                            print('You got a wooden sword!')
            print(' ')
            
            
        elif enemy['name'] == 'demon eye':
            exp_gained_demon_eye = round(random.uniform(0.35, 0.55) * exp_needed * math.sqrt(enemy['level'] ** 1.05))
            exp += exp_gained_demon_eye
            if random.uniform(0, 1) <= 0.2:
                inventory.append('copper_bar')
                print('You got a copper bar!')
                if inventory.count('copper_bar') >= 2 and inventory.count('stick') >= 1:
                    if inventory.count('copper_sword') < 1:
                        if input('Do you want to use 2 of your copper bars and a stick to make an copper sword\n(type anything for yes(spaces count) and press\n and press enter for no)?'):
                            inventory.remove('stick')
                            print('-1 stick')
                            print(' ')
                            inventory.remove('copper_bar')
                            inventory.remove('copper_bar')
                            print('-2 copper bars')
                            print(' ')
                            inventory.append('copper_sword')
                            print('You got an copper sword!')
            elif random.uniform(0, 1) <= 0.05:
                inventory.append('iron_bar')
                print('You got a iron bar!')
                if inventory.count('iron_bar') >= 2 and inventory.count('copper_sword') >= 1:
                    if inventory.count('iron_sword') < 1:
                        if input('Do you want to use 2 of your iron bars and your copper sword\n to make an iron sword(type anything for yes(spaces count) and\n press enter for no)?'):
                            inventory.remove('copper_sword')
                            print('-1 copper sword')
                            print(' ')
                            inventory.remove('iron_bar')
                            inventory.remove('iron_bar')
                            print('-2 iron bars')
                            print(' ')
                            inventory.append('iron_sword')
                            print('You got an iron sword')

            
        elif enemy['name'] == 'zombie':
            exp_gained_zombie = round(random.uniform(0.50, 0.75) * exp_needed * math.sqrt(enemy['level'] ** 1.15))
            exp += exp_gained_zombie
            if random.uniform(0, 1) <= 0.090625:
                inventory.append('zombie_arm')
                print('You got a zombie arm!')
        while exp >= exp_needed:
            exp -= exp_needed
            level += 1
            exp_needed = 9 + round(math.sqrt(level**np.e))
            max_health = round(10 + (level ** 1.15) - round(math.sqrt(math.sqrt(level - level*(np.e/9)))))
            health = max_health
            damage = round(random.uniform(1, 1.25) * math.sqrt(level**1.2))
            print(f'You leveled up! You are now level {level}.')

        if enemy['name'] == 'slime':
            print(f'+{exp_gained_slime} exp!')
        elif enemy['name'] == 'demon eye':
            print(f'+{exp_gained_demon_eye} exp!')
        elif enemy['name'] == 'zombie':
            print(f'+{exp_gained_zombie} exp!')
            
        print(f'Exp: {exp}/{exp_needed}({round((exp/exp_needed)* 1000) / 10}%)')
        max_health = round(10 + (level ** 1.15) - round(math.sqrt(math.sqrt(level - level*(np.e/9)))))
        player['level'] = level
        player['exp'] = exp
        player['exp_needed'] = exp_needed
        player['max_health'] = max_health
        player['damage'] = damage
        player['inventory'] = inventory
        enemy_appear()

print(f'A {enemy['name']} has appeared. What will you do?')
print(f'{enemy['name'].capitalize()}´s health: {enemy_health_using["health"]}')
print(f'{enemy['name'].capitalize()}´s level: {enemy['level']}')
print(' ')
print(f'Options: ')
while True:
    if health > max_health:
        health = max_health
    elif player['health'] <= 0:
        print('You died 🪦')
        exit()
    if enemy_health_using['health'] > enemy['max_health']:
        enemy_health_using['health'] = enemy['max_health']
    elif enemy_health_using['health'] <= 0:
        clear()
        print('You have defeated the enemy')
        print(' ')
        if enemy['name'] == 'slime':
            exp_gained_slime = round(random.uniform(0.25, 0.4) * exp_needed * math.sqrt(enemy['level']))
            exp += exp_gained_slime
            inventory.append('mushroom')
            print('You got a mushroom!')
            if random.uniform(0, 1) <= 0.3333:
                inventory.append('stick')
                print('You got a stick!')
                if inventory.count('stick') >= 2:
                    if inventory.count('wooden_sword') < 1:
                        if input('Do you want to use your 2 sticks to make a wooden sword(one of\nthe sticks is conserved in the process)(type anything for yes(spaces count)\nand press enter for no)? '):
                            inventory.remove('stick')
                            inventory.append('wooden_sword')
                            print('-1 stick')
                            print('You got a wooden sword!')
            print(' ')
            
            
        elif enemy['name'] == 'demon eye':
            exp_gained_demon_eye = round(random.uniform(0.35, 0.55) * exp_needed * math.sqrt(enemy['level'] ** 1.05))
            exp += exp_gained_demon_eye
            if random.uniform(0, 1) <= 0.2:
                inventory.append('copper_bar')
                print('You got a copper bar!')
                if inventory.count('copper_bar') >= 2 and inventory.count('stick') >= 1:
                    if inventory.count('copper_sword') < 1:
                        if input('Do you want to use 2 of your copper bars and a stick to make an copper sword\n(type anything for yes(spaces count) and press\n and press enter for no)?'):
                            inventory.remove('stick')
                            print('-1 stick')
                            print(' ')
                            inventory.remove('copper_bar')
                            inventory.remove('copper_bar')
                            print('-2 copper bars')
                            print(' ')
                            inventory.append('copper_sword')
                            print('You got an copper sword!')
            elif random.uniform(0, 1) <= 0.05:
                inventory.append('iron_bar')
                print('You got a iron bar!')
                if inventory.count('iron_bar') >= 2 and inventory.count('copper_sword') >= 1:
                    if inventory.count('iron_sword') < 1:
                        if input('Do you want to use 2 of your iron bars and your copper sword\n to make an iron sword(type anything for yes(spaces count) and\n press enter for no)?'):
                            inventory.remove('copper_sword')
                            print('-1 copper sword')
                            print(' ')
                            inventory.remove('iron_bar')
                            inventory.remove('iron_bar')
                            print('-2 iron bars')
                            print(' ')
                            inventory.append('iron_sword')
                            print('You got an iron sword')

            
        elif enemy['name'] == 'zombie':
            exp_gained_zombie = round(random.uniform(0.50, 0.75) * exp_needed * math.sqrt(enemy['level'] ** 1.15))
            exp += exp_gained_zombie
            if random.uniform(0, 1) <= 0.090625:
                inventory.append('zombie_arm')
                print('You got a zombie arm!')
        while exp >= exp_needed:
            exp -= exp_needed
            level += 1
            exp_needed = 9 + round(math.sqrt(level**np.e))
            max_health = round(10 + (level ** 1.15) - round(math.sqrt(math.sqrt(level - level*(np.e/9)))))
            health = max_health
            damage = round(random.uniform(1, 1.25) * math.sqrt(level**1.2))
            print(f'You leveled up! You are now level {level}.')

        if enemy['name'] == 'slime':
            print(f'+{exp_gained_slime} exp!')
        elif enemy['name'] == 'demon eye':
            print(f'+{exp_gained_demon_eye} exp!')
        elif enemy['name'] == 'zombie':
            print(f'+{exp_gained_zombie} exp!')
            
        print(f'Exp: {exp}/{exp_needed}({round((exp/exp_needed)* 1000) / 10}%)')
        max_health = round(10 + (level ** 1.15) - round(math.sqrt(math.sqrt(level - level*(np.e/9)))))
        player['level'] = level
        player['exp'] = exp
        player['exp_needed'] = exp_needed
        player['max_health'] = max_health
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
                print(f'Attack the {enemy['name']} with your zombie arm(gross)')
            elif option == 'zombie_arm':
                print(f'Attatck the {enemy['name']} with your copper sword')
            elif option == 'iron_sword':
                 print(f'Slice the {enemy['name']} with your iron sword')
        elif option in potions_list:
            if option == 'mushroom':
                print(f'Eat a mushroom(I don`t recommend doing that)({inventory.count('mushroom')}x)')
            elif option == 'lesser_healing_potion':
                print(f'Drink a lesser healing potion({inventory.count('lesser_healing_potion')})')
            elif option == 'healing_potion':
                print(f'Drink a healing potion({inventory.count('healing_potion')}x)')
            elif option == 'super_healing_potion':
                print(f'Drink a super healing potion("Legend says only those who are worthy can survive drinking it")({inventory.count('super_healing_potion')}x)')
    try:
        item_chosen = input('Insert your choice here: ')
        item_chosen_lower = item_chosen.lower()
        item_chosen_replace = item_chosen_lower.replace(' ', '_')
        
        if item_chosen_replace in weapon_list or item_chosen_replace in weapon_list:
            if item_chosen in inventory or item_chosen_replace in inventory:
                damage = round(random.uniform(1, 1.25) * (math.sqrt(level**1.2)) * weapon_list[item_chosen_replace])
                player['damage'] = damage
                player_damage_dealt = copy.deepcopy(player['damage'])

                use_weapon(item_chosen_replace)

                print(f'{enemy['name'].capitalize()}´s health is now {enemy_health_using['health']}/{enemy['max_health']}({round((enemy_health_using['health']/enemy['max_health'])*1000)/10}%)')
                enemy_die()
                enemy_attack(enemy['name'])
            else:
                clear()
                print('Please insert a valid option')
                print(f"{enemy['name'].capitalize()}´s health: {enemy_health_using["health"]}")
                print(f"{enemy['name'].capitalize()}´s level: {enemy['level']}")
                print(' ')
                print(f'{player['name']}´s health is now {player['health']}/{player['max_health']}({round((player['health']/player['max_health'])*1000)/10}%)')
    
                print(' ')
                print(f'Options: ')
                print(' ')
                continue
        elif item_chosen_replace in potions_list or item_chosen_replace in potions_list:
            if item_chosen_replace in inventory or item_chosen_replace in inventory:
                item_chosen_replace = item_chosen_lower.replace(' ', '_')
                use_potion(item_chosen_replace)
                enemy_die()
                enemy_attack(enemy['name'])
            else:
                clear()
                print('Please insert a valid option')
                print(f"{enemy['name'].capitalize()}´s health: {enemy_health_using["health"]}")
                print(f"{enemy['name'].capitalize()}´s level: {enemy['level']}")
                print(' ')
                print(f'{player['name']}´s health is now {player['health']}/{player['max_health']}({round((player['health']/player['max_health'])*1000)/10}%)')
    
                print(' ')
                print(f'Options: ')
                print(' ')
                continue
        else:
            clear()
            print('Please insert a valid option')
            print(f"{enemy['name'].capitalize()}´s health: {enemy_health_using["health"]}")
            print(f"{enemy['name'].capitalize()}´s level: {enemy['level']}")
            print(' ')
            print(f'{player['name']}´s health is now {player['health']}/{player['max_health']}({round((player['health']/player['max_health'])*1000)/10}%)')
    
            print(' ')
            print(f'Options: ')
            print(' ')
            continue
    
        print(f'What will you do?')
        print(' ')
        print(f'{enemy['name'].capitalize()}´s health: {enemy_health_using["health"]}')
        print(f'{enemy['name'].capitalize()}´s level: {enemy['level']}')
        print(' ')
        print(f'{player['name']}´s health is now {player['health']}/{player['max_health']}({round((player['health']/player['max_health'])*1000)/10}%)')
        print(f'{player['name']}´s level: {player['level']}')
        print(' ')
        print(f'Options: ')
        print(' ')
    except KeyError:
        clear()
        print('Please insert a valid option')
        print(' ')
        print(f'What will you do?')
        print(f'{enemy['name'].capitalize()}´s health: {enemy_health_using["health"]}/{enemy['max_health']}({round((enemy_health_using['health']/enemy['max_health'])*1000)/10}%)')
        print(f'{enemy['name'].capitalize()}´s level: {enemy['level']}')
        print(f'{player['name']}´s health is now {player['health']}/{player['max_health']}({round((player['health']/player['max_health'])*1000)/10}%)')
        print(f'{player['name']}´s level: {player['level']}')
        print(f'Options: ')
        print(' ')
        continue