# coding: utf-8

import numpy as np

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import swept
import title

data = None
idx = 0
steps = 10

class Drag:
  def __init__(self):
    self.ing = False
  def begin(self, point):
    self.ing = True
    self.source = point
  def move(self, point):
    self.target = point
  def end(self):
    self.ing = False
drag = Drag()

def keyboard(ch, x, y):
  global idx, steps
  if ch == ']':
    idx = (idx + 1) % data.n
    refresh_title()
    drag.end()
  elif ch == '[':
    idx = (idx - 1) % data.n
    refresh_title()
    drag.end()
  elif ch == '+':
    steps = steps + 1
  elif ch == '-':
    if steps > 1:
      steps = steps - 1

def mouse(button, state, x, y):
  if state == GLUT_DOWN:
    drag.begin(np.array([x, y]))
    pick_point()
  elif state == GLUT_UP:
    drag.end()

def motion(x, y):
  if not drag.ing:
    return
  drag.move(np.array([x, y]))
  move_point()

def display():
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
  glMatrixMode(GL_MODELVIEW)

  ring = data.points[idx]
  glBegin(GL_POINTS)
  for p in ring:
    glVertex(p[0], 0.0, p[1])
  glEnd()

  n = len(ring)
  if data.t == 'BSPLINE':
    spline = swept.bspline_closed(n, np.array(ring), steps)
  elif data.t == 'CATMULL_ROM':
    spline = swept.catmull_rom_closed(n, np.array(ring), steps)
  else: # data.t == 'NATURAL'
    spline = swept.natural_closed(n, np.array(ring), steps)
  glBegin(GL_LINE_LOOP)
  for p in spline:
    glVertex(p[0], 0.0, p[1])
  glEnd()

def pick_point():
  ring = data.points[idx]
  for i in xrange(len(ring)):
    v = np.array(ring[i]) - drag.source
    d = np.sqrt(v.dot(v))
    if d < 0.05:
      drag.picked_i = i
      drag.picked_p = ring[i]
      return
  drag.picked_i = None

def move_point():
  if drag.picked_i is None:
    return
  x = drag.target - drag.source
  ring = data.points[idx]
  ring[drag.picked_i] = list(np.array(drag.picked_p) + x)

def refresh_title():
  title.change('Cross Section #%d' % idx)

def start():
  glDisable(GL_LIGHTING)
  glClearColor(0.0, 0.0, 0.0, 0.0)
  glColor(1.0, 1.0, 1.0)

  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity()
  gluLookAt(0.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0)

  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  gluOrtho2D(-1.0, 1.0, -1.0, 1.0)

  refresh_title()
  drag.end()

