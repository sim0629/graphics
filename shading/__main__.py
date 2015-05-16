# coding: utf-8

import os
import sys

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from scene import Scene

sys.path.insert(0, os.path.join(sys.path[0], '..'))
from viewer.camera import Camera
from viewer.wavefront import Mesh
sys.path.pop(0)

model = None
camera = None
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
  glClear(GL_COLOR_BUFFER_BIT)

  glMatrixMode(GL_MODELVIEW)
  glColor(1.0, 1.0, 1.0)
  model.render()

  glutSwapBuffers()
  glutPostRedisplay()

def initializeWindow():
  glutInit(['shading'])
  glutInitWindowPosition(100, 100)
  glutInitWindowSize(width, height)
  glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
  glutCreateWindow('Shading by Gyumin Sim')

  glutReshapeFunc(reshape)
  glutDisplayFunc(display)
  glutKeyboardFunc(keyboard)
  glutMouseFunc(mouse)
  glutMotionFunc(motion)

def initializeSetting():
  glEnable(GL_NORMALIZE)
  glEnable(GL_LIGHTING)
  glEnable(GL_COLOR_MATERIAL)

  glEnable(GL_LIGHT0)
  glLight(GL_LIGHT0, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))
  glLight(GL_LIGHT0, GL_DIFFUSE, (0.9, 0.9, 0.9, 1.0))
  glLight(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
  glLight(GL_LIGHT0, GL_POSITION, (1.0, 1.0, 1.0, 1.0))

def prepareScene():
  scene = Scene()

  ring = Mesh.load_from_file(os.path.join(sys.path[0], 'ring.obj'))
  cube = Mesh.load_from_file(os.path.join(sys.path[0], '../viewer/cube.obj'))
  scene.add_object(ring)
  scene.add_object(cube, [0.5, 0.5, 0.5], [1.57, 1.0, 0.0, 0.0], [0.2, 0.0, 0.0])

  global model
  model = scene.to_mesh()

  global camera
  camera = Camera(model)
  camera.adjust_to_model()
  camera.see()
  camera.show_all()

if __name__ == '__main__':
  initializeWindow()
  initializeSetting()
  prepareScene()
  glutMainLoop()
