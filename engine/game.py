import pyglet
import random
import time

from engine.grid import Grid
from engine.handler import ClickHandler
from engine.log_spam import LogSpam
from engine.spawner import Spawner
from engine.wallet import Wallet
from engine.tower_sprites.lightning_tower import LightningTowerSprite
from engine.tower_sprites.rock_tower import RockTowerSprite
from engine.tower_sprites.poison_tower import PoisonTowerSprite
from engine.tower_sprites.ice_tower import IceTowerSprite

from loop import Loop
from towers.lightning_tower import LightningTower, lightning_build_price
from towers.rock_tower import RockTower, rock_build_price
from towers.poison_tower import PoisonTower, poison_build_price
from towers.ice_tower import IceTower, ice_build_price


START_MONEY = 200
ROUND_OVER_TIMER = 3
DEV = False


class Game:

    # -------------- Game Loop API ----------------
    def stop(self):
        self.stop_game()

    def start_round(self, level):
        self.wave_number += 1
        self.update_wave_label(self.wave_number)
        print("Starting Wave " + str(self.wave_number))
        self.is_wave_done = False
        for spawner in self.spawners:
            spawner.respawn(level)

    def is_round_over(self):
        return self.is_wave_done

    def add_lives(self, amount):
        self.lives += amount

    def add_reward(self, reward):
        self.wallet.add_amount(reward)

    def get_defeated_monsters(self):
        monsters = list()
        for sprite in self.defeated_monsters:
            # monster object in sprite holds state
            monsters.append(sprite.get_monster_object())
        return monsters

    def add_new_monsters(self, monsters):
        self.add_monsters(monsters)

    # ------------- End Loop API ---------------

    FPS = 30  # frames per second (aka speed of the game)

    def __init__(self, background, lives=3):
        window_width = 1400
        rows = 9
        cols = 16
        window_ratio = cols / rows
        window_height = int(window_width / window_ratio)

        # Set up a window
        window = pyglet.window.Window(window_width, window_height)

        pyglet.font.add_file('assets/PressStart2P-Regular.ttf')
        self.font = pyglet.font.load('Press Start 2P')

        # Set up batch and ordered groups
        self.bg_batch = pyglet.graphics.Batch()
        self.main_batch = pyglet.graphics.Batch()
        self.hidden = pyglet.graphics.OrderedGroup(0)
        self.background = pyglet.graphics.OrderedGroup(1)
        self.midground = pyglet.graphics.OrderedGroup(2)
        self.terrainground = pyglet.graphics.OrderedGroup(3)
        self.monster_layer = pyglet.graphics.OrderedGroup(10)
        self.finish_ground = pyglet.graphics.OrderedGroup(11)
        self.foreground = pyglet.graphics.OrderedGroup(99)

        # Set up window and grid variables
        self.window = window
        self.window_block_width = cols
        self.cols = cols
        self.rows = rows
        self.grid = Grid(self.rows, self.cols, self.window)

        # Set up background
        bg_image = pyglet.image.load(background)
        self.bg_sprite = pyglet.sprite.Sprite(
            bg_image,
            batch=self.bg_batch,
            group=self.background
        )
        height_scale = self.window.height / self.bg_sprite.height
        width_scale = self.window.width / self.bg_sprite.width
        self.bg_sprite.scale = max(height_scale, width_scale)

        self.lives = lives
        self.draw_life_counter()

        self.button_close_xy = self.grid.calculate_xy_from_percentage(
            (0.05, 0.92,)
        )
        self.close_button = self.add_close_button()

        # Set up character sprite info
        self.characters = dict()
        self.throwables = list()

        # State keeping variables
        self.lock = False
        self.round_over_timer = ROUND_OVER_TIMER
        self.safety_counter = 10
        self.log_spam = LogSpam()

        # Set up environment objects
        self.obstacles = dict()
        self.terrain = dict()
        self.tower_spots = dict()
        self.towers = dict()
        self.spawners = list()
        self.path_steps = list()
        self.finish = list()
        self.click_handler = None

        # Set up game loop elements
        self.wave_number = 1
        self.is_wave_done = False
        self.money = 0
        self.draw_wave_counter()
        self.draw_money_counter()
        self.defeated_monsters = list()
        self.defeated_set = set()
        self.wallet = Wallet(START_MONEY)
        self.loop = Loop(self)

    def on_draw(self):
        self.window.clear()
        self.bg_batch.draw()
        self.main_batch.draw()

    def start_game(self):
        build_prices = {
            'lightning': lightning_build_price,
            'ice': ice_build_price,
            'rock': rock_build_price,
            'poison': poison_build_price,
        }
        self.click_handler = ClickHandler(
            self.tower_spots, self.towers, self.wallet, build_prices,
            self.window, self.main_batch, self.foreground
        )

        def on_mouse_press(x, y, button, modifiers):
            if self.check_close_button_clicked(x, y):
                self.stop_game()
                return
            self.click_handler.handle_click(x, y)

        self.window.push_handlers(
            on_draw=self.on_draw
        )
        self.window.push_handlers(on_mouse_press)
        pyglet.clock.schedule_interval(self.update, 1.0 / self.FPS)

    def stop_game(self):
        print('Game shutting down')
        time.sleep(5)
        pyglet.clock.unschedule(self.update)
        self.window.pop_handlers()
        self.window.remove_handlers()
        pyglet.app.exit()

    def update(self, dt):
        if self.money != self.wallet.get_amount():
            self.money = self.wallet.get_amount()
            self.update_money_label(self.money)

        round_over = True
        monsters = list()
        self.defeated_monsters = list()
        for spawner in self.spawners:
            spawner.update(dt)
            if len(spawner.monster_queue) > 0:
                round_over = False
            for monster in spawner.spawned:
                if monster.at_destination():
                    spawner.spawned.remove(monster)
                    monster.hide()
                    self.lives = max(self.lives - 1, 0)
                    self.update_life_label(self.lives)
                elif not monster.is_defeated:
                    monsters.append(monster)
                else:
                    if monster.id not in self.defeated_set:
                        self.defeated_monsters.append(monster)
                        self.defeated_set.add(monster.id)

        for key in self.towers:
            pos_towers = self.towers[key]
            for tower in list(pos_towers.values()):
                tower.update(dt, monsters)

        # Call the game loop object to update loop status
        self.loop.update()

        # Round or game is over and controls locked
        if self.lock:
            self.round_over_timer -= dt
            if self.round_over_timer <= 0:
                # Game is over
                if self.lives <= 0:
                    self.stop_game()
                # Round is over
                else:
                    self.lock = False
                    self.round_over_timer = ROUND_OVER_TIMER
            else:
                return

        if len(monsters) > 0:
            round_over = False

        if self.lives <= 0:
            if not self.lock:
                print("Game Over, you lost all your lives")
            self.lock = True

        if round_over:
            if not self.lock:
                print("Wave {num} Over!".format(num=str(self.wave_number)))
                self.is_wave_done = True
            self.lock = True

    def add_finish(self, coord):
        x, y = self.grid.calculate_xy_from_percentage(coord)
        finish_image = pyglet.resource.image('assets/finish.png')
        finish_image.anchor_x = finish_image.width // 2
        finish_image.anchor_y = finish_image.height // 2
        finish = pyglet.sprite.Sprite(
            finish_image,
            batch=self.main_batch,
            x=x,
            y=y + self.grid.cell_length // 4,  # Account for offset of road
            group=self.finish_ground
        )
        finish.scale = 0.33
        self.finish.append(finish)

    def add_tower_spots(self, coords):
        self.tmp_ranges = list()
        for coord_name in coords:
            x, y = self.grid.calculate_xy_from_percentage(coord_name)
            sprite = self._add_spot(x, y)
            self.tower_spots[(x, y,)] = sprite
            self.add_towers(x, y)

    def add_towers(self, x, y):
        lightning_tower = LightningTowerSprite(
            x, y, LightningTower(), self.main_batch)
        lightning_tower.deactivate()
        rock_tower = RockTowerSprite(x, y, RockTower(), self.main_batch)
        rock_tower.deactivate()
        poison_tower = PoisonTowerSprite(
            x, y, PoisonTower(), self.main_batch
        )
        poison_tower.deactivate()
        ice_tower = IceTowerSprite(x, y, IceTower(), self.main_batch)
        ice_tower.deactivate()
        self.towers[(x, y,)] = {
            'lightning_tower': lightning_tower,
            'rock_tower': rock_tower,
            'ice_tower': ice_tower,
            'poison_tower': poison_tower
        }

    def _add_spot(self, x, y):
        spot_image = pyglet.resource.image('assets/background/dot.png')
        spot_image.anchor_x = spot_image.width // 2
        spot_image.anchor_y = spot_image.height
        spot_sprite = pyglet.sprite.Sprite(
            spot_image,
            batch=self.main_batch,
            x=x,
            y=y,
            group=self.hidden
        )
        if not DEV:
            spot_sprite.visible = False
        spot_sprite.scale = 0.5
        return spot_sprite

    def add_monsters(self, monsters):
        converted_monsters = list()
        for monster in monsters:
            # Convert starting xy
            start_x, start_y = self.grid.calculate_xy_from_percentage(
                (monster.x, monster.y,)
            )
            monster.x = start_x
            monster.y = start_y
            # Convert path
            path = monster.path
            converted_path = list()
            for step in path:
                x, y = self.grid.calculate_xy_from_percentage(step)
                if DEV:
                    target = pyglet.shapes.Circle(
                        x, y, 10,
                        color=(255, 0, 0),
                        batch=self.main_batch,
                        group=self.hidden
                    )
                    self.path_steps.append(target)
                converted_path.append((x, y,))
            monster.path = converted_path
            converted_monsters.append(monster)
        spawner = Spawner(converted_monsters,
                          self.main_batch, self.monster_layer)
        self.spawners.append(spawner)

    def _add_spawner(self, coord, path, config):
        converted_path = list()
        for step in path:
            x, y = self.grid.calculate_xy_from_percentage(step)
            if DEV:
                target = pyglet.shapes.Circle(
                    x, y, 10,
                    color=(255, 0, 0),
                    batch=self.main_batch,
                    group=self.hidden
                )
                self.path_steps.append(target)
            converted_path.append((x, y,))
        self.spawners.append(
            Spawner(config, coord, converted_path, self.grid,
                    self.main_batch, self.monster_layer)
        )

    def respawn_monsters(self):
        pass

    def add_selector_func(self, key, func):
        tower = self.towers[key]
        tower.set_selector_func(func)

    def draw_life_label(self):
        self.life_label = pyglet.text.Label(
            text="",
            x=self.window.width * 0.83,
            y=self.window.height * 0.90,
            font_name='Press Start 2P',
            font_size=14,
            anchor_x='left',
            batch=self.main_batch,
            group=self.foreground
        )
        self.life_label.draw()

    def draw_life_counter(self):
        self.draw_life_label()
        self.update_life_label(self.lives)
        life_icon = pyglet.resource.image(
            'assets/heart.png'
        )
        life_icon.anchor_x = life_icon.width * 1.5
        life_icon.anchor_y = life_icon.height * 0.1
        self.life_sprite = pyglet.sprite.Sprite(
            life_icon,
            x=self.window.width * 0.83,
            y=self.window.height * 0.9,
            batch=self.main_batch,
            group=self.foreground
        )

    def update_life_label(self, lives):
        self.life_label.text = "Lives:{lives}".format(lives=lives)

    def draw_wave_label(self):
        self.wave_label = pyglet.text.Label(
            text="",
            x=self.window.width * 0.83,
            y=self.window.height * 0.84,
            font_name='Press Start 2P',
            font_size=14,
            anchor_x='left',
            batch=self.main_batch,
            group=self.foreground
        )
        self.wave_label.draw()

    def draw_wave_counter(self):
        self.draw_wave_label()
        self.update_wave_label(self.wave_number)
        wave_icon = pyglet.resource.image(
            'assets/skull.png'
        )
        wave_icon.anchor_x = wave_icon.width * 1.5
        wave_icon.anchor_y = wave_icon.height * 0.1
        self.wave_sprite = pyglet.sprite.Sprite(
            wave_icon,
            x=self.window.width * 0.83,
            y=self.window.height * 0.84,
            batch=self.main_batch,
            group=self.foreground
        )
        self.wave_sprite.scale = 0.35

    def update_wave_label(self, wave):
        self.wave_label.text = "Wave:{wave}".format(wave=wave)

    def draw_money_label(self):
        self.money_label = pyglet.text.Label(
            text="",
            x=self.window.width * 0.83,
            y=self.window.height * 0.78,
            font_name='Press Start 2P',
            font_size=14,
            anchor_x='left',
            batch=self.main_batch,
            group=self.foreground
        )
        self.money_label.draw()

    def draw_money_counter(self):
        self.draw_money_label()
        self.update_money_label(self.money)
        money_icon = pyglet.resource.image(
            'assets/money.png'
        )
        money_icon.anchor_x = money_icon.width * 1.5
        money_icon.anchor_y = money_icon.height * 0.1
        self.money_sprite = pyglet.sprite.Sprite(
            money_icon,
            x=self.window.width * 0.83,
            y=self.window.height * 0.78,
            batch=self.main_batch,
            group=self.foreground
        )
        self.money_sprite.scale = 0.7

    def update_money_label(self, money):
        self.money_label.text = "Money:{money}".format(money=money)

    def add_close_button(self):
        image = pyglet.resource.image('assets/button_close.png')
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2
        button_sprite = pyglet.sprite.Sprite(
            image,
            x=self.button_close_xy[0],
            y=self.button_close_xy[1],
            batch=self.main_batch,
            group=self.foreground
        )
        button_sprite.scale = 0.5
        return button_sprite

    def check_close_button_clicked(self, x, y):
        bx = self.button_close_xy[0]
        by = self.button_close_xy[1]
        height = self.close_button.height * self.close_button.scale
        width = self.close_button.width * self.close_button.scale
        x_clicked = (bx - width // 2 < x and
                     x < bx + width // 2)
        y_clicked = (by - height // 2 < y and
                     y < by + height // 2)
        return x_clicked and y_clicked
