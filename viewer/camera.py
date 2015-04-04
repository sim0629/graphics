# coding: utf-8

import numpy as np

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import quaternion as qt

X, Y, Z = 0, 1, 2
IN, OUT = False, True

def is_pressed(flag):
  m = glutGetModifiers()
  return bool(m & flag)

def shift_pressed():
  return is_pressed(GLUT_ACTIVE_SHIFT)

def ctrl_pressed():
  return is_pressed(GLUT_ACTIVE_CTRL)

class Interpolation:

  def __init__(self, begin, end, count = 24):
    self.begin = begin
    self.end = end
    self.count = int(count)
    self.i = 0

  def is_done(self):
    return self.i >= self.count

  def next(self):
    self.i += 1
    if self.is_done():
      return self.end
    v = self.end - self.begin
    t = float(self.i) / self.count
    return self.begin + t * v

class Camera:

  def __init__(self, scene):
    self.pos = np.array([0.0, 0.0, 10.0])
    self.ref = np.array([0.0, 0.0, 0.0])
    self.up = np.array([0.0, 1.0, 0.0])
    self.theta = 60.0
    self.aspect = 1.0
    self.near = 3.0
    self.far = 30.0
    self.scene = scene

    self.pos_interp = None
    self.ref_interp = None
    self.up_interp = None

  def is_animating(self):
    return self.pos_interp is not None \
      or self.ref_interp is not None \
      or self.up_interp is not None

  def _look_at(self):
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(
      self.pos[X], self.pos[Y], self.pos[Z],
      self.ref[X], self.ref[Y], self.ref[Z],
      self.up[X], self.up[Y], self.up[Z]
    )

  def _perspective(self):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(
      self.theta, self.aspect,
      self.near, self.far
    )

  def init(self):
    self._look_at()
    self._perspective()

  def doly(self, out):
    speed = -0.1
    if out:
      speed = -speed
    v = self.pos - self.ref
    distance = np.sqrt(v.dot(v))
    if speed < 0 and distance + speed <= self.near \
      or speed > 0 and distance + speed >= self.far:
      return
    v *= speed / distance
    self.pos += v
    self._look_at()

  def zoom(self, out):
    speed = -1.0
    if out:
      speed = -speed
    if speed < 0 and self.theta + speed < 1.0 \
      or speed > 0 and self.theta + speed >= 180.0:
      return
    self.theta += speed
    self._perspective()

  def _get_nuv(self):
    n = self.prev_pos - self.prev_ref
    n /= np.sqrt(n.dot(n))
    u = np.cross(self.up, n) / np.sqrt(self.up.dot(self.up))
    v = np.cross(n, u)
    return n, u, v

  def _get_nearplane_half_size(self):
    height = np.tan(self.theta * 0.5 * np.pi / 180.0) * self.near
    width = height * self.aspect
    return np.array([width, height])

  def _nearplane_point(self, point):
    size = self._get_nearplane_half_size()
    point *= size
    n, u, v = self._get_nuv()
    o = self.prev_pos - self.near * n
    du = point[X] * u
    dv = point[Y] * v
    return o + du + dv

  def translate_start(self, source):
    self.prev_pos = self.pos
    self.prev_ref = self.ref
    self.n_source = self._nearplane_point(source)

  def translate(self, target):
    n_target = self._nearplane_point(target)
    displacement = n_target - self.n_source

    self.pos = self.prev_pos - displacement
    self.ref = self.prev_ref - displacement

    self._look_at()

  def _trackball_point(self, point):
    n_point = self._nearplane_point(point)

    v = n_point - self.prev_pos
    v /= np.sqrt(v.dot(v))

    l = self.prev_ref - self.prev_pos
    ll = l.dot(l)

    t = l.dot(v)
    dd = ll - t * t
    d = np.sqrt(dd)

    r = np.sqrt(l.dot(l)) - self.near
    rr = r * r

    len_l = np.sqrt(ll)
    unit_l = l / len_l
    axis = np.cross(unit_l, v)

    if dd > rr:
      sin = r / len_l
      s = np.sqrt(ll - rr)
      cos = s / len_l
      q = qt.Quaternion.from_axis_and_angle(axis, sin, cos)
      p = self.prev_pos + s * q.rotate(unit_l)
    else: # intersects
      sin = d / len_l
      cos = t / len_l
      q = qt.Quaternion.from_axis_and_angle(axis, sin, cos)
      dt = np.sqrt(rr - dd)
      t -= dt
      p = self.prev_pos + t * q.rotate(unit_l)

    return p

  def rotate_start(self, source):
    self.prev_pos = self.pos
    self.prev_ref = self.ref
    self.prev_up = self.up
    self.t_source = self._trackball_point(source)

  def rotate(self, target):
    s = self.t_source - self.prev_ref
    e = self._trackball_point(target) - self.prev_ref

    q = qt.Quaternion.from_two_vectors(s, e)
    q = q.conjugate()

    v = self.prev_pos - self.prev_ref
    self.pos = self.prev_ref + q.rotate(v)
    self.up = q.rotate(self.prev_up)

    self._look_at()

  def _intersect_triangle_with_ray(self, triangle, ray):
    v0, v1, v2 = triangle
    p = self.pos

    x = v1 - v0
    y = v2 - v0
    n = np.cross(x, y)
    l = np.sqrt(n.dot(n))
    if l < 1e-8:
      return None
    n /= l

    d = n.dot(v0 - p) / n.dot(ray)
    if d < 0.0:
      return None

    q = p + d * ray
    w = q - v0

    m = x.dot(y) * x.dot(y) - x.dot(x) * y.dot(y)
    if np.abs(m) < 1e-8:
      return None

    s = (x.dot(y) * w.dot(y) - y.dot(y) * w.dot(x)) / m
    t = (x.dot(y) * w.dot(x) - x.dot(x) * w.dot(y)) / m
    if s < 0.0 or t < 0.0 or s + t > 1.0:
      return None

    return q

  def _pick_point_on_scene(self, point):
    n_point = self._nearplane_point(point)
    v = n_point - self.pos
    l = np.sqrt(v.dot(v))
    v /= l

    min_distance2 = np.inf
    min_picked = None

    for model in self.scene:
      for face in model.faces:
        triangle = [
          np.array(model.vertices[face[0][0]]),
          np.array(model.vertices[face[1][0]]),
          np.array(model.vertices[face[2][0]]),
        ]
        picked = self._intersect_triangle_with_ray(triangle, v)
        if picked is None:
          continue

        x = self.pos - picked
        distance2 = x.dot(x)
        if distance2 < min_distance2:
          min_distance2 = distance2
          min_picked = picked

    return min_picked

  def pick(self, point):
    self.prev_pos = self.pos
    self.prev_ref = self.ref

    picked = self._pick_point_on_scene(point)
    if picked is None:
      return

    self.ref_interp = Interpolation(self.ref, picked)
    _, _, v = self._get_nuv()
    self.ref_up = Interpolation(self.up, v)

  def keyboard(self, ch, x, y):
    if self.is_animating():
      return

    if ch == 'w':
      self.doly(IN)
    elif ch == 's':
      self.doly(OUT)
    elif ch == 'd':
      self.zoom(IN)
    elif ch == 'a':
      self.zoom(OUT)
    else:
      pass

  def mouse(self, button, state, x, y):
    if self.is_animating():
      return

    if state == GLUT_DOWN:
      source = np.array([x, y])
      if ctrl_pressed():
        self.pick(source)
      elif shift_pressed():
        self.method = 'translate'
        self.translate_start(source)
      else:
        self.method = 'rotate'
        self.rotate_start(source)
    elif state == GLUT_UP:
      self.method = None
    else:
      pass

  def motion(self, x, y):
    if self.is_animating():
      return

    target = np.array([x, y])
    if self.method == 'translate':
      self.translate(target)
    elif self.method == 'rotate':
      self.rotate(target)
    else:
      pass

  def update(self):
    if not self.is_animating():
      return

    if self.pos_interp is not None:
      self.pos = self.pos_interp.next()
      if self.pos_interp.is_done():
        self.pos_interp = None

    if self.ref_interp is not None:
      self.ref = self.ref_interp.next()
      if self.ref_interp.is_done():
        self.ref_interp = None

    if self.up_interp is not None:
      self.up = self.up_interp.next()
      if self.up_interp.is_done():
        self.up_interp = None

    self._look_at()

