import copy
import ctypes

from OpenGL.GL import *
import glm

from .glshape import GLShape
from .renderable import Renderable
from util import Shader

class SuperQuadric(GLShape, Renderable):
    def __init__(self, 
                 shader: Shader, 
                 center: glm.vec3, 
                 scale: glm.vec3, 
                 e1: float, 
                 e2: float, 
                 color: glm.vec3, 
                 model: glm.mat4 = glm.mat4(1.0)):
        
        super().__init__(shader, model)
        self.center = copy.deepcopy(center)
        self.scale = copy.deepcopy(scale)
        self.e1 = e1  # Shape parameter for latitude
        self.e2 = e2  # Shape parameter for longitude
        self.color = copy.deepcopy(color)
        self.dummy = glm.array(glm.float32, 0.0)
        
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

        # Placeholder attribute array
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 1, GL_FLOAT, GL_FALSE, glm.sizeof(glm.float32), None)

        glBufferData(GL_ARRAY_BUFFER,
                     self.dummy.nbytes,
                     self.dummy.ptr,
                     GL_STATIC_DRAW)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
    
    def render(self, timeElapsedSinceLastFrame: int) -> None:
        self.shader.use()
        self.shader.setMat4('model', self.model)
        self.shader.setVec3('center', self.center)
        self.shader.setVec3('scale', self.scale)
        self.shader.setFloat('e1', self.e1)
        self.shader.setFloat('e2', self.e2)
        self.shader.setVec3('color', self.color)
        
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

        glPatchParameteri(GL_PATCH_VERTICES, 1)
        glDrawArrays(GL_PATCHES, 0, 1)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)


class Ellipsoid(SuperQuadric):
    def __init__(self, shader, center, scale, color, model=glm.mat4(1.0)):
        super().__init__(shader, center, scale, 1.0, 1.0, color, model)

class Torus(SuperQuadric):
    def __init__(self, shader, center, scale, color, model=glm.mat4(1.0)):
        super().__init__(shader, center, scale, 0.5, 0.5, color, model)

class Cylinder(SuperQuadric):
    def __init__(self, shader, center, scale, color, model=glm.mat4(1.0)):
        super().__init__(shader, center, scale, 0.1, 1.0, color, model)

class Cone(SuperQuadric):
    def __init__(self, shader, center, scale, color, model=glm.mat4(1.0)):
        super().__init__(shader, center, scale, 0.5, 1.0, color, model)
