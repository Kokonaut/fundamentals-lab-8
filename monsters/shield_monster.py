from monsters.base_monster import BaseMonster


class ShieldMonster(BaseMonster):

    # Offset needed to accurately flip sprite
    ANCHOR_OFFSET = 0.35

    # Base starting stats at level 1
    BASE_STARTING_HP = 150
    BASE_STARTING_SPEED = 60

    def __init__(self, path, spawn_delay):
        super(ShieldMonster, self).__init__(path, spawn_delay)
        self.assets = 'assets/enemy_3/'
        self.hp = self.BASE_STARTING_HP
        self.speed = self.BASE_STARTING_SPEED
        self.shield = 3
        self.reward = 10

    def take_damage(self, damage):
        if self.shield > 0:
            self.hp -= damage
        else:
            self.shield -= 1
            return
        if self.hp <= 0:
            self.hp = 0
            self.defeated = True

    def respawn(self, level):
        super().respawn(level)
        # Update hp and speed when the wave gets respawned and difficulty increases
        self.hp = self.BASE_STARTING_HP + level * 20
        self.speed = self.BASE_STARTING_SPEED + level * 2
