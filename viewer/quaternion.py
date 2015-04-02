# coding: utf-8

import numpy as np

class Quaternion:

  def __init__(self, w, x, y, z):
    mag = np.sqrt(w * w + x * x + y * y + z * z)
    self.w, self.x, self.y, self.z = w / mag, x / mag, y / mag, z / mag

  @classmethod
  def from_two_vectors(cls, v0, v1):
    w = np.sqrt(v0.dot(v0) * v1.dot(v1)) + v0.dot(v1)
    axis = np.cross(v0, v1)
    x, y, z = axis[0], axis[1], axis[2]
    return Quaternion(w, x, y, z)

  @classmethod
  def from_axis_and_angle(cls, axis, sin, cos):
    axis /= np.sqrt(axis.dot(axis))
    return Quaternion(cos, axis[0] * sin, axis[1] * sin, axis[2] * sin)

  def conjugate(self):
    return Quaternion(self.w, -self.x, -self.y, -self.z)

  def __mul__(self, other):
    w, x, y, z = self.w, self.x, self.y, self.z
    return Quaternion(
      w * other.w - x * other.x - y * other.y - z * other.z,
      w * other.x + x * other.w + y * other.z - z * other.y,
      w * other.y + y * other.w + z * other.x - x * other.z,
      w * other.z + z * other.w + x * other.y - y * other.x)

  def rotate(self, v):
    l = np.sqrt(v.dot(v))
    v /= l
    qv = Quaternion(0.0, v[0], v[1], v[2])
    q =  self * qv * self.conjugate()
    return l * np.array([q.x, q.y, q.z])

