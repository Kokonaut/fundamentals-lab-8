from os import listdir
from os.path import isfile, join


def get_files_in_path(path):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    files.sort()
    return files


def get_distance_to_goal(monster):
    diff_x = abs(monster.x - monster.dest_x)
    diff_y = abs(monster.y - monster.dest_y)
    return (diff_x ** 2 + diff_y ** 2) ** 0.5


def get_remaining_monster_health(monster):
    return monster._monster.hp


def run_tower_attack_monster(tower, monster, damage):
    tower.attack(monster, damage)


def selector_lightning(monsters):
    closest = None
    for monster in monsters:
        if get_remaining_monster_health(monster) < 20:
            return monster
        if closest == None:
            closest = monster
        elif get_distance_to_goal(monster) < get_distance_to_goal(closest):
            closest = monster
    return closest


def selector_rock(monsters):
    closest = None
    for monster in monsters:
        if get_remaining_monster_health(monster) > 100:
            return monster
        if closest == None:
            closest = monster
        elif get_distance_to_goal(monster) < get_distance_to_goal(closest):
            closest = monster
    return closest


def tower_attack(monsters, tower, tower_type):
    if tower_type == 'lightning':
        monster = selector_lightning(monsters)
        damage = 20
    elif tower_type == 'rock':
        monster = selector_rock(monsters)
        damage = 100
    run_tower_attack_monster(tower, monster, damage)
