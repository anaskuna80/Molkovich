import pyglet
from pyglet.window import key
from pyglet import shapes
import random

window_width = 1000
window_height = 800

class SoundManager:
    def __init__(self):
        self.bullet_sound = pyglet.media.load('resources/sound/pang.mp3', streaming=False)
        self.big_bullet_sound = pyglet.media.load('resources/sound/big_pang.mp3', streaming=False)
        self.background_music = pyglet.media.load('resources/sound/game_music.mp3')

    def play_bullet_sound(self):
        self.bullet_sound.play()

    def play_big_bullet_sound(self):
        self.big_bullet_sound.play()
        
    def play_background_music(self):
        bg_music_player = self.background_music.play()
        bg_music_player.volume = 0.0
        fade_duration=5.0
        volume = 1.0
        volume_change = volume / (fade_duration * 60)

        # def change_volume(dt):
        #     nonlocal bg_music_player
        #     if bg_music_player.volume < 1.0 and isinstance(current_state, IntroState):
        #         bg_music_player.volume += volume_change

        #     if bg_music_player.volume > 0.0 and isinstance(current_state, GameState):
        #         play_background_music.fade_duration = 1.0
        #         bg_music_player.volume -= volume_change

        # pyglet.clock.schedule_interval(change_volume, 1/60.0)

