# coding: utf-8

import math

from constants import *
from vector import Vector

class Quaternion:

  def __init__(self, w, x, y, z):
    self.w, self.x, self.y, self.z = w, x, y, z

  def __str__(self):
    w, x, y, z = self.w, self.x, self.y, self.z
    return "Quaternion (%f, %f, %f, %f)" % (w, x, y, z)

  def __neg__(self):
    return Quaternion(-self.w,
                      -self.x,
                      -self.y,
                      -self.z)

  def __pos__(self):
    return Quaternion(self.w,
                      self.x,
                      self.y,
                      self.z)

  def __invert__(self):
    return Quaternion(self.w,
                      -self.x,
                      -self.y,
                      -self.z)

  def __add__(self, other):
    return Quaternion(self.w + other.w,
                      self.x + other.x,
                      self.y + other.y,
                      self.z + other.z)

  def __sub__(self, other):
    return Quaternion(self.w - other.w,
                      self.x - other.x,
                      self.y - other.y,
                      self.z - other.z)

  def __mul__(self, other):
    w, x, y, z = self.w, self.x, self.y, self.z
    s, a, b, c = other.w, other.x, other.y, other.z
    return Quaternion(w * s - x * a - y * b - z * c,
                      w * a + x * s + y * c - z * b,
                      w * b + y * s + z * a - x * c,
                      w * c + z * s + x * b - y * a)

  def real(self):
    return self.w

  def imaginaries(self):
    return [self.x, self.y, self.z]

  def normalize(self):
    return self.div(self.length())

  def length(self):
    return math.sqrt(self.dot(self))

  def mul(self, r):
    return Quaternion(self.w * r,
                      self.x * r,
                      self.y * r,
                      self.z * r)

  def div(self, r):
    return Quaternion(self.w / r,
                      self.x / r,
                      self.y / r,
                      self.z / r)

  def dot(self, other):
    return (self.w * other.w +
            self.x * other.x +
            self.y * other.y +
            self.z * other.z)

  @staticmethod
  def exp(v):
    theta = v.length()
    if theta < EPS:
      sc = 1.0
    else:
      sc = math.sin(theta) / theta
    v = v.mul(sc)
    return Quaternion(math.cos(theta), v.x, v.y, v.z)

  @staticmethod
  def pow(v, r):
    return Quaternion.exp(v.mul(r))

  @staticmethod
  def ln(q):
    v = Vector(q.x, q.y, q.z)
    sc = v.length()
    theta = math.atan2(sc, q.w)
    if sc < EPS:
      sc = 1.0
    else:
      sc = theta / sc
    return v.mul(sc)

  @staticmethod
  def rotate(q, v):
    c = q * Quaternion(0.0, v.x, v.y, v.z) * (~q)
    return Vector(c.x, c.y, c.z)

  @staticmethod
  def slerp(a, b, t):
    c = a.dot(b)
    if 1.0 + c > EPS:
      if 1.0 - c > EPS:
        theta = math.acos(c)
        sinom = math.sin(theta)
        return (a.mul(math.sin((1 - t) * theta)) +
                b.mul(math.sin(t * theta))) / sinom
      else:
        return (a.mul(1 - t) + b.mul(t)).normalize()
    else:
      return (a.mul(math.sin((0.5 - t) * math.pi)) +
              b.mul(math.sin(t * math.pi)))

  @staticmethod
  def interpolate(t, a, b):
    return Quaternion.slerp(a, b, t)

  @staticmethod
  def distance(a, b):
    return min(Quaternion.ln(~a * b).length(),
               Quaternion.ln(~a * -b).length())

  @staticmethod
  def difference(a, b):
    return Quaternion.ln(~b * a)

