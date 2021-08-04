from towers.base_tower import BaseTower


ice_build_price = 70


class IceTower(BaseTower):

    def __init__(self):
        self.attack_level = 1
        self.speed_level = 1
        self.attack_damage = 10
        self.attack_cooldown = 2
        self.attack_radius = 350
        self.slow_effect = 5

    def run_attack(self, monsters_in_range):
        if len(monsters_in_range) == 0:
            return None
        target = monsters_in_range[0]
        for monster in monsters_in_range:
            if monster.speed > target.speed:
                target = monster
        target.apply_slow(self.slow_effect)
        target.take_damage(self.attack_damage)
        return target

    def get_attack_upgrade_price(self):
        return 50 * self.attack_level * 0.5

    def get_speed_upgrade_price(self):
        return 50 * self.speed_level * 0.5

    def upgrade_attack(self):
        self.slow_effect += self.attack_level
        print("Ice Tower slow effect upgraded to " + str(self.slow_effect))
        self.attack_level += 1

    def upgrade_speed(self):
        self.attack_cooldown -= self.speed_level * 0.1
        if self.attack_cooldown < 0.2:
            self.attack_cooldown = 0.2
            print("Tower Speed at max!")
        else:
            print("Ice Tower speed upgraded to " +
                  str(self.get_speed()) + " attacks per minute")
        self.speed_level += 1
