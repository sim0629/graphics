# coding: utf-8

import os
import sys

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import cross
from data import Data
import swept

sys.path.insert(0, os.path.join(sys.path[0], '..'))
from viewer.camera import Camera
from viewer.wavefront import Mesh
sys.path.pop()

MODE_VIEW, MODE_CROSS = range(2)
mode = None

data = None
model = Mesh()
steps = 5
wire = True
camera = Camera(model)
width, height = 600, 600

def reshape(new_width, new_height):
  global width, height
  width, height = new_width, new_height
  glViewport(0, 0, width, height)

def normalizeMouse(x, y):
  x, y = x / float(width), (height - y) / float(height)
  return 2.0 * x - 1.0, 2.0 * y - 1.0

def changeSteps(d):
  global steps
  steps = max(1, steps + d)
  swept.generate_surface(model, data, steps)

def keyboard(ch, x, y):
  if ch == chr(27): # esc
    sys.exit(0)
  elif ch == '+' or ch == '-':
    changeSteps(1 if ch == '+' else -1)
  elif ch == 'p':
    global wire
    wire = not wire
  x, y = normalizeMouse(x, y)
  if mode == MODE_VIEW:
    camera.keyboard(ch, x, y)
  elif mode == MODE_CROSS:
    cross.keyboard(ch, x, y)

def mouse(button, state, x, y):
  x, y = normalizeMouse(x, y)
  if mode == MODE_VIEW:
    camera.mouse(button, state, x, y)
  elif mode == MODE_CROSS:
    cross.mouse(button, state, x, y)

def motion(x, y):
  x, y = normalizeMouse(x, y)
  if mode == MODE_VIEW:
    camera.motion(x, y)
  elif mode == MODE_CROSS:
    cross.motion(x, y)

def displayView():
  camera.update()
  if camera.is_animating():
    glClearColor(0.5, 0.5, 0.5, 0.0)
  else:
    glClearColor(0.0, 0.0, 0.0, 0.0)

  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

  glMatrixMode(GL_MODELVIEW)

  glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
  glColor(1.0, 1.0, 1.0)
  glEnable(GL_LIGHTING)
  model.render()

  if not wire:
    return

  glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
  glColor(0.5, 1.0, 0.5)
  glDisable(GL_LIGHTING)
  model.render()

def display():
  if mode == MODE_VIEW:
    displayView()
  elif mode == MODE_CROSS:
    cross.display()
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

def initializeSetting():
  glClearDepth(1.0)
  glClearColor(0.0, 0.0, 0.0, 0.0)

  glEnable(GL_DEPTH_TEST)
  glEnable(GL_LIGHT0)
  glEnable(GL_COLOR_MATERIAL)

  glLightfv(GL_LIGHT0, GL_POSITION, (1.0, 1.0, 1.0, 0.0))

  glLineWidth(2.0)

def changeToViewMode():
  swept.generate_surface(model, data, steps)
  camera.adjust_to_model()
  camera.see()
  global mode
  mode = MODE_VIEW

def changeToCrossMode():
  cross.start()
  global mode
  mode = MODE_CROSS

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
  cross.data = data

if __name__ == '__main__':
  parseArguments()
  initializeWindow()
  initializeSetting()
  changeToViewMode()
  glutMainLoop()
