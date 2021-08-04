from monsters.base_monster import BaseMonster


class HeavyMonster(BaseMonster):

    # Offset needed to accurately flip sprite
    ANCHOR_OFFSET = 0.35

    # Base starting stats at level 1
    BASE_STARTING_HP = 240
    BASE_STARTING_SPEED = 40

    def __init__(self, path, spawn_delay):
        super(HeavyMonster, self).__init__(path, spawn_delay)
        self.assets = 'assets/enemy_1/'
        self.hp = self.BASE_STARTING_HP
        self.speed = self.BASE_STARTING_SPEED
        self.reward = 10

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.defeated = True

    def respawn(self, level):
        super().respawn(level)
        # Update hp and speed when the wave gets respawned and difficulty increases
        self.hp = self.BASE_STARTING_HP + level * 5
        self.speed = self.BASE_STARTING_SPEED + level * 3
