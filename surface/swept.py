# coding: utf-8

import numpy as np
import os
import sys

sys.path.insert(0, os.path.join(sys.path[0], '..'))
from jhm.vector import Vector
from jhm.quaternion import Quaternion
import viewer.quaternion as qt
sys.path.pop(0)

import data

def de_casteljau_vector(v0, v1, v2, v3, t):
  # step 0
  v4 = v0 + (v1 - v0) * t
  v5 = v1 + (v2 - v1) * t
  v6 = v2 + (v3 - v2) * t
  # step 1
  v7 = v4 + (v5 - v4) * t
  v8 = v5 + (v6 - v5) * t
  # step 2
  v9 = v7 + (v8 - v7) * t
  return v9

def interpolate_vectors(n, vectors, steps):
  assert n > 1 and n == len(vectors)
  # tangents
  tangents = [vectors[1] - vectors[0]] # for [0]
  for i in xrange(1, n - 1):
    tangents.append(vectors[i + 1] - vectors[i - 1])
  tangents.append(vectors[n - 1] - vectors[n - 2]) # for [n - 1]
  tangents = map(lambda v: v / 2.0, tangents)
  # splines
  for i in xrange(1, n):
    v0 = vectors[i - 1]
    v1 = vectors[i - 1] + tangents[i - 1] / 3.0
    v2 = vectors[i] - tangents[i] / 3.0
    v3 = vectors[i]
    yield vectors[i - 1] # t == 0
    for step in xrange(1, steps):
      t = float(step) / steps
      yield de_casteljau_vector(v0, v1, v2, v3, t)
  yield vectors[n - 1] # last t == 1

def de_casteljau_quaternion(q0, q1, q2, q3, t):
  # step 0
  q4 = Quaternion.slerp(q0, q1, t)
  q5 = Quaternion.slerp(q1, q2, t)
  q6 = Quaternion.slerp(q2, q3, t)
  # step 1
  q7 = Quaternion.slerp(q4, q5, t)
  q8 = Quaternion.slerp(q5, q6, t)
  # step 2
  q9 = Quaternion.slerp(q7, q8, t)
  return q9

def interpolate_quaternions(n, quaternions, steps):
  assert n > 1 and n == len(quaternions)
  # tangents
  tangents = [~quaternions[0] * quaternions[1]] # for [0]
  for i in xrange(1, n - 1):
    tangents.append(~quaternions[i - 1] * quaternions[i + 1])
  tangents.append(~quaternions[n - 2] * quaternions[n - 1]) # for [n - 1]
  tangents = map(lambda q: Quaternion.ln(q).div(2.0), tangents)
  # splines
  for i in xrange(1, n):
    q0 = quaternions[i - 1]
    q1 = quaternions[i - 1] * Quaternion.exp(tangents[i - 1].div(3.0))
    q2 = quaternions[i] * Quaternion.exp(-tangents[i].div(3.0))
    q3 = quaternions[i]
    yield quaternions[i - 1] # t == 0
    for step in xrange(1, steps):
      t = float(step) / steps
      yield de_casteljau_quaternion(q0, q1, q2, q3, t)
  yield quaternions[n - 1] # last t == 1

def bspline_closed(m, cross, steps):
  assert m > 3 and m == len(cross)
  Ts = []
  for step in xrange(steps):
    t = float(step) / steps
    Ts.append(np.array([t * t * t, t * t, t, 1.0]))
  M = np.array([
    [-1.0,  3.0, -3.0,  1.0],
    [ 3.0, -6.0,  3.0,  0.0],
    [-3.0,  0.0,  3.0,  0.0],
    [ 1.0,  4.0,  1.0,  0.0]]) / 6.0
  for i in xrange(m):
    p0 = cross[i - 3]
    p1 = cross[i - 2]
    p2 = cross[i - 1]
    p3 = cross[i]
    G = np.array([p0, p1, p2, p3])
    for T in Ts:
      yield T.dot(M).dot(G)

def catmull_rom_closed(m, cross, steps):
  assert m > 3 and m == len(cross)
  for i in xrange(m):
    # between [i - 2] and [i - 1]
    a0 = (cross[i - 1] - cross[i - 3]) / 2.0
    a1 = (cross[i] - cross[i - 2]) / 2.0
    p0 = cross[i - 2]
    p1 = cross[i - 2] + a0 / 3.0
    p2 = cross[i - 1] - a1 / 3.0
    p3 = cross[i - 1]
    yield p0
    for step in xrange(1, steps):
      t = float(step) / steps
      yield de_casteljau_vector(p0, p1, p2, p3, t)

