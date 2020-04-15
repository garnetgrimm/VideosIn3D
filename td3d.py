"""
Demonstrates the different vertex formats supported.
Pyglet don't support all formats pywavefront can produce.
Supported by pyglet:
    V3F
    C3F_V3F
    N3F_V3F
    T2F_V3F
    T2F_C3F_V3F
    T2F_N3F_V3F
Additional formats:
    C3F_N3F_V3F
    T2F_C3F_N3F_V3F
"""
import ctypes
import os

from pyglet.gl import *
from pywavefront import visualization, Wavefront

window = pyglet.window.Window(width=1280, height=720, resizable=True)
pyglet.gl.glClearColor(0.5,0,0,1)
root_path = os.path.dirname(__file__)

ANIM_FOLDER = "anim"

filelist = os.listdir(ANIM_FOLDER)
for fichier in filelist[:]: # filelist[:] makes a copy of filelist.
    if not(fichier.endswith(".png")):
        filelist.remove(fichier)

boxes = []
for filename in filelist:
    lines = ""
    with open('testtex.mtl', 'r') as file:
        for line in file:
            if(line.split(" ")[0] == "map_Kd"):
                line = "map_Kd " + ANIM_FOLDER + "/" + filename + "\n"
            lines += line
    with open('testtex.mtl', 'w') as file:
        file.write(lines)

    boxes.append(Wavefront(os.path.join(root_path, 'testtex.obj')))

rotation = 0.0
lightfv = ctypes.c_float * 4


@window.event
def on_resize(width, height):
    viewport_width, viewport_height = window.get_framebuffer_size()
    glViewport(0, 0, viewport_width, viewport_height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45., float(width)/height, 1., 100.)
    glMatrixMode(GL_MODELVIEW)
    return True


@window.event
def on_draw():
    window.clear()
    glLoadIdentity()

    glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-1.0, 1.0, 1.0, 0.0))

    for i in range(0, len(boxes)):
        draw_box(boxes[i], -0.1*(len(boxes)//2), 0, -10, i*0.1, 0.0, 0.0)


def draw_box(box, cx, cy, cz, x, y, z):
    glLoadIdentity()
    glTranslated(cx, cy, -10)
    glRotatef(rotation, 0.0, 1.0, 0.0)
    glTranslated(x, y, 00)
    #glTranslated(x, y, 1.0)
    #glRotatef(-25.0, 1.0, 0.0, 0.0)
    #glRotatef(45.0, 0.0, 0.0, 1.0)

    visualization.draw(box)


def update(dt):
    global rotation
    rotation += 90.0 * dt

    if rotation > 360.0:
        rotation = 0.0


pyglet.clock.schedule(update)
pyglet.app.run()
