# coding: utf-8 

import numpy as np

from OpenGL.GL import *

class Mesh:

  def __init__(self):
    self.clear()

  def clear(self):
    self.vertices = []
    self.textures = []
    self.normals = []
    self.faces = []

  def render(self):
    glBegin(GL_TRIANGLES)

    for face in self.faces:
      for point in face:
        vni = point[2]
        if vni is not None:
          vn = self.normals[vni]
          glNormal(vn[0], vn[1], vn[2])
        vi = point[0]
        v = self.vertices[vi]
        glVertex(v[0], v[1], v[2])

    glEnd()

  def bounding_box(self):
    min_x, max_x = np.inf, -np.inf
    min_y, max_y = np.inf, -np.inf
    min_z, max_z = np.inf, -np.inf

    if len(self.vertices) == 0:
      return None

    for vertex in self.vertices:
      x, y, z = vertex[0], vertex[1], vertex[2]
      if x < min_x:
        min_x = x
      if x > max_x:
        max_x = x
      if y < min_y:
        min_y = y
      if y > max_y:
        max_y = y
      if z < min_z:
        min_z = z
      if z > max_z:
        max_z = z

    return np.array([
      [min_x, min_y, min_z],
      [max_x, max_y, max_z],
    ])

  @classmethod
  def load_from_file(cls, filename):
    mesh = cls()
    file = open(filename, 'r')

    for l in file:
      a = l.split()
      if len(a) == 0:
        continue
      if a[0] == 'v':
        v = map(float, a[1:])
        mesh.vertices.append(v)
      elif a[0] == 'vt':
        vt = map(float, a[1:])
        mesh.textures.append(vt)
      elif a[0] == 'vn':
        vn = map(float, a[1:])
        mesh.normals.append(vn)
      elif a[0] == 'f':
        f = []
        if len(a) < 4:
          continue
        for ai in a[1:]:
          fi = [None, None, None]
          b = ai.split('/')
          for j in xrange(len(b)):
            bj = b[j]
            if len(bj) == 0:
              continue
            fi[j] = int(b[j]) - 1
          f.append(fi)
        mesh.faces.append(f)

    file.close()
    return mesh

