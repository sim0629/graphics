# coding: utf-8

import numpy as np

CURVE_TYPE = ['BSPLINE', 'CATMULL_ROM', 'NATURAL']

class Data:

  def __init__(self, filename):
    self.filename = filename
    with open(filename, 'r') as f:
      t = f.readline().strip().upper()
      if t not in CURVE_TYPE:
        raise Exception('Unknown curve type: %s' % t)
      self.t = t
      self.n = n = int(f.readline())
      self.m = m = int(f.readline())
      self.points = points = []
      self.scales = scales = []
      self.rotations = rotations = []
      self.positions = positions = []
      for i in xrange(n):
        cross = []
        for j in xrange(m):
          cross.append(map(float, f.readline().split()))
        points.append(cross)
        scales.append(float(f.readline()))
        rotations.append(map(float, f.readline().split()))
        positions.append(map(float, f.readline().split()))

  @staticmethod
  def sample(t, n, m):
    if t not in CURVE_TYPE:
      raise Exception('Unknown curve type: %s' % t)
    print t
    print '%d' % n
    print '%d' % m

    for i in xrange(n):
      for j in xrange(m):
        theta = 2.0 * np.pi * j / m
        x = np.cos(theta)
        y = np.sin(theta)
        print '%f %f' % (x, y)
      print '%f' % 1.0
      print '%f %f %f %f' % (0.0, 1.0, 0.0, 0.0)
      print '%f %f %f' % (0.0, 2.0 * i / n - 1.0, 0.0)

