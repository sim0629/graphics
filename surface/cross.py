# coding: utf-8

import numpy as np

from OpenGL.GLU import *
from OpenGL.GL import *

import swept

data = None
idx = 0
steps = 10

def keyboard(ch, x, y):
  global idx, steps
  if ch == ']':
    idx = (idx + 1) % data.n
  elif ch == '[':
    idx = (idx - 1) % data.n
  elif ch == '+':
    steps = steps + 1
  elif ch == '-':
    if steps > 1:
      steps = steps - 1

def mouse(button, state, x, y):
  pass

def motion(x, y):
  pass

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

def start():
  glDisable(GL_LIGHTING)
  glClearColor(0.0, 0.0, 0.0, 0.0)
  glColor(1.0, 1.0, 1.0)

  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity()
  gluLookAt( 0.0,  0.0,  0.0,
             0.0, -1.0,  0.0,
             0.0,  0.0,  1.0 )

  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  gluOrtho2D(-1.0, 1.0, -1.0, 1.0)

