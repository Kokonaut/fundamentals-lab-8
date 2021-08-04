from monsters.base_monster import BaseMonster


class FastMonster(BaseMonster):

    # Offset needed to accurately flip sprite
    ANCHOR_OFFSET = 0.2

    # Base starting stats at level 1
    BASE_STARTING_HP = 70
    BASE_STARTING_SPEED = 90

    def __init__(self, path, spawn_delay):
        super(FastMonster, self).__init__(path, spawn_delay)
        self.assets = 'assets/enemy_2/'
        self.hp = self.BASE_STARTING_HP
        self.speed = self.BASE_STARTING_SPEED
        self.reward = 5

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.defeated = True

    def respawn(self, level):
        super().respawn(level)
        # Update hp and speed when the wave gets respawned and difficulty increases
        self.hp = self.BASE_STARTING_HP + level * 5
        self.speed = self.BASE_STARTING_SPEED + level * 4
