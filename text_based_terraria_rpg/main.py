import json
import numpy as np
import random
import copy
import math
from clear import clear

armor_health = int

name = input('Insert your character´s name(Press enter to insert your name): ')
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

weapon_list = {
    'stick': random.uniform(1.25, 1.625),
    'wooden_sword': random.uniform(1.3125, 2.25),
    'copper_sword': random.uniform(2.25, 3),
    'zombie_arm': random.uniform(3, 4.25),
    'iron_sword': random.uniform(4.5, 5.75),
    'diamond_sword': random.uniform(6.125, 7.5),
}
potions_list = {
    'mushroom': 5 + round(0.1 * round(math.sqrt(max_health**(1+(math.e/10))))),
    'lesser_healing_potion': 10 + round(0.1 * round(math.sqrt(max_health**(1+(math.e/10))))),
    'healing_potion': 25 + round(0.1 * round(math.sqrt(max_health**(1+(math.e/10))))),
    'greater_healing_potion': 50 + round(0.1 * round(math.sqrt(max_health**(1+(math.e/10))))),
    'super_healing_potion': 100 + round(0.1 * round(math.sqrt(max_health**(1+(math.e/10))))),
}
weapon_materials_list = {
    'copper_bar': 'copper_bar',
    'iron_bar': 'iron_bar',
    'diamond': 'diamond',
}

potion_materials_list = {
    'gel': 'gel',
    'len': 'len',
    'slime_len': 'slime_len',
    'zombie_heart': 'zombie_heart',
}

armor_list = (
    {
        'copper_helmet': 10,
        'iron_helmet': 20, 
        'diamond_helmet': 35,
    },
    {
        'copper_chestplate': 20,
        'iron_chestplate': 35,
        'diamond_chestplate': 65,
    },
    {
        'copper_leggings': 15,
        'iron_leggings': 30,
        'diamond_leggings': 55
    },
    {
        'copper_boots': 10,
        'iron_boots': 20,
        'diamond_boots': 35,
    }
)

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

times_did_something_this_turn = 0

enemy = random_enemy(level)
enemy_health_using = {'health': enemy['health']}


def use_weapon(weapon=str):
    global times_did_something_this_turn
    clear()
    times_did_something_this_turn = 1
    print(f'{name} decides to attack {enemy['name']} with a {weapon.replace('_', ' ')}')
    enemy_health_using['health'] -= player_damage_dealt
    print(f'{player['name']} dealt {player_damage_dealt} damage!')
    print('')

def armor_health_calculation():
    armor_health = 0

    for i in range(len(armor_list)):
        owned_bonuses = []
        armor_slot_dict = armor_list[i]
        
        for name, health_armor in armor_slot_dict.items():
            if name in inventory:
                owned_bonuses.append(health_armor)
        
        if owned_bonuses:
            armor_health += max(owned_bonuses)
    return armor_health

def use_potion(potion):
    global health
    global times_did_something_this_turn
    clear()
    base_heal = potions_list[potion]
    bonus_heal = round(0.1 * round(math.sqrt(health**(1+(math.e/10)))))
    armor_health_calculation()
    total_heal = base_heal + bonus_heal
    times_did_something_this_turn = 1
    if health >= max_health or health + potions_list[potion] > max_health:
        health = max_health
    elif health <= 0:
        print('You died 🪦')
    else:
        health += total_heal
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
    print(' ')
    print(' ') 

