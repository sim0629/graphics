# coding: utf-8

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

X, Y, Z = 0, 1, 2

class Camera:

  def __init__(self):
    self.pos = [0.0, 0.0, 3.0]
    self.ref = [0.0, 0.0, 0.0]
    self.up = [0.0, 1.0, 0.0]
    self.theta = 90.0
    self.aspect = 1.0
    self.near = 1.0
    self.far = 30.0

  def _look_at(self):
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(
      self.pos[X], self.pos[Y], self.pos[Z],
      self.ref[X], self.ref[Y], self.ref[Z],
      self.up[X], self.up[Y], self.up[Z]
    )

  def _perspective(self):
    glMatrixMode(GL_PROJECTION)
    gluPerspective(
      self.theta, self.aspect,
      self.near, self.far
    )

  def init(self):
    self._look_at()
    self._perspective()

