from monsters.heavy_monster import HeavyMonster
from monsters.fast_monster import FastMonster
from monsters.speed_monster import SpeedMonster
from monsters.shield_monster import ShieldMonster

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


class Loop:

    def __init__(self, game):
        self.game = game
        self.level = 1

    def stop_game(self):
        self.game.stop()

    def start_round(self, level):
        self.game.start_round(level)

    def reward_player(self, amount):
        self.game.add_reward(amount)

    def add_player_lives(self, amount):
        self.game.add_lives(amount)

    def is_round_over(self):
        return self.game.is_round_over()

    def get_defeated_monsters(self):
        return self.game.get_defeated_monsters()

    def add_new_fast_monster(self):
        fast_monster = FastMonster(path_1, 3)
        self.add_new_monster(fast_monster)

    def add_new_heavy_monster(self):
        heavy_monster = HeavyMonster(path_1, 3)
        self.add_new_monster(heavy_monster)

    def add_new_speed_monster(self):
        speed_monster = SpeedMonster(path_1, 3)
        self.add_new_monster(speed_monster)

    def add_new_shield_monster(self):
        shield_monster = ShieldMonster(path_1, 3)
        self.add_new_monster(shield_monster)

    def add_new_monster(self, monster):
        # Add a single monster
        return self.game.add_new_monsters([monster])

    def add_new_monsters(self, monsters):
        # Add a list of monsters
        return self.game.add_new_monsters(monsters)

    def update(self):
        pass
