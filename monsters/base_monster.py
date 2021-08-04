import uuid


class BaseMonster:

    # Offset needed to accurately flip sprite
    ANCHOR_OFFSET = 0

    def __init__(self, path, spawn_delay):
        if not path:
            raise ValueError("Need path for monster")
        initial_step = path[0]
        self.x = initial_step[0]
        self.y = initial_step[1]
        self.spawn_delay = spawn_delay
        self.path = path
        self.defeated = False
        self.id = None

        self.level = 1
        self.reward = 0

        # Status effects
        self.poison_time = 0
        self.poison_delay = 1
        self.poison_damage = 0
        self.is_poisoned = False

        # Filled in by children
        self.assets = None
        self.hp = None
        self.speed = None

    def set_id(self, id):
        self.id = id

    def update_status(self, delta):
        self.update_poison(delta)

    def update_poison(self, delta):
        self.poison_time -= delta
        self.poison_delay -= delta
        # Check if currently poisoned
        if self.poison_time <= 0:
            self.is_poisoned = False
        else:
            self.is_poisoned = True
        if self.is_poisoned:
            # Check if a second has passed and we should apply damage
            if self.poison_delay < 0:
                self.take_damage(self.poison_damage)
                self.poison_delay = 1

    def apply_slow(self, speed_modifier):
        self.speed -= speed_modifier
        if self.speed < 10:
            self.speed = 10

    def apply_poisoned(self, time, damage):
        self.poison_time = time
        self.poison_damage = damage

    def take_damage(self, damage):
        raise NotImplementedError

    def respawn(self, level):
        self.defeated = False
        self.is_poisoned = False

    def get_reward(self):
        return self.reward
