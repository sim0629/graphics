# coding: utf-8 

from OpenGL.GL import *

class Mesh:

  def __init__(self):
    self.vertices = []
    self.textures = []
    self.normals = []
    self.faces = []

  def load(self, filename):
    file = open(filename, 'r')

    for l in file:
      a = l.split()
      if len(a) == 0:
        continue
      if a[0] == 'v':
        v = map(float, a[1:])
        self.vertices.append(v)
      elif a[0] == 'vt':
        vt = map(float, a[1:])
        self.textures.append(vt)
      elif a[0] == 'vn':
        vn = map(float, a[1:])
        self.normals.append(vn)
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
        self.faces.append(f)

    file.close()

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

