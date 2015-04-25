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
  t = np.arctan2(c, s)
  return Quaternion.pow(a, t)

def from_axis_and_angle(a, c, s):
  a = Vector.from_list(a).normalize()
  t = np.arctan2(c, s)
  return Quaternion.pow(a, t)

def rotate(q, v):
  return np.array(Quaternion.rotate(q, Vector.from_list(v)).to_list())

