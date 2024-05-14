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
        self.bg_music_player = None
        # TODO: self.boss_music = pyglet.media.load('resources/sound/boss_music.mp3') #NYI
        # TODO: self.pause_music = pyglet.media.load('resources/sound/pause_music.mp3') #NYI
     
    def play_bullet_sound(self):
        self.bullet_sound.play()

    def play_big_bullet_sound(self):
        self.big_bullet_sound.play()
        
    def play_background_music(self):
        if not self.bg_music_player:
            self.bg_music_player = self.background_music.play()
            self.bg_music_player.volume = 1.0
    
    def pause_background_music(self):
        if self.bg_music_player:
            self.bg_music_player.pause()
        
    def resume_background_music(self):
        if self.bg_music_player:
            self.bg_music_player.play()
        
    def play_enemy_killed(self):
        enemy_killed_sound = pyglet.media.load('resources/sound/die.mp3', streaming=False)
        enemy_killed_sound.play()
    
    ## NYI (Need to find/create appropriate boss music)   
    # def play_boss_music(self):
    #     bg_music_player = self.boss_music.play()
    #     bg_music_player.volume = 1.0

class GameWindow(pyglet.window.Window):
    def __init__(self, width, height, *args, **kwargs):
        super().__init__(width, height, *args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        self.pause_screen_batch = pyglet.graphics.Batch()  # Separate batch for pause screen elements
        self.sound_manager = SoundManager()
        self.points = [Point(random.randint(0, self.width), random.randint(0, self.height), self.batch) for _ in range(1)]
        self.score_label = pyglet.text.Label('Score: 0', font_name='Courier New', font_size=16, x=self.width // 2, y=self.height - 780,
                                             color=(200, 255, 215, 200), bold=True, batch=self.batch)   
        self.keys = set()
        self.score = 0
        self.player = Player(self.width // 2, self.height // 2, self.width // 2, self.height, self.batch)
        self.enemy = Enemy(800, self.height // 2, self.width, self.height, self.batch)
        self.bullets = self.player.bullets
        self.big_bullets = self.player.big_bullets
        self.dots = [Dot(random.randint(0, self.width), random.randint(0, self.height), self.batch) for _ in range(100)]
        self.stars = [Star(random.randint(0, self.width), random.randint(0, self.height), self.batch) for _ in range(100)]
        
        # Pause screen variables
        self.paused = False
        self.game_clock = None
        
        # Initialize blink timer for pause screen
        self.blink_timer = 0
        self.blink_interval = 0.5  # Blink interval in seconds
        self.show_continue_label = True 

    def on_draw(self):
        self.clear()
        if not self.paused:
            self.batch.draw()
        else:
            self.draw_pause_screen()
            
        # Toggle the visibility of continue label for blinking effect
        if self.paused:
            self.blink_timer += 1
            if self.blink_timer >= self.blink_interval * 60:  # Convert blink interval to frames (assuming 60 FPS)
                self.show_continue_label = not self.show_continue_label
                self.blink_timer = 0        
        
    def draw_pause_screen(self):
        self.paused = True
        self.clear()
        
        pause_bg_rect_color = (0, 0, 0, 128)  # Black with increased transparency for darkness
        pause_rect_border_color = (255, 255, 255, 255)  # White border for the pause screen rectangle
        pause_rect_width = self.width // 2
        pause_rect_height = self.height // 2
        pause_rect_x = (self.width - pause_rect_width) // 2
        pause_rect_y = (self.height - pause_rect_height) // 2
        pause_rect_color = (0,0,250, 255)  # Dark blue
        
        pause_bg_rect = shapes.Rectangle(x=0, y=0, width=self.width, height=self.height, color=pause_bg_rect_color, batch=self.pause_screen_batch)
        pause_rect_border = shapes.Rectangle(x=pause_rect_x - 4, y=pause_rect_y - 4, width=pause_rect_width + 7, height=pause_rect_height + 7,
                                            color=pause_rect_border_color, batch=self.pause_screen_batch)
        pause_rect = shapes.Rectangle(x=pause_rect_x, y=pause_rect_y, width=pause_rect_width, height=pause_rect_height, color=pause_rect_color, batch=self.pause_screen_batch)
        pause_label = pyglet.text.Label('PAUSE', font_name='Arial', font_size=72,
                                        x=self.width // 2, y=self.height // 2 + pause_rect_height // 4,
                                        anchor_x='center', anchor_y='center',
                                        color=(255, 255, 255, 255), batch=self.pause_screen_batch)
        
        # Draw continue label only when show_continue_label is True
        if self.show_continue_label:
            continue_label = pyglet.text.Label('Press P to continue...', font_name='Arial', font_size=18,
                                                x=self.width // 2, y=self.height // 2 - pause_rect_height // 4,
                                                anchor_x='center', anchor_y='center',
                                                color=(255, 255, 255, 255), batch=self.pause_screen_batch)
        else:
            continue_label = None

        self.pause_screen_batch.draw()  # Draw all pause screen elements



                            
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
        elif symbol == key.P:  # Pause/unpause with 'P' key
            self.paused = not self.paused

    def on_key_release(self, symbol, modifiers):
        if symbol == key.UP:
            self.keys.remove('up')
        elif symbol == key.DOWN:
            self.keys.remove('down')
        elif symbol == key.LEFT:
            self.keys.remove('left')
        elif symbol == key.RIGHT:
            self.keys.remove('right')
            
    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.sound_manager.pause_background_music()
            self.pause_game_clock()
        else:
            self.sound_manager.resume_background_music()
            self.resume_game_clock()
            
    def pause_game_clock(self):
        if self.game_clock:
            self.game_clock.unschedule()

    def resume_game_clock(self):
        if self.game_clock:
            self.game_clock.schedule_interval(self.update, 1/60.0)
        else:
            self.game_clock = pyglet.clock.schedule_interval(self.update, 1/60.0)

    def update(self, dt):
        if not self.paused:
            self.player.update(self.keys)
            self.enemy.update()
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
            
        for star in self.stars:
            star.update()
        
        # Bullet collision with enemy
        for bullet in self.bullets:
            if self.enemy.collides_with(bullet):
                # Play sound for bullet hit
                self.sound_manager.play_enemy_killed()
                print("Bullet hit") # Alert that big bullet hit enemy
                self.bullets.remove(bullet)  # Remove bullet from the list
                bullet.delete()
                self.enemy.respawn()  # Respawn enemy
                # TODO: Increment score when enemy is killed

        # Big bullet collision with enemy
        for big_bullet in self.big_bullets:
            if self.enemy.collides_with(big_bullet):
                self.sound_manager.play_enemy_killed()
                print("Big bullet hit") # Alert that big bullet hit enemy
                self.big_bullets.remove(big_bullet) # Remove big bullet from the list
                big_bullet.delete()          
                self.enemy.respawn()  # Respawn enemy
               # TODO: Increment score when enemy is killed
               
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
    def __init__(self, x, y, window_width, window_height, batch):
        super().__init__(pyglet.image.load('resources/image/enemy.png'), x=x, y=y, batch=batch)
        self.scale = 0.05
        self.speed = -5
        self.window_width = window_width
        self.window_height = window_height
        self.respawn_timer = random.uniform(3, 10)

    def collides_with(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        distance = (dx * dx + dy * dy) ** 0.5
        distance_change = distance < self.width / 2 # Collision radius.
        if distance_change:  # Draw collision circle only if there's a collision
            self.draw_collision_circle(distance)
        return distance_change

    def respawn(self):
        self.x = self.window_width
        self.y = random.randint(0, self.window_height - self.height)
        self.respawn_timer = random.uniform(3, 10)

    def draw_collision_circle(self, distance):
        shapes.Circle(self.x + self.width / 2, self.height - self.y / 2, distance, color=(255, 0, 0), batch=self.batch)
    
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
        super().__init__(x, y, 2, color=(128, 128, 128), batch=batch)

    def update(self):
        global window_width
        self.x -= 2.5
        if self.x < 0:
            self.x = window_width
            
class Dot(shapes.Circle):
    def __init__(self, x, y, batch):
        super().__init__(x, y, 2, color=(128, 128, 128), batch=batch)

    def update(self):
        global window_width
        self.x -= 2.5
        if self.x < 0:
            self.x = window_width

class Star(shapes.Star):
    def __init__(self, x, y, batch):
        super().__init__(x, y, 3, 3, 2, color=(255, 100, 0), batch=batch)

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
    window.sound_manager.play_background_music()
    pyglet.clock.schedule_interval(window.update, 1/60.0)
    pyglet.app.run()