class GameWindow(pyglet.window.Window):
    def __init__(self, width, height, *args, **kwargs):
        super().__init__(width, height, *args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        self.sound_manager = SoundManager()
        self.score_label = pyglet.text.Label('Score: 0', font_name='Courier New', font_size=16, x=self.width // 2, y=self.height - 780, color=(200, 255, 215, 200), bold=True, batch=self.batch)
        self.keys = set()
        self.score = 0
        self.player = Player(self.width // 2, self.height // 2, self.width // 2, self.height, self.batch)
        self.enemy = Enemy(800, self.height // 2, self.width, self.batch)
        self.dots = [Dot(random.randint(0, self.width), random.randint(0, self.height), self.batch) for _ in range(50)]
        self.points = [Point(random.randint(0, self.width), random.randint(0, self.height), self.batch) for _ in range(1)]
        self.bullets = self.player.bullets
        self.big_bullets = self.player.big_bullets

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP:
            self.keys.add('up')
        elif symbol == key.DOWN:
            self.keys.add('down')
        elif symbol == key.LEFT:
            self.keys.add('left')
        elif symbol == key.RIGHT:
            self.keys.add('right')
        elif symbol == key.SPACE:
            self.player.fire_bullet()
        elif symbol == key.R:
            self.player.fire_big_bullet()
        elif symbol == key.ESCAPE:
            self.close()

    def on_key_release(self, symbol, modifiers):
        if symbol == key.UP:
            self.keys.remove('up')
        elif symbol == key.DOWN:
            self.keys.remove('down')
        elif symbol == key.LEFT:
            self.keys.remove('left')
        elif symbol == key.RIGHT:
            self.keys.remove('right')

    def update(self, dt):
        self.player.update(self.keys)
        self.enemy.update()
        for dot in self.dots:
            dot.update()
        for point in self.points:
            if self.player.collides_with(point):
                self.score += 1
                self.score_label.text = f'Score: {self.score}'
                self.points.remove(point)
                point.delete()
                new_point = Point(random.randint(0, self.width), random.randint(0, self.height), self.batch)
                self.points.append(new_point)
        
        bullets_to_remove = []        
        for bullet in self.bullets:
            bullet.update(dt)
            if bullet.x > self.width:
                bullets_to_remove.append(bullet)
                
        for bullet in bullets_to_remove:
            self.bullets.remove(bullet)
            bullet.delete()

        big_bullets_to_remove = []
        for big_bullet in self.big_bullets:
            big_bullet.update(dt)
            if big_bullet.x > self.width:
                big_bullets_to_remove.append(big_bullet)

        for big_bullet in big_bullets_to_remove:
            self.big_bullets.remove(big_bullet)
            big_bullet.delete()
        

class Player(pyglet.sprite.Sprite):
    def __init__(self, x, y, window_width, window_height, batch):
        super().__init__(pyglet.image.load('resources/image/ship.png'), x=x, y=y, batch=batch)
        self.scale = 0.2
        self.window_width = window_width
        self.window_height = window_height
        self.sound_manager = SoundManager()
        self.batch = batch
        self.bullets = []
        self.big_bullets = []
        self.health = 3
        self.vx = 0
        self.vy = 0
        
        self.collision_offset_x = 40
        self.collision_offset_y = 25

    def update(self, keys):
        acceleration = 0.5  # Adjust the acceleration factor for smoother movement
        friction = 0.1  # Friction factor to gradually slow down the ship

        if 'up' in keys:
            self.vy += acceleration
        if 'down' in keys:
            self.vy -= acceleration
        if 'left' in keys:
            self.vx -= acceleration
        if 'right' in keys:
            self.vx += acceleration

        # Apply friction
        self.vx *= (1 - friction)
        self.vy *= (1 - friction)

        # Update position
        new_x = self.x + self.vx
        new_y = self.y + self.vy

        # Check boundaries
        if new_x > window_width - self.width:
            new_x = window_width - self.width
                        
        elif new_x < 0:
            new_x = 0

        if new_y > window_height - self.height:
            new_y = window_height - self.height
            
        elif new_y < 0:
            new_y = 0

        self.x = new_x
        self.y = new_y
            
    def fire_bullet(self):
        bullet = Bullet(self.x + 40, self.y + 25, self.batch, self.window_width)
        self.bullets.append(bullet)
        bullet.fire()
        self.sound_manager.play_bullet_sound()

    def fire_big_bullet(self):
        big_bullet = BigBullet(self.x + 40, self.y + 22, self.batch, self.window_width)
        self.big_bullets.append(big_bullet)
        big_bullet.fire()
        self.sound_manager.play_big_bullet_sound()

    def collides_with(self, other):
        dx = self.x + self.collision_offset_x - other.x
        dy = self.y + self.collision_offset_y - other.y
        distance = (dx * dx + dy * dy) ** 0.5
        return distance < 30  # Collision radius.

class Enemy(pyglet.sprite.Sprite):
    def __init__(self, x, y, window_width, batch):
        super().__init__(pyglet.image.load('resources/image/enemy.png'), x=x, y=y, batch=batch)
        self.scale = 0.2
        self.speed = -5
        self.window_width = window_width

    def update(self):
        self.x += self.speed
        if self.x < 0:
            self.x = self.window_width

class Bullet(shapes.Rectangle):
    def __init__(self, x, y, batch, window_width):
        super().__init__(x=x, y=y, color=(255, 255, 255), batch=batch, width=10, height=2)
        self.speed = 10
        self.window_width = window_width

    def fire(self):
        self.update(0)

    def update(self, dt):
        self.x += self.speed

class BigBullet(shapes.Rectangle):
    def __init__(self, x, y, batch, window_width):
        super().__init__(x, y, 15, 10, color=(78, 128, 255), batch=batch)
        self.speed = 6
        self.window_width = window_width

    def fire(self):
        self.update(0)

    def update(self, dt):
        self.x += self.speed

class Dot(shapes.Circle):
    def __init__(self, x, y, batch):
        super().__init__(x, y, 2, color=(255, 255, 255), batch=batch)

    def update(self):
        global window_width
        self.x -= 2.5
        if self.x < 0:
            self.x = window_width

class Point(shapes.Circle):
    def __init__(self, x, y, batch):
        super().__init__(x, y, 5, color=(0, 255, 0), batch=batch)

if __name__ == "__main__":
    window = GameWindow(window_width, window_height, "Molkovich")
    pyglet.clock.schedule_interval(window.update, 1/60.0)
    pyglet.app.run()
