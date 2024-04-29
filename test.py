import pyglet
from pyglet import window
from pyglet.window import key

window = pyglet.window.Window()

@window.event
def on_draw():
    window.clear()

keys = set()

def update(dt):

    # Move the player
    if "UP" in keys:
        print("up")
    if "DOWN" in keys:
        print("down")
    if "RIGHT" in keys:
        print("right")
    if "LEFT" in keys:
        print("left")

@window.event
def on_key_press(symbol, modifiers):
    
    print(key.symbol_string(symbol))
    keys.add(key.symbol_string(symbol))

@window.event
def on_key_release(symbol, modifiers):
    
    keys.remove(key.symbol_string(symbol))

# Schedule the update function
pyglet.clock.schedule_interval(update, 1/60.0)


# Run the game
pyglet.app.run()