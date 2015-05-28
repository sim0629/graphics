# coding: utf-8

import numpy as np

p = []
for i in xrange(10):
  theta = np.pi / 2 + 2 * np.pi * i / 10
  radius = 1.0 if i % 2 == 0 else 0.5
  x, y = radius * np.cos(theta), radius * np.sin(theta)
  p.append((x, y))

print 'solid star'

for z in [-0.5, 0.5]:
  for i in xrange(10):
    a = np.array([p[i - 1][0], p[i - 1][1], 0.0])
    b = np.array([p[i][0], p[i][1], 0.0])
    c = np.array([0.0, 0.0, z])
    n = np.cross(a - c, b - c)
    n /= np.sqrt(n.dot(n))

    print 'facet normal %f %f %f' % tuple(n)
    print '\touter loop'
    print '\t\tvertex %f %f %f' % tuple(c)
    if z > 0:
      print '\t\tvertex %f %f %f' % tuple(a)
      print '\t\tvertex %f %f %f' % tuple(b)
    else:
      print '\t\tvertex %f %f %f' % tuple(b)
      print '\t\tvertex %f %f %f' % tuple(a)
    print '\tendloop'
    print 'endfacet'

print 'endsolid star'
