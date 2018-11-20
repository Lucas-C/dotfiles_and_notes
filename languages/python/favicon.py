from contextlib import contextmanager
from gifmaze import GIFSurface, PixelCanvas, Animation


with closing(GIFSurface(width=16, height=16, bg_color=0)) as surface:
    surface.set_palette(
        # cf. https://www.rapidtables.com/web/color/RGB_Color.html#color-table
        [0, 0, 0]        # black
      + [255, 255, 255]  # white
      + [255, 0, 0]      # red
      + [0, 255, 0]      # green
      + [0, 0, 255]      # blue
      + [255, 255, 0]    # yellow
      + [0, 255, 255]    # cyan
      + [255, 0, 255]    # magenta
    )

    pixels = [(i, i) for i in range(0, 16, 2)]
    def favicon(pcanvas, render, pixels, speed):
        for i in range(len(pixels)):
            pcanvas.set_pixel(*pixels[i], i)  # 2nd param is a color palette index
            if i % speed == 0:
                yield render(pcanvas)
        yield render(pcanvas)
    anim = Animation(surface)
    anim.run(pixels=pixels, algo=favicon, speed=1, pcanvas=PixelCanvas(width=16, height=16), delay=5)

    surface.save('favicon.gif')
