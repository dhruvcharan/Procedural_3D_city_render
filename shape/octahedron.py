import ctypes
from OpenGL.GL import *
import copy 
import glm
from shape.mesh import Mesh
from util import Shader

class Octahedron(Mesh):
    def __init__(self, shader: Shader,
                 color: glm.vec3 = glm.vec3(0.7, 0.3, 0.3),
                 model: glm.mat4 = glm.mat4(1.0)):
        
        vertices = [
            0.0,1.0,0.0,
            1.0,0.0,0.0,
            -1.0,0.0,0.0,
            0.0,0.0,1.0,
            0.0,-1.0,0.0,
        ]
        
        vertex_data = []
        faces = [(0,2,3),(0,3,1),(0,1,4),(0,4,2),
                 (5,3,2),(5,1,3),(5,2,4),(5,4,1)]
        
        for face in faces:
            v1 = glm.vec3(vertices[face[0] * 3], vertices[face[0] * 3 + 1], vertices[face[0] * 3 + 2])
            v2 = glm.vec3(vertices[face[1] * 3], vertices[face[1] * 3 + 1], vertices[face[1] * 3 + 2])
            v3 = glm.vec3(vertices[face[2] * 3], vertices[face[2] * 3 + 1], vertices[face[2] * 3 + 2])
            
            normal = glm.normalize(glm.cross(v2 - v1, v3 - v1))
            
            
            for vertex in [v1, v2, v3]:
                vertex_data.extend([vertex.x, vertex.y, vertex.z, normal.x, normal.y, normal.z, color.x, color.y, color.z])
        
        self.vertices = glm.array(glm.float32,*vertex_data)
        super().__init__(shader, self.vertices, model)        
                                
