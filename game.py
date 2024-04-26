import pyglet
from pyglet.window import key
from pyglet import shapes
import random

# Load the bullet sound and to initialize the score and the label
bullet_sound = pyglet.media.load('resources/sound/pang.mp3', streaming=False)
big_bullet_sound = pyglet.media.load('resources/sound/big_pang.mp3', streaming=False)
score = 0

# Window dimensions
window_width = 800
window_height = 600

# Create the window
window = pyglet.window.Window(window_width, window_height, "Space Shooter")

# Create a batch to draw the stars and player
batch = pyglet.graphics.Batch()

# Create the score label
score_label = pyglet.text.Label('Score: 0', font_name='Arial', font_size=36, x=10, y=window_height - 50, batch=batch)

# Create a list to hold the stars and bullets
stars = []
bullets = []
points = []
big_bullets = []

# Create the stars
for _ in range(50):
    star = shapes.Circle(random.randint(0, window_width), random.randint(0, window_height), 2, color=(255, 255, 255), batch=batch)
    stars.append(star)

# Create the point
point = shapes.Circle(random.randint(0, window_width), random.randint(0, window_height), 5, color=(0, 255, 0), batch=batch)
points.append(point)

# Load the player's ship image
player_image = pyglet.image.load('resources/image/ship.png')
player_image.anchor_x = player_image.width // 2
player_image.anchor_y = player_image.height // 2

# Create the player sprite and scale it down to 70% of its original size
player = pyglet.sprite.Sprite(player_image, x=window_width // 2, y=window_height // 2, batch=batch)
player.scale = 0.2

def collides_with(sprite, point):
    dx = sprite.x - point.x
    dy = sprite.y - point.y
    distance = (dx * dx + dy * dy) ** 0.5
    return distance < 50  # Adjust this value as needed

# Define the game logic
def update(dt):
    global score
    # Move the player
    if 'up' in keys and player.y < window_height - player.height // 2:
        player.y += 10
    if 'down' in keys and player.y > player.height // 2:
        player.y -= 10
    if 'left' in keys and player.x > player.width // 2:
        player.x -= 10
    if 'right' in keys and player.x < window_width - player.width // 2:
        player.x += 10
    
    # Move the bullets
    for bullet in bullets:
        bullet.x += 10
        if bullet.x > window_width:
            bullets.remove(bullet)
            bullet.delete()
            
    # Move the big bullets
    for big_bullet in big_bullets:
        big_bullet.x += 6
        if big_bullet.x > window_width:
            big_bullets.remove(big_bullet)
            big_bullet.delete()
        
    # Move the stars
    for star in stars:
        star.x -= 2.5
        if star.x < 0:
            star.x = window_width
            star.y = random.randint(0, window_height)
            
    # Check for collisions with point objects
    for point in points:
        if collides_with(player, point):
            # Increase the score and update the score label
            score += 1
            score_label.text = f'Score: {score}'

            # Remove the point from the list and delete it
            points.remove(point)
            point.delete()

            # Create a new point at a random location
            new_point = shapes.Circle(random.randint(0, window_width), random.randint(0, window_height), 5, color=(0, 255, 0), batch=batch)
            points.append(new_point)

# Create a set to hold the current keys
keys = set()

# Event handlers
@window.event
def on_draw():
    window.clear()
    batch.draw()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.UP:
        keys.add('up')
    elif symbol == key.DOWN:
        keys.add('down')
    elif symbol == key.LEFT:
        keys.add('left')
    elif symbol == key.RIGHT:
        keys.add('right')
    elif symbol == key.SPACE:  # Create a bullet when space is pressed
        bullet = shapes.Rectangle(player.x, player.y, 10, 2, color=(255, 255, 255), batch=batch)
        bullets.append(bullet)
        bullet_sound.play()  # Play the bullet sound
    elif symbol == key.R:  # Create a big bullet when R is pressed
        big_bullet = shapes.Rectangle(player.x, player.y, 20, 4, color=(255, 255, 0), batch=batch)  # Bigger and yellow
        big_bullets.append(big_bullet)
        big_bullet_sound.play()
    elif symbol == key.ESCAPE:  # Terminate the game when ESC is pressed
        window.close()

@window.event
def on_key_release(symbol, modifiers):
    if symbol == key.UP:
        keys.remove('up')
    elif symbol == key.DOWN:
        keys.remove('down')
    elif symbol == key.LEFT:
        keys.remove('left')
    elif symbol == key.RIGHT:
        keys.remove('right')

# Schedule the update function
pyglet.clock.schedule_interval(update, 1/60.0)

# Run the game
pyglet.app.run()