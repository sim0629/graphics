# coding: utf-8

import numpy as np

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

X, Y, Z = 0, 1, 2
IN, OUT = False, True

def is_pressed(flag):
  m = glutGetModifiers()
  return bool(m & flag)

def shift_pressed():
  return is_pressed(GLUT_ACTIVE_SHIFT)

def ctrl_pressed():
  return is_pressed(GLUT_ACTIVE_CTRL)

class Camera:

  def __init__(self):
    self.pos = np.array([0.0, 0.0, 3.0])
    self.ref = np.array([0.0, 0.0, 0.0])
    self.up = np.array([0.0, 1.0, 0.0])
    self.theta = 90.0
    self.aspect = 1.0
    self.near = 1.0
    self.far = 30.0

  def _look_at(self):
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(
      self.pos[X], self.pos[Y], self.pos[Z],
      self.ref[X], self.ref[Y], self.ref[Z],
      self.up[X], self.up[Y], self.up[Z]
    )

  def _perspective(self):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(
      self.theta, self.aspect,
      self.near, self.far
    )

  def init(self):
    self._look_at()
    self._perspective()

  def doly(self, out):
    speed = -0.1
    if out:
      speed = -speed
    v = self.pos - self.ref
    distance = np.sqrt(v.dot(v))
    if speed < 0 and distance + speed <= self.near \
      or speed > 0 and distance + speed >= self.far:
      return
    v *= speed / distance
    self.pos += v
    self._look_at()
    glutPostRedisplay()

  def zoom(self, out):
    speed = -1.0
    if out:
      speed = -speed
    if speed < 0 and self.theta + speed < 1.0 \
      or speed > 0 and self.theta + speed >= 180.0:
      return
    self.theta += speed
    self._perspective()
    glutPostRedisplay()

  def translate(self, target):
    speed = 1.5

    n = self.pos - self.ref
    n /= np.sqrt(n.dot(n))
    u = np.cross(self.up, n) / np.sqrt(self.up.dot(self.up))
    v = np.cross(n, u)

    displacement = target - self.source
    du = displacement[X] * u
    dv = displacement[Y] * v
    diff = speed * (du + dv)

    self.pos = self.prev_pos - diff
    self.ref = self.prev_ref - diff

    self._look_at()

    glutPostRedisplay()

  def rotate(self, target):
    # TODO
    glutPostRedisplay()

  def keyboard(self, ch, x, y):
    if ch == 'w':
      self.doly(IN)
    elif ch == 's':
      self.doly(OUT)
    elif ch == 'd':
      self.zoom(IN)
    elif ch == 'a':
      self.zoom(OUT)
    else:
      pass

  def mouse(self, button, state, x, y):
    if state == GLUT_DOWN:
      self.source = np.array([x, y])
      if ctrl_pressed():
        pass
      elif shift_pressed():
        self.method = 'translate'
        self.prev_pos = self.pos
        self.prev_ref = self.ref
      else:
        self.method = 'rotate'
    elif state == GLUT_UP:
      self.method = None
    else:
      pass

  def motion(self, x, y):
    target = np.array([x, y])
    if self.method == 'translate':
      self.translate(target)
    elif self.method == 'rotate':
      self.rotate(target)
    else:
      pass

