# coding: utf-8

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(sys.path[0], '..'))
from viewer.wavefront import Mesh
import viewer.quaternion as qt
sys.path.pop(0)

MODEL, SCALE, ROT, POS = range(4)

class Scene:

  def __init__(self):
    self.objects = []

  def add_object(self, model, scale = [1.0, 1.0, 1.0], rotation = [0.0, 1.0, 0.0, 0.0], position = [0.0, 0.0, 0.0]):
    self.objects.append((model, scale, rotation, position))

  def to_mesh(self):
    mesh = Mesh()

    for obj in self.objects:
      v_ofs = len(mesh.vertices)
      vt_ofs = len(mesh.textures)
      vn_ofs = len(mesh.normals)

      q = qt.from_rotation(obj[ROT])
      v_list = list(np.array([qt.rotate(q, v) for v in
        np.array(obj[MODEL].vertices) * np.array(obj[SCALE])])
        + np.array(obj[POS]))
      vt_list = obj[MODEL].textures
      vn_list = [qt.rotate(q, v) for v in obj[MODEL].normals]

      mesh.vertices += v_list
      mesh.textures += vt_list
      mesh.normals += vn_list

      mesh.faces += [[
        [p[0] + v_ofs,
         p[1] + vt_ofs if p[1] is not None else None,
         p[2] + vn_ofs if p[2] is not None else None]
        for p in face] for face in obj[MODEL].faces]

    return mesh

