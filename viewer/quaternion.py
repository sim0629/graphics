# coding: utf-8

import numpy as np
import os
import sys

sys.path.insert(0, os.path.join(sys.path[0], '..'))
from jhm.quaternion import Quaternion
from jhm.vector import Vector
sys.path.pop()

def from_two_vectors(v0, v1):
  v0 = Vector.from_list(v0).normalize()
  v1 = Vector.from_list(v1).normalize()
  a = v0 * v1
  c = v0.dot(v1)
  s = a.length()
  t = np.arctan2(s, c)
  return Quaternion.pow(a, t / 2.0)

def from_axis_and_angle(a, s, c):
  a = Vector.from_list(a).normalize()
  t = np.arctan2(s, c)
  return Quaternion.pow(a, t / 2.0)

def rotate(q, v):
  return np.array(Quaternion.rotate(q, Vector.from_list(v)).to_list())

def to_rotation(q):
  v = Quaternion.ln(q)
  return [v.length() * 2.0] + v.normalize().to_list()

def from_rotation(rot):
  return Quaternion.pow(Vector.from_list(rot[1:]), rot[0] / 2.0)

