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

def pick_point():
  return True

def move_point():
  return True

def refresh_title():
  title.change('Transforming')

def start():
  glDisable(GL_LIGHTING)
  glClearColor(0.0, 0.0, 0.0, 0.0)

  camera.see()

