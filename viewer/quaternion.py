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
  c = v0.dot(v1)
  a = v0 * v1
  s = a.length()
  q = Quaternion(c, s * a.x, s * a.y, s * a.z)
  return Quaternion.exp(Quaternion.ln(q).div(2.0))

def from_axis_and_angle(a, s, c):
  a = Vector.from_list(a).normalize()
  return Quaternion(c, s * a.x, s * a.y, s * a.z)

def rotate(q, v):
  return np.array(Quaternion.rotate(q, Vector.from_list(v)).to_list())

