# coding: utf-8

import os
import sys

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

model = None
camera = None
width, height = 600, 600

def reshape(new_width, new_height):
  global width, height
  width, height = new_width, new_height
  glViewport(0, 0, width, height)

def normalize_xy(x, y):
  x, y = x / float(width), (height - y) / float(height)
  return 2.0 * x - 1.0, 2.0 * y - 1.0

def keyboard(ch, x, y):
  if ch == chr(27): # esc
    sys.exit(0)
  else:
    x, y = normalize_xy(x, y)
    camera.keyboard(ch, x, y)

def mouse(button, state, x, y):
  x, y = normalize_xy(x, y)
  camera.mouse(button, state, x, y)

def motion(x, y):
  x, y = normalize_xy(x, y)
  camera.motion(x, y)

def display():
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

  glMatrixMode(GL_MODELVIEW)
  model.render()

  glutSwapBuffers()

def initializeWindow():
  glutInit(['viewer'])
  glutInitWindowPosition(100, 100)
  glutInitWindowSize(width, height)
  glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
  glutCreateWindow('3D model viewer by Gyumin Sim')

  glutReshapeFunc(reshape)
  glutDisplayFunc(display)
  glutKeyboardFunc(keyboard)
  glutMouseFunc(mouse)
  glutMotionFunc(motion)

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
  import camera

  global camera
  camera = camera.Camera()
  camera.init()

if __name__ == "__main__":
  initializeWindow()
  initializeSetting()
  prepareModel()
  prepareCamera()
  glutMainLoop()
