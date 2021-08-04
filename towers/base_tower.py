class BaseTower:

    def __init__(self):
        self.attack_level = 1
        self.speed_level = 1
        self.attack_damage = 0
        self.attack_cooldown = 0
        self.attack_radius = 0

    def run_attack(self, monsters_in_range):
        raise NotImplementedError

    def upgrade_attack(self):
        raise NotImplementedError

    def upgrade_speed(self):
        raise NotImplementedError

    def get_attack_upgrade_price(self):
        return 0

    def get_speed_upgrade_price(self):
        return 0

    def get_speed(self):
        if self.attack_cooldown == 0:
            return 0
        return 60 / self.attack_cooldown
