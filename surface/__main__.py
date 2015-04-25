# coding: utf-8

import os
import sys

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from data import Data
import swept

sys.path.insert(0, os.path.join(sys.path[0], '..'))
from viewer.camera import Camera
from viewer.wavefront import Mesh
sys.path.pop()

MODE_VIEW, MODE_EDIT = range(2)
mode = None

data = None
model = Mesh()
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
  if mode == MODE_VIEW:
    x, y = normalizeMouse(x, y)
    camera.keyboard(ch, x, y)

def mouse(button, state, x, y):
  if mode == MODE_VIEW:
    x, y = normalizeMouse(x, y)
    camera.mouse(button, state, x, y)

def motion(x, y):
  if mode == MODE_VIEW:
    x, y = normalizeMouse(x, y)
    camera.motion(x, y)

def displayView():
  camera.update()
  if camera.is_animating():
    glClearColor(0.5, 0.5, 0.5, 0.0)
  else:
    glClearColor(0.0, 0.0, 0.0, 0.0)

  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

  glMatrixMode(GL_MODELVIEW)
  model.render()

def display():
  if mode == MODE_VIEW:
    displayView()
  else:
    pass

  glutSwapBuffers()
  glutPostRedisplay()

def initializeWindow():
  glutInit(['surface'])
  glutInitWindowPosition(100, 100)
  glutInitWindowSize(width, height)
  glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
  glutCreateWindow('Swept Surface Designer by Gyumin Sim')

  glutReshapeFunc(reshape)
  glutDisplayFunc(display)
  glutKeyboardFunc(keyboard)
  glutMouseFunc(mouse)
  glutMotionFunc(motion)

def settingForViewMode():
  glClearDepth(1.0)
  glClearColor(0.0, 0.0, 0.0, 0.0)

  glEnable(GL_DEPTH_TEST)
  glEnable(GL_LIGHTING)
  glEnable(GL_LIGHT0)
  glEnable(GL_COLOR_MATERIAL)

  glLightfv(GL_LIGHT0, GL_POSITION, (1.0, 1.0, 1.0, 0.0))

def changeToViewMode():
  settingForViewMode()
  swept.generate_surface(model, data)
  camera.see()
  global mode
  mode = MODE_VIEW

def parseArguments():
  argc = len(sys.argv)
  if argc < 2:
    raise Exception('No command line argument')
  filename = sys.argv[1]
  if filename == 'sample':
    if argc < 5:
      raise Exception('Few arguments to generate data')
    t = sys.argv[2].upper()
    n = int(sys.argv[3])
    m = int(sys.argv[4])
    Data.sample(t, n, m)
    sys.exit(0)
  global data
  data = Data(filename)

if __name__ == '__main__':
  parseArguments()
  initializeWindow()
  changeToViewMode()
  glutMainLoop()
