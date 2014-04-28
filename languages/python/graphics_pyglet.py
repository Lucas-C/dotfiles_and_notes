# http://steveasleep.com/pyglettutorial.html
# http://www.pyglet.org/doc/api/index.html
import pyglet

window = pyglet.window.Window(800, 600)

drawables = []

@window.event
def on_draw():
    window.clear()
    for d in drawables:
        d.draw()

#drawables.append(pyglet.graphics.Batch())

pyglet.app.run()

