# coding: utf-8

import os
import sys

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

model = None

def keyboard(ch, x, y):
  if ch == chr(27): # esc
    sys.exit(0)
  else:
    pass

def mouse(button, state, x, y):
  pass

def display():
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

  glMatrixMode(GL_MODELVIEW)
  model.render()

  glutSwapBuffers()

def initializeWindow():
  glutInit(['viewer'])
  glutInitWindowPosition(100, 100)
  glutInitWindowSize(600, 600)
  glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
  glutCreateWindow('3D model viewer by Gyumin Sim')

  glutDisplayFunc(display)
  glutKeyboardFunc(keyboard)
  glutMouseFunc(mouse)

def initializeSetting():
  glClearDepth(1.0)
  glClearColor(0.0, 0.0, 0.0, 0.0)

  glEnable(GL_DEPTH_TEST)
  glEnable(GL_LIGHTING)
  glEnable(GL_LIGHT0)
  glEnable(GL_NORMALIZE)
  glEnable(GL_COLOR_MATERIAL)

  glLightfv(GL_LIGHT0, GL_POSITION, (1.0, 1.0, 1.0, 0.0))

def prepareModel():
  sys.path.insert(0, os.path.join(sys.path[0], '..'))
  import hierarchy.oryzae

  pos = (0.0, 0.0, 0.0)
  scale = (1.0, 1.0, 1.0)

  global model
  model = hierarchy.oryzae.Oryzae(pos, scale)

def prepareCamera():
  glMatrixMode(GL_MODELVIEW)
  gluLookAt(
    0.0, 0.0, 3.0,
    0.0, 0.0, 0.0,
    0.0, 1.0, 0.0
  )

  glMatrixMode(GL_PROJECTION)
  gluPerspective(90.0, 1.0, 1.0, 30.0)

if __name__ == "__main__":
  initializeWindow()
  initializeSetting()
  prepareModel()
  prepareCamera()
  glutMainLoop()
