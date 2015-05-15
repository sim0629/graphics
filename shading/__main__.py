# coding: utf-8

import os
import sys

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

sys.path.insert(0, os.path.join(sys.path[0], '..'))
from viewer.camera import Camera
from viewer.wavefront import Mesh
sys.path.pop(0)

model = Mesh.load_from_file(os.path.join(sys.path[0], 'ring.obj'))
camera = Camera(model)
width, height = 600, 600

def reshape(new_width, new_height):
  global width, height
  width, height = new_width, new_height
  glViewport(0, 0, width, height)

def normalizeMouse(x, y):
  x, y = x / float(width), (height - y) / float(height)
  return 2.0 * x - 1.0, 2.0 * y - 1.0

def keyboard(ch, x, y):
  if ch == chr(27): # esc
    sys.exit(0)
  x, y = normalizeMouse(x, y)
  camera.keyboard(ch, x, y)

def mouse(button, state, x, y):
  x, y = normalizeMouse(x, y)
  camera.mouse(button, state, x, y)

def motion(x, y):
  x, y = normalizeMouse(x, y)
  camera.motion(x, y)

def display():
  camera.update()

  if camera.is_animating():
    glClearColor(0.5, 0.5, 0.5, 0.0)
  else:
    glClearColor(0.0, 0.0, 0.0, 0.0)
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

  glMatrixMode(GL_MODELVIEW)
  glColor(1.0, 1.0, 1.0)
  model.render()

  glutSwapBuffers()
  glutPostRedisplay()

def initializeWindow():
  glutInit(['shading'])
  glutInitWindowPosition(100, 100)
  glutInitWindowSize(width, height)
  glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
  glutCreateWindow('Shading by Gyumin Sim')

  glutReshapeFunc(reshape)
  glutDisplayFunc(display)
  glutKeyboardFunc(keyboard)
  glutMouseFunc(mouse)
  glutMotionFunc(motion)

def initializeSetting():
  glEnable(GL_LIGHTING)
  glEnable(GL_LIGHT0)
  glEnable(GL_COLOR_MATERIAL)
  glEnable(GL_NORMALIZE)
  glEnable(GL_DEPTH_TEST)

  glClearDepth(1.0)
  glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
  glLightfv(GL_LIGHT0, GL_POSITION, (1.0, 1.0, 1.0, 0.0))

  camera.adjust_to_model()
  camera.see()

if __name__ == '__main__':
  initializeWindow()
  initializeSetting()
  glutMainLoop()
