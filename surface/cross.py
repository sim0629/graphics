# coding: utf-8

from OpenGL.GL import *

data = None
idx = 0

def keyboard(ch, x, y):
  global idx
  if ch == ']':
    idx = (idx + 1) % data.n
  elif ch == '[':
    idx = (idx - 1) % data.n

def mouse(button, state, x, y):
  pass

def motion(x, y):
  pass

def display():
  pass

def start():
  pass

