# coding: utf-8

import numpy as np
import random

import material

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

V, VT, VN = range(3)
EPS = 1e-4

def lin_interp(t, a, b):
  return (1.0 - t) * a + t * b

def sign(x):
  if abs(x) < EPS:
    return 0
  return np.sign(x)

class BspTree:

  def __init__(self, mesh, faces):
    mid = random.choice(faces)
    left = []
    right = []
    v = [None, None, None]
    n = [None, None, None]
    s = [None, None, None]

    face = mesh.faces[mid]
    for i in xrange(3):
      v[i] = np.array(mesh.vertices[face[i][V]])

    plane_v = v[0]
    plane_n = np.cross(v[1] - v[0], v[2] - v[0])
    plane_n /= np.sqrt(plane_n.dot(plane_n))

    for fi in faces:
      if fi == mid:
        continue

      face = mesh.faces[fi]
      for i in xrange(3):
        v[i] = np.array(mesh.vertices[face[i][V]])
        n[i] = np.array(mesh.normals[face[i][VN]])
        s[i] = sign(plane_n.dot(v[i] - plane_v))

      if s[0] == s[1] == s[2]:
        if s[0] < 0:
          left.append(fi)
        else:
          right.append(fi)
        continue

      success = True
      for i in xrange(3):
        i0 = i
        i1 = (i + 1) % 3
        i2 = (i + 2) % 3
        if s[i0] == 0:
          if s[i1] == s[i2]:
            if s[i1] < 0:
              left.append(fi)
            else:
              right.append(fi)
          elif s[i1] == 0:
            if s[i2] < 0:
              left.append(fi)
            else:
              right.append(fi)
          elif s[i2] == 0:
            if s[i1] < 0:
              left.append(fi)
            else:
              right.append(fi)
          else:
            t = plane_n.dot(plane_v - v[i1]) / plane_n.dot(v[i2] - v[i1])
            new_v = lin_interp(t, v[i1], v[i2])
            new_n = lin_interp(t, n[i1], n[i2])
            new_vi = len(mesh.vertices)
            new_ni = len(mesh.normals)
            mesh.vertices.append(list(new_v))
            mesh.normals.append(list(new_n))
            mesh.faces[fi] = [face[i0], face[i1], [new_vi, None, new_ni]]
            new_fi = len(mesh.faces)
            mesh.faces.append([face[i0], [new_vi, None, new_ni], face[i2]])
            mesh.materials.append(mesh.materials[fi])
            if s[i1] < 0:
              left.append(fi)
              right.append(new_fi)
            else:
              right.append(fi)
              left.append(new_fi)
          break
      else:
        success = False
      if success:
        continue

      for i in xrange(3):
        i0 = i
        i1 = (i + 1) % 3
        i2 = (i + 2) % 3
        if s[i1] == s[i2]:
          t1 = plane_n.dot(plane_v - v[i0]) / plane_n.dot(v[i1] - v[i0])
          new_v1 = lin_interp(t1, v[i0], v[i1])
          new_n1 = lin_interp(t1, n[i0], n[i1])
          new_vi1 = len(mesh.vertices)
          new_ni1 = len(mesh.normals)
          mesh.vertices.append(list(new_v1))
          mesh.normals.append(list(new_n1))
          new_fi1 = len(mesh.faces)
          mesh.faces.append([[new_vi1, None, new_ni1], face[i1], face[i2]])
          mesh.materials.append(mesh.materials[fi])
          t2 = plane_n.dot(plane_v - v[i0]) / plane_n.dot(v[i2] - v[i0])
          new_v2 = lin_interp(t2, v[i0], v[i2])
          new_n2 = lin_interp(t2, n[i0], n[i2])
          new_vi2 = len(mesh.vertices)
          new_ni2 = len(mesh.normals)
          mesh.vertices.append(list(new_v2))
          mesh.normals.append(list(new_n2))
          new_fi2 = len(mesh.faces)
          mesh.faces.append([[new_vi1, None, new_ni1], face[i2], [new_vi2, None, new_ni2]])
          mesh.materials.append(mesh.materials[fi])
          mesh.faces[fi] = [face[i0], [new_vi1, None, new_ni1], [new_vi2, None, new_ni2]]
          if s[i0] < 0:
            left.append(fi)
            right.append(new_fi1)
            right.append(new_fi2)
          else:
            right.append(fi)
            left.append(new_fi1)
            left.append(new_fi2)
          break
      else:
        assert False # impossible

    self.mesh = mesh
    self.mid = mid
    self.left = None if len(left) == 0 else BspTree(mesh, left)
    self.right = None if len(right) == 0 else BspTree(mesh, right)

  def render(self, eye):
    v = [None, None, None]

    face = self.mesh.faces[self.mid]
    v[0] = np.array(self.mesh.vertices[face[0][V]])
    v[1] = np.array(self.mesh.vertices[face[1][V]])
    v[2] = np.array(self.mesh.vertices[face[2][V]])

    plane_v = v[0]
    plane_n = np.cross(v[1] - v[0], v[2] - v[0])
    plane_n /= np.sqrt(plane_n.dot(plane_n))

    s = plane_n.dot(eye - plane_v)

    if s < 0:
      if self.right is not None:
        self.right.render(eye)
    else:
      if self.left is not None:
        self.left.render(eye)

    material.apply_property(self.mesh.materials[self.mid])
    for point in face:
      norm = self.mesh.normals[point[2]]
      glNormal(norm[0], norm[1], norm[2])
      vert = self.mesh.vertices[point[0]]
      glVertex(vert[0], vert[1], vert[2])

    if s < 0:
      if self.left is not None:
        self.left.render(eye)
    else:
      if self.right is not None:
        self.right.render(eye)

  @classmethod
  def tree(cls, mesh):
    if len(mesh.faces) == 0:
      return None
    print 'Please wait for constructing BSP tree...'
    t = cls(mesh, range(len(mesh.faces)))
    return t

