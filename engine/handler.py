import pyglet


class ClickHandler:

    SLOT_CLICK_BOX_X = 100
    SLOT_CLICK_BOX_Y = 50

    TILE_CLICK_BOX_X = 20
    TILE_CLICK_BOX_Y = 20

    TILE_OFFSET_HEIGHT = 50
    TILE_OFFSET_WIDTH = 40

    def __init__(self, slots, towers, wallet, build_prices, window, batch, group):
        self.slots = slots
        self.towers = towers
        self.wallet = wallet
        self.window = window
        self.batch = batch
        self.focused = None
        self.focused_upgrade = None
        self.upgrades_shown = False
        self.group = group
        self.lightning_price = build_prices['lightning']
        self.rock_price = build_prices['rock']
        self.ice_price = build_prices['ice']
        self.poison_price = build_prices['poison']
        self.lightning_tile = self.build_lightning_tile(
            self.lightning_price)
        self.rock_tile = self.build_rock_tile(self.rock_price)
        self.ice_tile = self.build_ice_tile(self.ice_price)
        self.poison_tile = self.build_poison_tile(self.poison_price)
        self.speed_tile = self.build_speed_tile()
        self.attack_tile = self.build_attack_tile()
        self.destroy_tile = self.build_destroy_tile()

    def build_label(self, price):
        label = pyglet.text.Label(
            text=str(price),
            x=0,
            y=0,
            font_name='Press Start 2P',
            font_size=10,
            anchor_x='center',
            batch=self.batch,
            group=self.group
        )
        label.draw()
        label.visible = False
        return label

    def build_lightning_tile(self, price):
        tile_1 = pyglet.resource.image('assets/tiles/lightning.png')
        tile_1.anchor_x = tile_1.width // 2
        tile_1.anchor_y = tile_1.height // 2
        lightning_tile = pyglet.sprite.Sprite(
            tile_1, x=0, y=0, batch=self.batch, group=self.group)
        lightning_tile.scale = 0.33
        lightning_tile.visible = False
        self.lightning_label = self.build_label(price)
        return lightning_tile

    def build_rock_tile(self, price):
        tile_2 = pyglet.resource.image('assets/tiles/rock.png')
        tile_2.anchor_x = tile_2.width // 2
        tile_2.anchor_y = tile_2.height // 2
        rock_tile = pyglet.sprite.Sprite(
            tile_2, x=0, y=0, batch=self.batch, group=self.group)
        rock_tile.scale = 0.33
        rock_tile.visible = False
        self.rock_label = self.build_label(price)
        return rock_tile

    def build_ice_tile(self, price):
        tile_1 = pyglet.resource.image('assets/tiles/ice.png')
        tile_1.anchor_x = tile_1.width // 2
        tile_1.anchor_y = tile_1.height // 2
        ice_tile = pyglet.sprite.Sprite(
            tile_1, x=0, y=0, batch=self.batch, group=self.group)
        ice_tile.scale = 0.33
        ice_tile.visible = False
        self.ice_label = self.build_label(price)
        return ice_tile

    def build_poison_tile(self, price):
        tile_1 = pyglet.resource.image('assets/tiles/poison.png')
        tile_1.anchor_x = tile_1.width // 2
        tile_1.anchor_y = tile_1.height // 2
        poison_tile = pyglet.sprite.Sprite(
            tile_1, x=0, y=0, batch=self.batch, group=self.group)
        poison_tile.scale = 0.33
        poison_tile.visible = False
        self.poison_label = self.build_label(price)
        return poison_tile

    def build_speed_tile(self):
        tile_1 = pyglet.resource.image('assets/tiles/speed.png')
        tile_1.anchor_x = tile_1.width // 2
        tile_1.anchor_y = tile_1.height // 2
        speed_tile = pyglet.sprite.Sprite(
            tile_1, x=0, y=0, batch=self.batch, group=self.group)
        speed_tile.scale = 0.33
        speed_tile.visible = False
        self.build_speed_label()
        return speed_tile

    def build_speed_label(self):
        self.speed_label = pyglet.text.Label(
            text="",
            x=0,
            y=0,
            font_name='Press Start 2P',
            font_size=10,
            anchor_x='center',
            batch=self.batch,
            group=self.group
        )
        self.speed_label.draw()
        self.speed_label.visible = False

    def build_attack_tile(self):
        tile_1 = pyglet.resource.image('assets/tiles/attack.png')
        tile_1.anchor_x = tile_1.width // 2
        tile_1.anchor_y = tile_1.height // 2
        attack_tile = pyglet.sprite.Sprite(
            tile_1, x=0, y=0, batch=self.batch, group=self.group)
        attack_tile.scale = 0.33
        attack_tile.visible = False
        self.build_attack_label()
        return attack_tile

    def build_attack_label(self):
        self.attack_label = pyglet.text.Label(
            text="",
            x=0,
            y=0,
            font_name='Press Start 2P',
            font_size=10,
            anchor_x='center',
            batch=self.batch,
            group=self.group
        )
        self.attack_label.draw()
        self.attack_label.visible = False

    def build_destroy_tile(self):
        tile_1 = pyglet.resource.image('assets/button_close.png')
        tile_1.anchor_x = tile_1.width // 2
        tile_1.anchor_y = tile_1.height // 2
        destroy_tile = pyglet.sprite.Sprite(
            tile_1, x=0, y=0, batch=self.batch, group=self.group)
        destroy_tile.scale = 0.33
        destroy_tile.visible = False
        return destroy_tile

    def handle_click(self, x, y):
        click_handled = False
        if self.upgrades_shown:
            tower = self.tower_is_active(self.focused)
            speed_tile_xy = (self.speed_tile.x, self.speed_tile.y,)
            attack_tile_xy = (self.attack_tile.x, self.attack_tile.y,)
            destroy_tile_xy = (self.destroy_tile.x, self.destroy_tile.y,)
            if self.tile_is_clicked(speed_tile_xy, x, y):
                if self.wallet.request_purchase(tower.get_speed_price()):
                    tower.upgrade_speed()
                else:
                    print("Not enough money for speed upgrade")
            elif self.tile_is_clicked(attack_tile_xy, x, y):
                if self.wallet.request_purchase(tower.get_attack_price()):
                    tower.upgrade_attack()
                else:
                    print("Not enough money for attack upgrade")
            elif self.tile_is_clicked(destroy_tile_xy, x, y):
                tower.deactivate()
            self.focused = None
            self.upgrades_shown = False
            self.hide_upgrades()
            return True
        elif self.focused:
            lightning_tile_xy = (self.lightning_tile.x, self.lightning_tile.y,)
            rock_tile_xy = (self.rock_tile.x, self.rock_tile.y,)
            ice_tile_xy = (self.ice_tile.x, self.ice_tile.y,)
            poison_tile_xy = (self.poison_tile.x, self.poison_tile.y,)
            if self.tile_is_clicked(lightning_tile_xy, x, y):
                if self.wallet.request_purchase(self.lightning_price):
                    self.towers[(self.focused.x, self.focused.y,)
                                ]['lightning_tower'].activate()
                else:
                    print("Not enough money for Lightning Tower")
                click_handled = True
            elif self.tile_is_clicked(rock_tile_xy, x, y):
                if self.wallet.request_purchase(self.rock_price):
                    self.towers[(self.focused.x, self.focused.y,)
                                ]['rock_tower'].activate()
                else:
                    print("Not enough money for Rock Tower")
                click_handled = True
            elif self.tile_is_clicked(ice_tile_xy, x, y):
                if self.wallet.request_purchase(self.ice_price):
                    self.towers[(self.focused.x, self.focused.y,)
                                ]['ice_tower'].activate()
                else:
                    print("Not enough money for Ice Tower")
            elif self.tile_is_clicked(poison_tile_xy, x, y):
                if self.wallet.request_purchase(self.poison_price):
                    self.towers[(self.focused.x, self.focused.y,)
                                ]['poison_tower'].activate()
                else:
                    print("Not enough money for Poison Tower")
            elif self.slot_is_clicked((self.focused.x, self.focused.y,), x, y):
                return True
            self.focused = None
            self.hide_tiles()
            return click_handled
        else:
            for slot in self.slots:
                if self.slot_is_clicked(slot, x, y):
                    self.focused = self.slots[slot]
                    if self.tower_is_active(self.focused):
                        self.show_upgrades(self.focused)
                        self.upgrades_shown = True
                    else:
                        self.show_tiles(self.focused)
                    return True
            self.hide_tiles()
            self.hide_upgrades()

    def show_tiles(self, slot):
        x = slot.x
        y = slot.y
        tile_down_x = x - self.TILE_OFFSET_WIDTH
        tile_up_y = y + self.TILE_OFFSET_HEIGHT
        tile_up_x = x + self.TILE_OFFSET_WIDTH
        tile_down_y = y - self.TILE_OFFSET_HEIGHT

        self.lightning_tile.x = tile_down_x
        self.lightning_tile.y = tile_up_y
        self.lightning_tile.visible = True
        self.match_label(self.lightning_tile, self.lightning_label)

        self.rock_tile.x = tile_up_x
        self.rock_tile.y = tile_up_y
        self.rock_tile.visible = True
        self.match_label(self.rock_tile, self.rock_label)

        self.ice_tile.x = tile_down_x
        self.ice_tile.y = tile_down_y
        self.ice_tile.visible = True
        self.match_label(self.ice_tile, self.ice_label)

        self.poison_tile.x = tile_up_x
        self.poison_tile.y = tile_down_y
        self.poison_tile.visible = True
        self.match_label(self.poison_tile, self.poison_label)

    def match_label(self, tile, label):
        label.x = tile.x
        label.y = tile.y - 50
        label.visible = True

    def show_upgrades(self, slot):
        tower = self.tower_is_active(slot)

        x = slot.x
        y = slot.y
        tile_down_x = x - self.TILE_OFFSET_WIDTH
        tile_up_y = y + self.TILE_OFFSET_HEIGHT
        tile_up_x = x + self.TILE_OFFSET_WIDTH
        tile_down_y = y - self.TILE_OFFSET_HEIGHT

        self.attack_tile.x = tile_down_x
        self.attack_tile.y = tile_up_y
        self.attack_tile.visible = True

        self.attack_label.x = self.attack_tile.x
        self.attack_label.y = self.attack_tile.y - 50
        self.attack_label.visible = True
        self.attack_label.text = str(int(tower.get_attack_price()))

        self.speed_tile.x = tile_up_x
        self.speed_tile.y = tile_up_y
        self.speed_tile.visible = True

        self.speed_label.x = self.speed_tile.x
        self.speed_label.y = self.speed_tile.y - 50
        self.speed_label.visible = True
        self.speed_label.text = str(int(tower.get_speed_price()))

        self.destroy_tile.x = x
        self.destroy_tile.y = tile_down_y
        self.destroy_tile.visible = True

    def hide_tiles(self):
        self.lightning_tile.visible = False
        self.rock_tile.visible = False
        self.ice_tile.visible = False
        self.poison_tile.visible = False
        self.lightning_label.x = -50
        self.rock_label.x = -50
        self.ice_label.x = -50
        self.poison_label.x = -50

    def hide_upgrades(self):
        self.attack_tile.visible = False
        self.speed_tile.visible = False
        self.speed_label.x = -50
        self.attack_label.x = -50
        self.destroy_tile.visible = False

    def slot_is_clicked(self, origin, x, y):
        clicked_x = (origin[0] - self.SLOT_CLICK_BOX_X < x
                     and x < origin[0] + self.SLOT_CLICK_BOX_X)
        clicked_y = (origin[1] - self.SLOT_CLICK_BOX_Y < y
                     and y < origin[1] + self.SLOT_CLICK_BOX_Y)
        return clicked_x and clicked_y

    def tile_is_clicked(self, origin, x, y):
        clicked_x = (origin[0] - self.TILE_CLICK_BOX_X < x
                     and x < origin[0] + self.TILE_CLICK_BOX_X)
        clicked_y = (origin[1] - self.TILE_CLICK_BOX_Y < y
                     and y < origin[1] + self.TILE_CLICK_BOX_Y)
        return clicked_x and clicked_y

    def tower_is_active(self, focused):
        for tower_name in self.towers[(focused.x, focused.y,)]:
            tower = self.towers[(focused.x, focused.y,)][tower_name]
            if tower.active:
                return tower
        return None
