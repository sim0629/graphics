# coding: utf-8

import numpy
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

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
    glutSolidSphere(1.0, 32, 32)
    for hair in self.hairs:
      hair.render()

# // Head

class Hair(Model):

  tilt = 5.0
  roll_axis_x = 0
  roll_axis_y = -numpy.sin(tilt / 180.0 * numpy.pi)
  roll_axis_z = numpy.cos(tilt / 180.0 * numpy.pi)

  def __init__(self, degree):
    self.degree = degree
    self.node = HairNode(HairNode(HairNode()))

  def _draw(self):
    glRotate(Hair.tilt, -1.0, 0.0, 0.0)
    glRotate(self.degree, Hair.roll_axis_x, Hair.roll_axis_y, Hair.roll_axis_z)
    glTranslate(0.0, 1.0, 0.0)
    self.node.render()

# // Hair

class HairNode(Model):

  def __init__(self, next_node=None):
    self.next_node = next_node

  def _draw(self):
    glTranslate(0.0, 0.1, 0.0)
    glutSolidSphere(0.2, 32, 32)
    glTranslate(0.0, 0.2, 0.0)
    if self.next_node:
      self.next_node.render()

# // HairNode
