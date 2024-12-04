import ctypes
from OpenGL.GL import *
import copy 
import glm
from shape.mesh import Mesh
from util import Shader

class Cube(Mesh):
    def __init__(self, shader: Shader,
                 color: glm.vec3 = glm.vec3(0.7, 0.3, 0.3),
                 model: glm.mat4 = glm.mat4(1.0)):
        
        vertices = [
            -0.5, -0.5,  0.5,  0.0,  0.0,  1.0,  color.x, color.y, color.z,  # 0
             0.5, -0.5,  0.5,  0.0,  0.0,  1.0,  color.x, color.y, color.z,  # 1
             0.5,  0.5,  0.5,  0.0,  0.0,  1.0,  color.x, color.y, color.z,  # 2
            -0.5,  0.5,  0.5,  0.0,  0.0,  1.0,  color.x, color.y, color.z,  # 3
            
            -0.5, -0.5, -0.5,  0.0,  0.0, -1.0,  color.x, color.y, color.z,  # 4
             0.5, -0.5, -0.5,  0.0,  0.0, -1.0,  color.x, color.y, color.z,  # 5
             0.5,  0.5, -0.5,  0.0,  0.0, -1.0,  color.x, color.y, color.z,  # 6
            -0.5,  0.5, -0.5,  0.0,  0.0, -1.0,  color.x, color.y, color.z,  # 7
            
             0.5, -0.5, -0.5,  1.0,  0.0,  0.0,  color.x, color.y, color.z,  # 8
             0.5,  0.5, -0.5,  1.0,  0.0,  0.0,  color.x, color.y, color.z,  # 9
             0.5,  0.5,  0.5,  1.0,  0.0,  0.0,  color.x, color.y, color.z,  # 10
             0.5, -0.5,  0.5,  1.0,  0.0,  0.0,  color.x, color.y, color.z,  # 11
            
            -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,  color.x, color.y, color.z,  # 12
            -0.5,  0.5, -0.5, -1.0,  0.0,  0.0,  color.x, color.y, color.z,  # 13
            -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,  color.x, color.y, color.z,  # 14
            -0.5, -0.5,  0.5, -1.0,  0.0,  0.0,  color.x, color.y, color.z,  # 15
            
            -0.5,  0.5, -0.5,  0.0,  1.0,  0.0,  color.x, color.y, color.z,  # 16
             0.5,  0.5, -0.5,  0.0,  1.0,  0.0,  color.x, color.y, color.z,  # 17
             0.5,  0.5,  0.5,  0.0,  1.0,  0.0,  color.x, color.y, color.z,  # 18
            -0.5,  0.5,  0.5,  0.0,  1.0,  0.0,  color.x, color.y, color.z,  # 19
            
            -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,  color.x, color.y, color.z,  # 20
             0.5, -0.5, -0.5,  0.0, -1.0,  0.0,  color.x, color.y, color.z,  # 21
             0.5, -0.5,  0.5,  0.0, -1.0,  0.0,  color.x, color.y, color.z,  # 22
            -0.5, -0.5,  0.5,  0.0, -1.0,  0.0,  color.x, color.y, color.z,  # 23
        ]

        indices = [
            0,  1,  2,  2,  3,  0,   
            4,  5,  6,  6,  7,  4,   
            8,  9,  10, 10, 11, 8,   
            12, 13, 14, 14, 15, 12,  
            16, 17, 18, 18, 19, 16,  
            20, 21, 22, 22, 23, 20   
        ]
        
        vertex_data = []
        for i in range(0, len(indices), 3):
            for j in range(3):
                idx = indices[i + j]
                base = idx * 9
                vertex_data.extend(vertices[base:base + 9])
        
        self.vertices = glm.array(glm.float32, *vertex_data)
        super().__init__(shader, self.vertices, model)