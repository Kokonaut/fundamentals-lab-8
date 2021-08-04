from towers.base_tower import BaseTower


rock_build_price = 100


class RockTower(BaseTower):

    def __init__(self):
        self.attack_level = 1
        self.speed_level = 1
        self.attack_damage = 80
        self.attack_cooldown = 4
        self.attack_radius = 200

    def run_attack(self, monsters_in_range):
        if len(monsters_in_range) == 0:
            return None
        target = monsters_in_range[0]
        for monster in monsters_in_range:
            if monster.hp > target.hp:
                target = monster
        target.take_damage(self.attack_damage)
        return target

    def get_attack_upgrade_price(self):
        return 50 * self.attack_level * 0.5

    def get_speed_upgrade_price(self):
        return 50 * self.speed_level * 0.5

    def upgrade_attack(self):
        self.attack_damage += self.attack_level
        print("Rock Tower damage upgraded to " + str(self.attack_damage))
        self.attack_level += 1

    def upgrade_speed(self):
        self.attack_cooldown -= self.speed_level * 0.1
        if self.attack_cooldown < 0.2:
            self.attack_cooldown = 0.2
            print("Tower Speed at max!")
        else:
            print("Rock Tower speed upgraded to " +
                  str(self.get_speed()) + " attacks per minute")
        self.speed_level += 1
