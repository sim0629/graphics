# coding: utf-8

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

quadric = gluNewQuadric()

class Model:

  def _draw(self):
    pass

  def render(self):
    glPushMatrix()
    self._draw()
    glPopMatrix()

# // Model

class Oryzae(Model):

  def __init__(self, pos, scale):
    self.pos_x, self.pos_y, self.pos_z = pos
    self.scale_x, self.scale_y, self.scale_z = scale
    self.head = Head()

  def _draw(self):
    glTranslate(self.pos_x, self.pos_y, self.pos_z)
    glScale(self.scale_x, self.scale_y, self.scale_z)
    self.head.render()

# // Oryzae

class Head(Model):

  def __init__(self):
    pass

  def _draw(self):
    gluSphere(quadric, 1.0, 32, 32)

# // Head
