# coding: utf-8

import os
import sys

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

sys.path.insert(0, os.path.join(sys.path[0], '..'))
from viewer.wavefront import Mesh
sys.path.pop(0)

def apply_property(name):
  if name == 'ruby':
    ambient = (0.1745, 0.01175, 0.01175, 0.8)
    diffuse = (0.61424, 0.04136, 0.04136, 0.8)
    specular = (0.727811, 0.626959, 0.626959, 1.0)
    shininess = 0.6
  elif name == 'gold':
    ambient = (0.24725, 0.1995, 0.0745, 1.0)
    diffuse = (0.75164, 0.60648, 0.22648, 1.0)
    specular = (0.628281, 0.555802, 0.366065, 1.0)
    shininess = 0.4
  else:
    ambient = (0.1, 0.1, 0.1, 1.0)
    diffuse = (0.9, 0.9, 0.9, 1.0)
    specular = (0.0, 0.0, 0.0, 1.0)
    shininess = 0.0
  glMaterial(GL_FRONT_AND_BACK, GL_AMBIENT, ambient)
  glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, diffuse)
  glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, specular)
  glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, shininess * 128.0)

def load_object(name):
  mesh = Mesh.load_from_file(os.path.join(sys.path[0], name + '.obj'))

  mat = {}
  mat_file = open(os.path.join(sys.path[0], name + '.mat'), 'r')
  for line in mat_file:
    i, m = line.split()
    mat[int(i)] = m
  mat_file.close()

  mesh.materials = []
  material = None
  for fi in xrange(len(mesh.faces)):
    if fi in mat:
      material = mat[fi]
    mesh.materials.append(material)

  return mesh
