from engine.tower_sprites.tower import TowerSprite
from engine.util import selector_lightning


class LightningTowerSprite(TowerSprite):

    def get_attack_cooldown(self):
        return self.tower.attack_cooldown

    def get_attack_radius(self):
        return self.tower.attack_radius

    def get_attack_damage(self):
        return self.tower.attack_damage
