from os import path
import pyglet
import random

from engine.game import Game
from monsters.heavy_monster import HeavyMonster
from monsters.fast_monster import FastMonster
from monsters.speed_monster import SpeedMonster
from monsters.shield_monster import ShieldMonster


def get_random():
    return random.uniform(0.05, 0.90)

# ------- Your Code Here -------


background_file = 'assets/background/game_background.png'
game = Game(background_file, lives=5)

game.add_finish((0.97, 0.35))
game.add_finish((0.97, 0.15))

path_1 = [
    (0.25, 0),
    (0.24, 0.14,),
    (0.20, 0.18,),
    (0.14, 0.2,),
    (0.1, 0.24,),
    (0.08, 0.34,),
    (0.1, 0.44,),
    (0.14, 0.48,),
    (0.19, 0.5,),
    (0.225, 0.53,),
    (0.26, 0.62,),
    (0.2675, 0.72,),
    (0.31, 0.789,),
    (0.5, 0.789,),
    (0.53, 0.77,),
    (0.56, 0.73,),
    (0.57, 0.41,),
    (0.58, 0.33,),
    (0.61, 0.27,),
    (0.75, 0.27,),
    (1.1, 0.27,),
]

path_2 = [
    (0.75, 1.1,),
    (0.75, 0.27,),
    (1.1, 0.27,),
]

tower_spots = [
    (0.154, 0.085,),
    (0.185, 0.375,),
    (0.148, 0.66,),
    (0.41, 0.71,),
    (0.655, 0.755,),
    (0.655, 0.44,),
    (0.752, 0.15,),
    (0.85, 0.44,),
]

game.add_tower_spots(tower_spots)

monsters = [
    FastMonster(path_1, 0),
    FastMonster(path_1, 1),
    FastMonster(path_1, 2),
    FastMonster(path_2, 2),
    HeavyMonster(path_1, 7),
    HeavyMonster(path_1, 3),
    FastMonster(path_1, 1),
    FastMonster(path_2, 3),
    SpeedMonster(path_1, 6),
    ShieldMonster(path_1, 5),
    HeavyMonster(path_1, 8),
    ShieldMonster(path_2, 1),
    SpeedMonster(path_1, 5),
]

game.add_monsters(monsters)


# ------- End Code Here -------

if __name__ == '__main__':
    game.start_game()
    pyglet.app.run()