def natural_closed(m, cross, steps):
  assert m > 3 and m == len(cross)
  N = np.zeros((m, m))
  for i in xrange(m):
    N[i][i - 1] = 1.0
    N[i][i] = 4.0
    N[i][(i + 1) % m] = 1.0
  N /= 6.0
  return bspline_closed(m, np.linalg.inv(N).dot(cross), steps)

def spline_each_crosses(t, n, m, points, steps):
  assert t in data.CURVE_TYPE
  assert n > 0 and n == len(points)
  for i in xrange(n):
    cross = points[i]
    if t == 'BSPLINE':
      spline = bspline_closed(m, cross, steps)
    elif t == 'CATMULL_ROM':
      spline = catmull_rom_closed(m, cross, steps)
    else: # t == 'NATURAL'
      spline = natural_closed(m, cross, steps)
    yield np.array(list(spline))

def interpolate_crosses(n, crosses, steps):
  assert n > 1 and n == len(crosses)
  return np.swapaxes(np.array(
      [list(interpolate_vectors(n, points, steps))
       for points in np.swapaxes(crosses, 0, 1)]),
    0, 1)

def construct_mesh(model, points, scales, rotations, positions, enclosed):
  model.clear()
  n, m, _ = points.shape
  idx = lambda i, j: i * m + j % m
  # vertices
  for pp in points:
    scale = next(scales)
    rotation = next(rotations)
    position = next(positions)
    for p in pp:
      vertex = qt.rotate(rotation,
        [p[0] * scale, 0.0, p[1] * scale]
      ) + position
      model.vertices.append(list(vertex))
  # normals
  for i in xrange(n):
    for j in xrange(m):
      # 4 3
      # 5 C 2
      #   0 1
      center = np.array(model.vertices[idx(i, j)])
      indices = [idx(i    , j - 1),
                 idx(i + 1, j - 1),
                 idx(i + 1, j    ),
                 idx(i    , j + 1),
                 idx(i - 1, j + 1),
                 idx(i - 1, j    )]
      if i == 0:
        boundary = np.array([model.vertices[indices[0]],
                             model.vertices[indices[1]],
                             model.vertices[indices[2]],
                             model.vertices[indices[3]]])
      elif i == n - 1:
        boundary = np.array([model.vertices[indices[3]],
                             model.vertices[indices[4]],
                             model.vertices[indices[5]],
                             model.vertices[indices[0]]])
      else:
        vertices = [model.vertices[index] for index in indices]
        vertices.append(model.vertices[indices[0]])
        boundary = np.array(vertices)
      norm = np.zeros(np.shape(center))
      for k in xrange(len(boundary) - 1):
        norm_k = np.cross(boundary[k] - center, boundary[k + 1] - center)
        norm_k /= np.sqrt(norm_k.dot(norm_k))
        norm += norm_k
      norm /= len(boundary) - 1
      model.normals.append(list(norm))
  # faces
  for i in xrange(1, n):
    for j in xrange(m):
      # 1   3
      #   \
      # 0   2
      k0 = idx(i - 1, j - 1)
      k1 = idx(i - 1, j)
      k2 = idx(i, j - 1)
      k3 = idx(i, j)
      model.faces.append([[k0, None, k0],
                          [k2, None, k2],
                          [k1, None, k1]])
      model.faces.append([[k3, None, k3],
                          [k1, None, k1],
                          [k2, None, k2]])
  # caps
  if enclosed:
    for i in [0, n - 1]:
      o = i * m + 0
      for j in xrange(2, m):
        a = i * m + j
        b = i * m + j - 1
        if i == 0:
          c = a
          a = b
          b = c
        norm = np.cross(np.array(model.vertices[a]) - np.array(model.vertices[o]), np.array(model.vertices[b]) - np.array(model.vertices[o]))
        model.normals.append(list(norm))
        norm_i = len(model.normals) - 1
        model.faces.append([[o, None, norm_i],
                            [a, None, norm_i],
                            [b, None, norm_i]])

def generate_surface(model, data, steps, enclosed):
  # transformation factors
  scales = interpolate_vectors(data.n, data.scales, steps)
  rotations = interpolate_quaternions(data.n, map(lambda rotation: qt.from_rotation(rotation), data.rotations), steps)
  positions = interpolate_vectors(data.n, np.array(data.positions), steps)
  # cross sections
  crosses = spline_each_crosses(data.t, data.n, data.m, np.array(data.points), steps)
  points = interpolate_crosses(data.n, np.array(list(crosses)), steps)
  # mesh
  construct_mesh(model, points, scales, rotations, positions, enclosed)

