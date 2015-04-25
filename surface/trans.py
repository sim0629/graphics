# coding: utf-8

import numpy as np

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import title

camera = None
data = None

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

def mouse(button, state, x, y):
  if state == GLUT_DOWN:
    drag.begin(np.array([x, y]))
    if pick_point():
      return
  elif state == GLUT_UP:
    drag.end()
  camera.mouse(button, state, x, y)

def motion(x, y):
  if not drag.ing:
    return
  drag.move(np.array([x, y]))
  if move_point():
    return
  camera.motion(x, y)

def display():
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
  glMatrixMode(GL_MODELVIEW)

  for i in xrange(data.n):
    glPushMatrix()
    glScale(data.scales[i],
            1.0,
            data.scales[i])
    glRotate(data.rotations[i][0] * 180.0 / np.pi,
             data.rotations[i][1],
             data.rotations[i][2],
             data.rotations[i][3])
    glTranslate(data.positions[i][0],
                data.positions[i][1],
                data.positions[i][2])
    glColor(1.0, 1.0, 1.0)
    glBegin(GL_POLYGON)
    for p in data.points[i]:
      glVertex(p[0], 0.0, p[1])
    glEnd()
    glColor(0.5, 0.5, 1.0)
    glBegin(GL_POINTS)
    glVertex(0.0, 0.0, 0.0)
    glEnd()
    glPopMatrix()

def pick_point():
  return True

def move_point():
  return True

def refresh_title():
  title.change('Transforming')

def start():
  glDisable(GL_LIGHTING)
  glClearColor(0.0, 0.0, 0.0, 0.0)
  glPolygonMode(GL_FRONT, GL_FILL)
  glPolygonMode(GL_BACK, GL_LINE)

  camera.see()

