# coding: utf-8

import os
import sys

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from scene import Scene
from bsp import BspTree
import material

sys.path.insert(0, os.path.join(sys.path[0], '..'))
from viewer.camera import Camera
sys.path.pop(0)

tree = None
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
  glBegin(GL_TRIANGLES)
  if tree is not None:
    tree.render(camera.pos)
  glEnd()

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

  glEnable(GL_LIGHT0)
  glLight(GL_LIGHT0, GL_AMBIENT, (1.0, 1.0, 1.0, 1.0))
  glLight(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
  glLight(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
  glLight(GL_LIGHT0, GL_POSITION, (1.0, 1.0, 1.0, 1.0))

  glEnable(GL_BLEND)
  glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def prepareScene():
  scene = Scene()

  ring = material.load_object('ring')
  scene.add_object(ring, [1.0, 1.0, 1.0], [1.05, -1.0, 0.0, 0.0], [0.0, 0.0, 0.0])
  cube = material.load_object('cube')
  scene.add_object(cube, [0.5, 0.5, 0.5], [0.0, 1.0, 0.0, 0.0], [0.2, 0.0, 0.6])

  global tree
  model = scene.to_mesh()
  tree = BspTree.tree(model)

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
