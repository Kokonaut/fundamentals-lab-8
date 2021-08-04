from towers.base_tower import BaseTower


poison_build_price = 80


class PoisonTower(BaseTower):

    def __init__(self):
        self.attack_level = 1
        self.speed_level = 1
        self.attack_damage = 10
        self.attack_cooldown = 3
        self.attack_radius = 250

        self.poison_duration = 10
        self.damage_from_poison = 6

    def run_attack(self, monsters_in_range):
        if len(monsters_in_range) == 0:
            return None
        monster = monsters_in_range[0]
        for m in monsters_in_range:
            if not m.is_poisoned:
                monster = m
        monster.take_damage(self.attack_damage)
        monster.apply_poisoned(self.poison_duration, self.damage_from_poison)
        return monster

    def get_attack_upgrade_price(self):
        return 50 * self.attack_level * 0.5

    def get_speed_upgrade_price(self):
        return 50 * self.speed_level * 0.5

    def upgrade_attack(self):
        self.damage_from_poison += self.attack_level * 0.2
        print("Poison Tower damage upgraded to " + str(self.damage_from_poison))
        self.attack_level += 1

    def upgrade_speed(self):
        self.attack_cooldown -= self.speed_level * 0.1
        if self.attack_cooldown < 0.2:
            self.attack_cooldown = 0.2
            print("Tower Speed at max!")
        else:
            print("Poison Tower speed upgraded to " +
                  str(self.get_speed()) + " attacks per minute")
        self.speed_level += 1
