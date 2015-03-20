# coding: utf-8

import sys

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import oryzae

model = None

def keyboard(ch, x, y):
  if ch == chr(27):
    sys.exit(0)
  return 0

def display():
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

  model.render()

  glutSwapBuffers()
  return

def init():
  glClearDepth(1.0)
  glClearColor(0.0, 0.0, 0.0, 0.0)

  glEnable(GL_DEPTH_TEST)
  glEnable(GL_LIGHTING)
  glEnable(GL_LIGHT0)
  glLightfv(GL_LIGHT0, GL_POSITION, (1.0, 1.0, 1.0, 1.0))

  glMatrixMode(GL_PROJECTION)
  glFrustum(-1.0, 1.0, -1.0, 1.0, 1.0, 30)

  glMatrixMode(GL_MODELVIEW)

def makeModel():
  global model
  pos = (0.0, 0.0, -3.0)
  scale = (1.0, 1.0, 1.0)
  model = oryzae.Oryzae(pos, scale)

if __name__ == "__main__":
  glutInit(['hierarchy'])
  glutInitWindowPosition(100, 100)
  glutInitWindowSize(600, 600)
  glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
  glutCreateWindow('Hierarchical model by Gyumin Sim')
  glutDisplayFunc(display)
  glutKeyboardFunc(keyboard)

  init()
  makeModel()
  glutMainLoop()
