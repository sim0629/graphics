# coding: utf-8

import numpy as np

BSPLINE, CATMULL_ROM, NATURAL = range(3)

class Data:

  def __init__(self, filename):
    pass

  @staticmethod
  def sample(t, n, m):
    if t == BSPLINE:
      print 'BSPLINE'
    elif t == CATMULL_ROM:
      print 'CATMULL_ROM'
    elif t == NATURAL:
      print 'NATURAL'
    else:
      raise Exception('Unknown curve type')

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

