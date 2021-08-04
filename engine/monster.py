import math
import pyglet

from engine.util import get_files_in_path


class MonsterSprite:

    FADE_OUT_SPEED = 75

    def __init__(self, id, path, x, y, steps, _monster, batch=None, group=None):
        self.id = id
        self.path = path
        self.batch = batch
        self.group = group
        # These are the true x/y we consider the sprite to be at
        self.x = x
        self.y = y
        self.steps = steps
        self.angle = None
        self.scale = 0.25
        self.animation = None

        self.velocity_x = 0
        self.velocity_y = 0
        self.dest_x = None
        self.dest_y = None

        # Keep track of what step in path monster is on
        self.step_i = 0

        # Sprite x/y is offset due to the anchor point not being in center
        self.sprite = self._generate_sprite()
        self._monster = _monster
        self.speed = self._monster.speed
        self.health = self._monster.hp

        self.max_health_width = 40
        self.health_bar = self.get_health_bar()

        self.is_defeated = False
        self.done = False

        self.adjust_destination()

    def hide(self):
        self.sprite.visible = False
        self.health_bar.visible = False

    def show(self):
        self.sprite.visible = True
        self.health_bar.visible = True

    def _generate_sprite(self):
        walk_path = self.path + "move/"
        defeated_path = self.path + "defeated/"
        # Set up animation for character sprite
        walk_frames = [pyglet.resource.image(walk_path + f)
                       for f in get_files_in_path(walk_path)]
        defeated_frames = [pyglet.resource.image(defeated_path + f)
                           for f in get_files_in_path(defeated_path)]
        self.walk_animation = pyglet.image.Animation.from_image_sequence(
            walk_frames,
            duration=0.1,
            loop=True
        )
        self.walk_animation_rev = self.walk_animation.get_transform(
            flip_x=True
        )
        self.defeated_animation = pyglet.image.Animation.from_image_sequence(
            defeated_frames,
            duration=0.05,
            loop=False
        )
        self.defeated_animation_rev = self.defeated_animation.get_transform(
            flip_x=True
        )

        self.animation = self.walk_animation

        # Set up character sprite
        monster_sprite = pyglet.sprite.Sprite(
            self.animation,
            group=self.group,
            batch=self.batch,
            x=self.convert_x(),
            y=self.convert_y()
        )
        monster_sprite.scale = self.scale

        return monster_sprite

    def convert_x(self):
        # Need these to offset the sprite due to anchor being on the bottom left
        if self.velocity_x >= 0:
            return self.x - self.animation.get_max_width() * self.scale / 2
        else:
            scaled = self.animation.get_max_width() * self.scale
            orig = self.x + scaled / 2
            return orig - scaled * self._monster.ANCHOR_OFFSET

    def convert_y(self):
        # Need these to offset the sprite due to anchor being on the bottom left
        return self.y - self.animation.get_max_height() * self.scale / 6

    def at_destination(self):
        return self.done

    def fade_out(self, dt):
        diff = self.FADE_OUT_SPEED * dt
        body_o = self.sprite.opacity
        if body_o > 0:
            body_diff = body_o - diff
            self.sprite.opacity = max(body_diff, 0)
        else:
            self.sprite.visible = False
        health_o = self.health_bar.opacity
        if health_o > 0:
            health_diff = health_o - diff
            self.health_bar.opacity = health_diff
        else:
            self.sprite.visible = False

    def update(self, dt):
        if self.speed != self._monster.speed:
            self.speed = self._monster.speed
            self.adjust_speed(self.speed)
        if self.is_defeated:
            if (self.sprite.image == self.walk_animation
                    or self.sprite.image == self.walk_animation_rev):
                self.update_sprite_animation()
            self.fade_out(dt)
            return True
        else:
            # Apply status effects
            self._monster.update_status(dt)

            self.health_bar.x = self.x - int(self.sprite.width * 3/8)
            self.health_bar.y = self.y + self.sprite.height
            new_width = self.max_health_width * \
                (max(self._monster.hp, 0) / self.health)
            if new_width >= 0:
                self.health_bar.width = new_width
            if self._monster.defeated:
                self.is_defeated = True

        reached_dest = self.move(dt)
        if reached_dest:
            self.adjust_destination()

    def move(self, dt):
        new_x, reached_x = self.handle_move(
            self.x, self.dest_x, self.velocity_x, dt)
        new_y, reached_y = self.handle_move(
            self.y, self.dest_y, self.velocity_y, dt)
        self.x = new_x
        self.y = new_y
        self.sprite.x = self.convert_x()
        self.sprite.y = self.convert_y()
        return reached_x or reached_y

    def handle_move(self, orig, dest, speed, dt):
        reached_dest = False
        new = orig + speed * dt
        if speed >= 0:
            reached_dest = dest < new
        else:
            reached_dest = dest > new
        if reached_dest:
            return dest, True
        return new, False

    def adjust_destination(self):
        if self.step_i >= len(self.steps):
            self.done = True
            return
        self.dest_x, self.dest_y = self.steps[self.step_i]
        self.step_i += 1
        dx = self.dest_x - self.x
        dy = self.dest_y - self.y

        # Prevent divide by zero
        if dx == 0:
            if dy > 0:
                self.velocity_y = self.speed
            else:
                self.velocity_y = -self.speed
            self.velocity_x = 0
            return

        ratio = abs(dy / dx)
        self.angle = math.atan(ratio)
        velocity_y = math.sin(self.angle) * self.speed
        velocity_x = math.cos(self.angle) * self.speed
        self.velocity_x = velocity_x if dx > 0 else -velocity_x
        self.velocity_y = velocity_y if dy > 0 else -velocity_y
        self.update_sprite_animation()

    def update_sprite_animation(self):
        if not self.is_defeated:
            if self.velocity_x >= 0:
                self.animation = self.walk_animation
            else:
                self.animation = self.walk_animation_rev
        else:
            if self.velocity_x >= 0:
                self.animation = self.defeated_animation
            else:
                self.animation = self.defeated_animation_rev
        self.sprite.image = self.animation
        self.sprite.x = self.convert_x()

    def adjust_speed(self, new_speed):
        if self.angle != None:
            velocity_y = math.sin(self.angle) * new_speed
            velocity_x = math.cos(self.angle) * new_speed
            self.velocity_x = velocity_x if self.velocity_x > 0 else -velocity_x
            self.velocity_y = velocity_y if self.velocity_y > 0 else -velocity_y

    def damage(self, damage_amount):
        print("{monster_id} got damaged for {dmg}".format(
            monster_id=self.id, dmg=damage_amount))
        self._monster.take_damage(damage_amount)

    def get_health_bar(self):
        health_bar = pyglet.shapes.Rectangle(
            self.x, self.y + self.sprite.height,
            self.max_health_width,
            5,
            color=(255, 0, 0),
            batch=self.batch,
            group=self.group
        )
        return health_bar

    def adjust_level(self, level):
        self._monster.respawn(level)

    def get_monster_object(self):
        return self._monster
