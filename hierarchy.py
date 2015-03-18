# coding: utf-8

import sys

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

def keyboard(ch, x, y):
  if ch == chr(27):
    sys.exit(0)
  return 0

def display():
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

  # TODO: draw

  glutSwapBuffers()
  return

if __name__ == "__main__":
  glutInit(['hierarchy'])
  glutInitWindowPosition(100, 100)
  glutInitWindowSize(800, 600)
  glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
  glutCreateWindow('Hierarchical model by Gyumin Sim')
  glutDisplayFunc(display)
  glutKeyboardFunc(keyboard)

  glClearDepth(1.0)
  glClearColor(0.0, 0.0, 0.0, 0.0)

  glMatrixMode(GL_PROJECTION)
  glFrustum(-1.0, 1.0, -1.0, 1.0, 1.0, 30)

  glMatrixMode(GL_MODELVIEW)
  glEnable(GL_DEPTH_TEST)
  glShadeModel(GL_FLAT)
  glutMainLoop()