def enemy_die():
    global level
    global exp
    global damage
    global health
    global max_health
    global inventory
    global name

    exp_needed = 9 + (math.sqrt(level**np.e))
    if enemy_health_using['health'] > enemy['max_health']:
        enemy_health_using['health'] = enemy['max_health']
    elif enemy_health_using['health'] <= 0:
        clear()
        print('You have defeated the enemy')
        print(' ')
        if enemy['name'] == 'slime':
            exp_gained_slime = round(random.uniform(1.25, 1.75) * math.sqrt(level) * math.sqrt(enemy['level']))
            exp += exp_gained_slime
            inventory.append('mushroom')
            print('You got a mushroom!')
            print(' ')
            if random.uniform(0, 1) <= 0.5:
                if round(random.uniform(1, 2)) == 1:
                    inventory.append('gel')
                    print('+1 gel')
                    print(' ')
                elif round(random.uniform(1, 2)) == 2:
                    inventory.append('gel')
                    inventory.append('gel')
                    print('+2 gel')
                    print(' ')
                if inventory.count('gel') >= 2 and inventory.count('len'):
                    try:
                        craft_option = input(f'Do you want to craft a [slime len],\n an [lesser healing potion](both use 2 gel and a len),\n or [nothing](type the option exactly right with or without caps\n(it doesnt matter), or press enter if\n you don´t want to craft anything)')
                        craft_option_lower = craft_option.lower()
                        craft_option_replace = craft_option_lower.replace(' ', '_')
                        if craft_option_replace:
                            if craft_option_replace == 'slime_len':
                                inventory.remove('gel')
                                inventory.remove('gel')
                                print('-2 gel')
                                print(' ')
                                inventory.remove('len')
                                print('-1 len')
                                print(' ')
                                inventory.append('slime_len')
                                print('You got a slime len!')
                                print(' ')
                                if inventory.count('slime_len') >= 1 and inventory.count('gel') >= 1:
                                    if input(f'Do you want to brew a healing potion with one slime len of yours and one gel\n([type anything] if yes(spaces count)\nand press [enter] if no)?'):
                                        inventory.remove('slime_len')
                                        print('-1 slime len')
                                        inventory.remove('gel')
                                        print('-1 gel')
                                        inventory.append('healing_potion')
                                        print('You got a healing potion!')
                            elif craft_option_replace == 'lesser_healing_potion':
                                inventory.remove('gel')
                                inventory.remove('gel')
                                print('-2 gel')
                                inventory.remove('len')
                                print('-1 len')
                                inventory.append('lesser_healing_potion')
                                print('You got a lesser healing potion!')
                    except TypeError:
                        print('Please insert a valid answer')
                        print('It´s a TypeError')
                            
                                
            if random.uniform(0, 1) <= 0.3333:
                inventory.append('stick')
                print('You got a stick!')
                if inventory.count('stick') >= 2:
                    if inventory.count('wooden_sword') < 1:
                        if input('Do you want to use your 2 sticks to make a wooden sword(one of\nthe sticks is conserved in the process)([type anything] if yes(spaces count)and press [enter] if no)? '):
                            inventory.remove('stick')
                            print('-1 stick')
                            print(' ')
                            inventory.append('wooden_sword')
                            print('You got a wooden sword!')
            print(' ')
            
            
        elif enemy['name'] == 'demon eye':
            exp_gained_demon_eye = round(random.uniform(0.35, 0.55) * math.sqrt(level) * math.sqrt(enemy['level'] ** 1.05))
            exp += exp_gained_demon_eye
            if random.uniform(0,1) <= 0.3333:
                clear()
                inventory.append('len')
                print('You got a len!')
                if inventory.count('gel') >= 2 and inventory.count('len'): # Slime len crafting
                    try:
                        craft_option = input(f'Do you want to craft a [slime len],\n an [lesser healing potion](both use 2 gel and a len),\n or [nothing](type the option exactly right with or without caps\n(it doesnt matter), or press enter if\n you don´t want to craft anything)')
                        craft_option_lower = craft_option.lower()
                        craft_option_replace = craft_option_lower.replace(' ', '_')
                        if craft_option_replace:
                            if craft_option_replace == 'slime_len':
                                inventory.remove('gel')
                                inventory.remove('gel')
                                print('-2 gel')
                                print(' ')
                                inventory.remove('len')
                                print('-1 len')
                                print(' ')
                                inventory.append('slime_len')
                                print('You got a slime len!')
                                if inventory.count('slime_len') >= 1 and inventory.count('gel') >= 1:
                                    if input(f'Do you want to brew a healing potion with one slime len of yours and one gel\n([type anything] if yes(spaces count)\nand press [enter] if no)?'):
                                        inventory.remove('slime_len')
                                        print('-1 slime len')
                                        inventory.remove('gel')
                                        print('-1 gel')
                                        inventory.append('healing_potion')
                                        print('You got a healing potion!')
                                if inventory.count('zombie_heart') >= 1 and inventory.count('slime_len') >= 2: # Greater healing potion crafting
                                    if input('Do you want to use your zombie heart and 2 slime lens to make\na greater healing potion(type anything for yes(spaces\ncount) and press enter for no)?'):
                                        inventory.remove('zombie_heart')
                                        print('-1 zombie heart0')
                                        print(' ')
                                        for removing_slime_lens in range(2):
                                            inventory.remove('slime_len')
                                        print('-2 slime lens')
                                        print(' ')
                                        inventory.append('greater_healing_potion')
                                        print('You got a greater healing potion')

                            elif craft_option_replace == 'lesser_healing_potion':
                                inventory.remove('gel')
                                inventory.remove('gel')
                                print('-2 gel')
                                print(' ')
                                inventory.remove('len')
                                print('-1 len')
                                print(' ')
                                inventory.append('lesser_healing_potion')
                                print('You got a lesser healing potion!')
                    except ValueError:
                        print('Please insert a valid answer')
                        print('It´s a ValueError')
            if random.uniform(0, 1) <= 0.2:
                clear()
                inventory.append('copper_bar')
                print('You got a copper bar!')
                if inventory.count('copper_bar') >= 2 and inventory.count('stick') >= 1: #
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
                if inventory.count('copper_bar') >= 4: # Copper armor crafting

                    if inventory.count('copper_bar') >= 4 and inventory.count('copper_helmet') < 1: # Copper helmet crafting
                        if input('Do you want to use 4 of your copper bars and a stick to make an\n copper helmet(type anything for yes(spaces\n count) and press enter for no)?'):
                            for removing_copper in range(4):
                                inventory.remove('copper_bar')
                            print('-4 copper bars')
                            print(' ')
                            inventory.append('copper_helmet')
                            print('You got an copper helmet!')
                            print(' ')

                    if inventory.count('copper_bar') >= 7 and inventory.count('copper_chestplate') < 1: # Copper chestplate crafting
                        if input('Do you want to use 7 of your copper bars and a stick to make an\n copper chestplate(type anything for yes(spaces\n count) and press enter for no)?'):
                            for removing_copper in range(7):
                                inventory.remove('copper_bar')
                            clear()
                            print('-7 copper bars')
                            print(' ')
                            inventory.append('copper_chestplate')
                            print('You got an copper chestplate!')
                            print(' ')

                    if inventory.count('copper_bar') >= 6 and inventory.count('copper_leggings') < 1: # Copper leggings crafting
                        if input('Do you want to use 6 of your copper bars and a stick to make a pair \nof copper leggings(type anything for yes(spaces\n count) and press enter for no)?'):
                            for removing_copper in range(6):
                                inventory.remove('copper_bar')
                            clear()
                            print('-6 copper bars')
                            print(' ')
                            inventory.append('copper_leggings')
                            print('You got a pair of copper leggings')
                            print(' ')

                    if inventory.count('copper_bar') >= 3 and inventory.count('copper_boots') < 1: # Copper boots crafting
                        if input('Do you want to use 3 of your copper bars and a stick to make a pair \nof copper boots(type anything for yes(spaces\n count) and press enter for no)?'):
                            for removing_copper in range(3):
                                inventory.remove('copper_bar')
                            clear()
                            print('-3 copper bars')
                            print(' ')
                            inventory.append('copper_boots')
                            print('You got a pair of copper leggings')
                            print(' ')

            if random.uniform(0, 1) <= 0.05:
                clear()
                inventory.append('iron_bar')
                print('You got a iron bar!')
                if inventory.count('iron_bar') >= 2 and inventory.count('copper_sword') >= 1:
                    if inventory.count('iron_sword') < 1: # Iron sword crafting
                        if input('Do you want to use 2 of your iron bars and your copper sword\n to make an iron sword(type anything for yes(spaces count) and\npress enter for no)?'):
                            inventory.remove('copper_sword')
                            print('-1 copper sword')
                            print(' ')
                            inventory.remove('iron_bar')
                            inventory.remove('iron_bar')
                            print('-2 iron bars')
                            print(' ')
                            inventory.append('iron_sword')
                            print('You got an iron sword')

                if inventory.count('iron_bar') >= 2: # Iron armor crafting

                    if inventory.count('iron_bar') >= 2 and inventory.count('copper_helmet') >= 1: # Iron helmet crafting
                        if inventory.count('iron_helmet') < 1:
                            if input('Do you want to use 2 of your iron bars and your copper helmet\nto make an iron helmet(type anything for yes(spaces count) and\npress enter for no)?'):
                                inventory.remove('copper_helmet')
                                print('-1 copper helmet')
                                print(' ')
                                for removing_iron in range(2):
                                    inventory.remove('iron_bar')
                                print('-2 iron bars')
                                print(' ')
                                inventory.append('iron_helmet')
                                print('You got an iron helmet')
                                print(' ')

                    if inventory.count('iron_bar') >= 5 and inventory.count('copper_chestplate') >= 1: # Iron chestplate crafting
                        if inventory.count('iron_chestplate') < 1:
                            if input('Do you want to use 5 of your iron bars and your copper chestplate\nto make an iron chestplate(type anything for yes(spaces count) and\npress enter for no)?'):
                                inventory.remove('copper_chestplate')
                                print('-1 copper chestplate')
                                print(' ')
                                for removing_iron in range(5):
                                    inventory.remove('iron_bar')
                                print('-5 iron bars')
                                print(' ')
                                inventory.append('iron_chestplate')
                                print('You got an iron chestplate!')
                                print(' ')

                    if inventory.count('iron_bar') >= 4 and inventory.count('copper_leggings') >= 1: # Iron leggings crafting
                        if inventory.count('iron_leggings') < 1:
                            if input('Do you want to use 4 of your iron bars and your pair of copper leggings\n to make a pair of iron leggings(type anything for\nyes(spaces count) and press enter for no)?'):
                                inventory.remove('copper_leggings')
                                print('-1 copper leggings')
                                print(' ')
                                for removing_iron in range(4):
                                    inventory.remove('iron_bar')
                                print('-4 iron bars')
                                print(' ')
                                inventory.append('iron_chestplate')
                                print('You got a pair of iron leggings!')
                                print(' ')

                    if inventory.count('iron_bar') >= 2 and inventory.count('copper_boots') >= 1: # Iron boots crafting
                        if inventory.count('iron_boots') < 1:
                            if input('Do you want to use 2 of your iron bars and your pair of copper boots\n to make a pair of iron boots(type anything for\nyes(spaces count) and press enter for no)?'):
                                inventory.remove('copper_boots')
                                print('-1 copper boots')
                                print(' ')
                                for removing_iron in range(2):
                                    inventory.remove('iron_bar')
                                print('-2 iron bars')
                                print(' ')
                                inventory.append('iron_boots')
                                print('You got a pair of iron boots!')
                                print(' ')

        elif enemy['name'] == 'zombie':
            exp_gained_zombie = round(random.uniform(0.50, 0.75) * math.sqrt(level) * math.sqrt(enemy['level'] ** 1.15))
            exp += exp_gained_zombie
            if random.uniform(0, 1) <= 0.090625: # Zombie arm drop
                inventory.append('zombie_arm')
                print('You got a zombie arm!')
                print(' ')
            if random.uniform(0, 1) <= 0.075: # Zombie heart drop
                inventory.append('zombie_heart')
                print('You got a zombie heart')
                print(' ')
                if inventory.count('zombie_heart') >= 1 and inventory.count('slime_len') >= 2: # Greater healing potion crafting
                    if input('Do you want to use your zombie heart and 2 slime lens to make\na greater healing potion(type anything for yes(spaces\ncount) and press enter for no)?'):
                        inventory.remove('zombie_heart')
                        print('-1 zombie heart')
                        print(' ')
                        for removing_slime_lens in range(2):
                            inventory.remove('slime_len')
                        print('-2 slime lens')
                        print(' ')
                        inventory.append('greater_healing_potion')
                        print('You got a greater healing potion')
            if random.uniform(0, 1) < 0.075:
                inventory.append('diamond')
                print('You got an diamond!')
                print(' ')
                if inventory.count('diamond') >= 3  and inventory.count('iron_bar') >= 2: # Diamond helmet crafting
                    if input('Do you want to use 3 of your diamonds and 2 of your iron bars to\nmake a diamond helmet(type anything for yes(spaces count)and\npress enter for no)?'):
                        for removing_diamonds in range(3):
                            inventory.remove('diamond')
                        print('-3 diamonds')
                        print(' ')
                        for removing_iron in range(2):
                            inventory.remove('iron_bar')
                        print('-2 iron bars')
                        print(' ')
                        inventory.append('diamond_helmet')
                        print('You got a diamond helmet!')
                        print(' ')

                if inventory.count('diamond') >= 5 and inventory.count('iron_bar') >= 2: # Diamond chestplate crafting
                    if input('Do you want to use 5 of your diamonds and 2 of your iron bars to\nmake a diamond chestplate(type anything for yes(spaces\ncount)and press enter for no)?'):
                        for removing_diamonds in range(5):
                            inventory.remove('diamond')
                        print('-5 diamonds')
                        print(' ')
                        for removing_iron in range(2):
                            inventory.remove('iron_bar')
                        print('-2 iron bars')
                        print(' ')
                        inventory.append('diamond_chestplate')
                        print('You got a diamond chestplate')
                        print(' ')

                if inventory.count('diamond') >= 4 and inventory.count('iron_bar') >= 2: # Diamond leggings crafting
                    if input('Do you want to use 4 of your diamonds and 2 of your iron bars to\nmake a pair of diamond leggings(type anything for yes(spaces\ncount)and press enter for no)?'):
                        for removing_diamonds in range(4):
                            inventory.remove('diamond')
                        print('-4 diamonds')
                        print(' ')
                        for removing_iron in range(2):
                            inventory.remove('iron_bar')
                        print('-2 iron bars')
                        print(' ')
                        inventory.append('diamond_leggings')
                        print('You got a pair of diamond leggings!')
                        print(' ')
                
                if inventory.count('diamond') >= 2 and inventory.count('iron_bar') >= 1: # Diamond boots crafting
                    if input('Do you want to use 2 of your diamonds and 1 of your iron bars to\nmake a pair of diamond boots(type anything for yes(spaces\ncount)and press enter for no)?'):
                        for removing_diamonds in range(2):
                            inventory.remove('diamond')
                        print('-2 diamonds')
                        print(' ')
                        inventory.remove('iron_bar')
                        print('-1 iron bar')
                        print(' ')
                        inventory.append('diamond_boots')
                        print('You got a pair of diamond boots!')
                        print(' ')

        while exp >= exp_needed:
            exp -= exp_needed
            level += 1
            exp_needed = 9 + round(math.sqrt(level**np.e))
            armor_bonus_health = armor_health_calculation()
            
            max_health = round(10 + (level ** 1.15) - round(math.sqrt(math.sqrt(level - level*(np.e/9)))) + round(armor_bonus_health))
            health = copy.deepcopy(max_health)
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
print('Options: ')
while True:
    if health > max_health:
        health = max_health
    elif health <= 0:
        print('You died')
        exit()


    enemy_die()
    options = set(inventory)
    enemy_damage_dealt = copy.deepcopy(enemy['damage'])
    player_damage_dealt = copy.deepcopy(player['damage'])

    for option in options:
        
        if option in weapon_list:
            if option == 'stick':
                print(f'Poke the {enemy['name']} with your mighty... [stick]?(why)')
            elif option == 'wooden_sword':
                print(f'Attack the {enemy['name']} with your [wooden sword](still just a fancy stick)')
            elif option == 'copper_sword':
                print(f'Attack the {enemy['name']} with your [copper sword]')
            elif option == 'zombie_arm':
                print(f'Attatck the {enemy['name']} with your [zombie arm](gross)')
            elif option == 'iron_sword':
                print(f'Slice the {enemy['name']} with your [iron sword]')
            elif option == 'diamond_sword':
                print(f'Slice the {enemy['name']} with you [diamond sword]')
        elif option in potions_list:
            if option == 'mushroom':
                print(f'Eat a [mushroom](I don`t recommend doing that)({inventory.count('mushroom')}x)')
            elif option == 'lesser_healing_potion':
                print(f'Drink a [lesser healing potion]({inventory.count('lesser_healing_potion')})')
            elif option == 'healing_potion':
                print(f'Drink a [healing potion]({inventory.count('healing_potion')}x)')
            elif option == 'super_healing_potion':
                print(f'Drink a [super healing potion]("Legend says only those who are worthy can survive drinking it")({inventory.count('super_healing_potion')}x)')
    try:
        times_did_something_this_turn = 0
        item_chosen = input('Insert your choice here: ')
        item_chosen_lower = item_chosen.lower()
        item_chosen_replace = item_chosen_lower.replace(' ', '_')
        options_possibilities = list()


        
        if item_chosen_replace in weapon_list or item_chosen_replace in weapon_list:
            if item_chosen in inventory or item_chosen_replace in inventory:
                damage = round(random.uniform(1, 1.25) * (math.sqrt(level**1.2)) * weapon_list[item_chosen_replace])
                player['damage'] = damage
                player_damage_dealt = copy.deepcopy(player['damage'])
                
                if times_did_something_this_turn <= 0:
                    use_weapon(item_chosen_replace)

                print(f'{enemy['name'].capitalize()}´s health is now {enemy_health_using['health']}/{enemy['max_health']}({round((enemy_health_using['health']/enemy['max_health'])*1000)/10}%)')
                enemy_die()
                if enemy_health_using['health'] < enemy['max_health']: enemy_attack(enemy['name'])
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
                if times_did_something_this_turn <= 0:
                    use_potion(item_chosen_replace)
                enemy_die()
                if enemy_health_using['health'] < enemy['max_health']: enemy_attack(enemy['name'])
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

            
        elif item_chosen_replace in inventory:
            options_possibilities.append(item_chosen_replace)

        elif not options_possibilities:

            for weapon in weapon_list:
                if item_chosen_replace in weapon and weapon in inventory:
                    options_possibilities.append(weapon)

            for potion in potions_list:
                if item_chosen_replace in potion and potion in inventory:
                    options_possibilities.append(potion)

            if len(options_possibilities) == 1:
                item_using = options_possibilities[0]
            
                if item_using in weapon_list:
                    damage = round(random.uniform(1, 1.25) * math.sqrt(level ** 1.2) * weapon_list[item_using])
                    player['damage'] = damage
                    player_damage_dealt = copy.deepcopy(player['damage'])
                    use_weapon(item_using.replace('_', ' '))

                    print(f'{enemy['name'].capitalize()}´s health is now {enemy_health_using['health']}/{enemy['max_health']}({round((enemy_health_using['health']/enemy['max_health'])*1000)/10}%)')
                    enemy_die()
                    if enemy_health_using['health'] > 0: enemy_attack(enemy['name'])
                elif item_using in potions_list:
                    use_potion(item_using)
                    enemy_die()
                    if enemy_health_using['health'] > 0: enemy_attack(enemy['name'])

            elif len(options_possibilities) > 1:
                raise SyntaxError(options_possibilities)
        
            else: raise KeyError

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
    except SyntaxError as e:
        clear()
        print('Please be more specific(not possible to certainly know which option you mean to use),\nwith what you provided, it could be:')
        ambiguous_options = e.args[0]
        for option in ambiguous_options:
            print(f'- {option.replace('_', ' ')}')
        print(' ')

        print(' ')
        print(f'What will you do?')
        print(f'{enemy['name'].capitalize()}´s health: {enemy_health_using["health"]}/{enemy['max_health']}({round((enemy_health_using['health']/enemy['max_health'])*1000)/10}%)')
        print(f'{enemy['name'].capitalize()}´s level: {enemy['level']}')
        print(f'{player['name']}´s health is now {player['health']}/{player['max_health']}({round((player['health']/player['max_health'])*1000)/10}%)')
        print(f'{player['name']}´s level: {player['level']}')
        print(f'Options: ')
        print(' ')