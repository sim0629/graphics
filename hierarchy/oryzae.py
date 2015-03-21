# coding: utf-8

import numpy
import numpy.random
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

X, Y, Z = 0, 1, 2

class Animation:

  def __init__(self, speed):
    self.ratio = 0.0
    self._increment = speed

  def update(self):
    self.ratio += self._increment
    if self.ratio >= 1.0 or self.ratio <= 0.0:
      self._increment = -self._increment

# // Animation

class Model:

  def _draw(self):
    pass

  def render(self):
    glPushMatrix()
    self._draw()
    glPopMatrix()

  def update(self):
    pass

# // Model

class Oryzae(Model):

  def __init__(self, pos, scale):
    self.pos_x, self.pos_y, self.pos_z = pos
    self.scale_x, self.scale_y, self.scale_z = scale
    self.degree_pan = 0.0
    self.degree_tilt = 0.0
    self.head = Head()
    self.body = Body()

  def _draw(self):
    glTranslate(self.pos_x, self.pos_y, self.pos_z)
    glScale(self.scale_x, self.scale_y, self.scale_z)
    glRotate(self.degree_pan, 0.0, 1.0, 0.0)
    glRotate(self.degree_tilt, 1.0, 0.0, 0.0)
    self.head.render()
    self.body.render()

  def update(self):
    self.head.update()
    self.body.update()

  def pan(self, degree):
    self.degree_pan += degree

  def tilt(self, degree):
    self.degree_tilt += degree

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
    self.eyes = [
      Eye(60.0),
      Eye(-60.0),
    ]
    self.mouth = Mouth()
    self.roll = 0.0
    self.animation = Animation(0.01)
    self.animation.ratio = 0.5

  def _draw(self):
    glColor(1.0, 1.0, 0.6)
    glRotate(self.roll, 0.0, 0.0, 1.0)
    glutSolidSphere(1.0, 32, 32)
    for hair in self.hairs:
      hair.render()
    for eye in self.eyes:
      eye.render()
    self.mouth.render()

  def update(self):
    self.roll = (self.animation.ratio - 0.5) * 20.0
    self.animation.update()
    for hair in self.hairs:
      hair.update()
    for eye in self.eyes:
      eye.update()
    self.mouth.update()

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

  def update(self):
    self.node.update()

# // Hair

class HairNode(Model):

  def __init__(self, next_node=None):
    self.next_node = next_node
    self.tilt = 0.0
    self.animation = Animation(0.02 - numpy.random.random() * 0.01)

  def _draw(self):
    glTranslate(0.0, 0.1, 0.0)
    glutSolidSphere(0.2, 32, 32)
    glRotate(self.tilt, -1.0, 0.0, 0.0)
    glTranslate(0.0, 0.2, 0.0)
    if self.next_node:
      self.next_node.render()

  def update(self):
    self.tilt = self.animation.ratio * 30.0
    self.animation.update()
    if self.next_node:
      self.next_node.update()

# // HairNode

class Eye(Model):

  tilt = 60.0
  roll_axis_x = 0
  roll_axis_y = numpy.sin(tilt / 180.0 * numpy.pi)
  roll_axis_z = numpy.cos(tilt / 180.0 * numpy.pi)

  def __init__(self, degree):
    self.degree = degree

  def _draw(self):
    glColor(0.0, 0.0, 0.0)
    glRotate(Eye.tilt, 1.0, 0.0, 0.0)
    glRotate(self.degree, Eye.roll_axis_x, Eye.roll_axis_y, Eye.roll_axis_z)
    glTranslate(0.0, 1.0, 0.0)
    glutSolidSphere(0.04, 8, 8)

# // Eye

class Mouth(Model):

  def __init__(self):
    self.width = 1.0
    self.height = 0.5
    self.thickness = 0.3

  def _draw(self):
    glColor(1.0, 1.0, 1.0)
    glRotate(15.0, 1.0, 0.0, 0.0)
    glTranslate(0.0, 0.0, 1.0 - self.thickness * 0.5 + 0.01) # don't delete 0.01
    glRotate(-90.0, 1.0, 0.0, 0.0)
    glScale(self.width, self.thickness, self.height)
    glTranslate(0.0, 0.0, -0.5)
    quad = gluNewQuadric()
    gluCylinder(quad, 0.5, 0.5, 1.0, 16, 16)
    gluDeleteQuadric(quad)

# // Mouth

class Body(Model):

  def __init__(self):
    self.bottom_list = [
      [-0.3, -0.6, 0.3],
      [0.3, -0.6, 0.3],
      [0.3, -0.6, -0.3],
      [-0.3, -0.6, -0.3],
    ]
    self.top_list = [
      [-0.25, 0.2, 0.25],
      [0.25, 0.2, 0.25],
      [0.25, 0.2, -0.25],
      [-0.25, 0.2, -0.25],
    ]
    self.animation = Animation(0.02)

  def _normal(self, n):
    return numpy.cross(
      numpy.array(self.bottom_list[(n + 1) % 4])
      - numpy.array(self.bottom_list[n]),
      numpy.array(self.top_list[n])
      - numpy.array(self.bottom_list[n])
    )

  def _draw(self):
    glColor(1.0, 1.0, 0.6)
    glTranslate(0.0, -1.0, 0.0)
    glBegin(GL_QUADS)
    for i in xrange(4):
      normal_vector = self._normal(i)
      glNormal(normal_vector[0], normal_vector[1], normal_vector[2])
      glVertex(self.top_list[i][X], self.top_list[i][Y], self.top_list[i][Z])
      glVertex(self.bottom_list[i][X], self.bottom_list[i][Y], self.bottom_list[i][Z])
      j = (i + 1) % 4
      glVertex(self.bottom_list[j][X], self.bottom_list[j][Y], self.bottom_list[j][Z])
      glVertex(self.top_list[j][X], self.top_list[j][Y], self.top_list[j][Z])
    glEnd()

  def update(self):
    v = 0.3 + self.animation.ratio * 0.05
    self.animation.update()
    self.bottom_list[0][X], self.bottom_list[0][Z] = -v, v
    self.bottom_list[1][X], self.bottom_list[1][Z] = v, v
    self.bottom_list[2][X], self.bottom_list[2][Z] = v, -v
    self.bottom_list[3][X], self.bottom_list[3][Z] = -v, -v

# // Body
