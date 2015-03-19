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
    self.hairs = [
      Hair(0.0),
      Hair(60.0),
      Hair(120.0),
      Hair(-60.0),
      Hair(-120.0),
    ]

  def _draw(self):
    gluSphere(quadric, 1.0, 32, 32)
    for hair in self.hairs:
      hair.render()

# // Head

class Hair(Model):

  def __init__(self, degree):
    self.degree = degree
    self.node = HairNode()

  def _draw(self):
    glRotate(self.degree, 0.0, 0.0, 1.0)
    glTranslate(0.0, 1.0, 0.0)
    self.node.render()

# // Hair

class HairNode(Model):

  def __init__(self):
    pass

  def _draw(self):
    gluSphere(quadric, 0.2, 32, 32)

# // HairNode
