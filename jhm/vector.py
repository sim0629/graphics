# coding: utf-8

import math

class Vector:

  def __init__(self, x, y, z):
    self.x, self.y, self.z = x, y, z

  def __str__(self):
    x, y, z = self.x, self.y, self.z
    return "Vector (%f, %f, %f)" % (x, y, z)

  def __neg__(self):
    return Vector(-self.x,
                  -self.y,
                  -self.z)

  def __pos__(self):
    return Vector(self.x,
                  self.y,
                  self.z)

  def __add__(self, other):
    return Vector(self.x + other.x,
                  self.y + other.y,
                  self.z + other.z)

  def __sub__(self, other):
    return Vector(self.x - other.x,
                  self.y - other.y,
                  self.z - other.z)

  def normalize(self):
    return self.div(self.length())

  def length(self):
    return math.sqrt(self.dot(self))

  def mul(self, r):
    return Vector(self.x * r,
                  self.y * r,
                  self.z * r)

  def div(self, r):
    return Vector(self.x / r,
                  self.y / r,
                  self.z / r)

  def dot(self, other):
    return (self.x * self.x +
            self.y * self.y +
            self.z * self.z)

