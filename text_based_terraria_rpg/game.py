import json
import cmath
import numpy as np
import random

weapom_list = {
    'stick': random.randint(2, 4),
    'wooden_sword': random.randint(3, 6),
    'copper_sword': random.randint(5, 9),
    'iron_sword': random.randint(6, 10)
}

name = input('Insert your character´s name: ')
level = 1
exp = 0
exp_needed = 9 + (cmath.sqrt(level**np.e))
max_health = 9 + (level ** 1.15) - cmath.sqrt(cmath.sqrt(level - level*0.25))
damage = 3 * (cmath.sqrt(level**1.2))
inventory = ['stick']

player = {
    'name': name,
    'max_health': max_health,
    'health': max_health,
    'level': level,
    'damage': damage,
    'inventory': inventory
}

enemy_level = round(level * random.uniform(0.85, 1.15))








enemy = {
    'name': random.choice(
        ['slime'] if level == 1 else
        (['slime', 'zombie'] if 2 <= level <= 5   else ['slime', 'zombie', 'demon eye'] )),
    'level': enemy_level,
}