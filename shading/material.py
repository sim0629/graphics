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
  elif name == 'silver':
    ambient = (0.19225, 0.19225, 0.19225, 1.0)
    diffuse = (0.50754, 0.50754, 0.50754, 1.0)
    specular = (0.508273, 0.508273, 0.508273, 1.0)
    shininess = 0.4
  elif name == 'bronze':
    ambient = (0.2125, 0.1275, 0.054, 1.0)
    diffuse = (0.714, 0.4284, 0.18144, 1.0)
    specular = (0.393548, 0.271906, 0.166721, 1.0)
    shininess = 0.2
  elif name == 'pearl':
    ambient = (0.25, 0.20725, 0.20725, 1.0)
    diffuse = (1.0, 0.829, 0.829, 1.0)
    specular = (0.296648, 0.296648, 0.296648, 1.0)
    shininess = 0.088
  elif name == 'emerald':
    ambient = (0.0215, 0.1745, 0.0215, 1.0)
    diffuse = (0.07568, 0.61424, 0.07568, 1.0)
    specular = (0.633, 0.727811, 0.633, 1.0)
    shininess = 0.6
  elif name == 'jade':
    ambient = (0.135, 0.2225, 0.1575, 1.0)
    diffuse = (0.54, 0.89, 0.63, 1.0)
    specular = (0.316228, 0.316228, 0.316228, 1.0)
    shininess = 0.1
  elif name == 'cube':
    ambient = (0.0, 0.0, 0.0, 0.5)
    diffuse = (0.1, 0.65, 0.1, 0.5)
    specular = (0.45, 0.55, 0.45, 0.5)
    shininess = 0.25
  elif name == 'north':
    ambient = (0.0, 0.0, 0.0, 0.5)
    diffuse = (0.65, 0.1, 0.1, 0.5)
    specular = (0.55, 0.45, 0.45, 0.5)
    shininess = 0.25
  elif name == 'south':
    ambient = (0.0, 0.0, 0.0, 0.5)
    diffuse = (0.1, 0.1, 0.65, 0.5)
    specular = (0.45, 0.45, 0.55, 0.5)
    shininess = 0.25
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
