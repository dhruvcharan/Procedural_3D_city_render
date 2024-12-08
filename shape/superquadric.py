import copy
import glm
from OpenGL.GL import *
import numpy as np

from shape.glshape import GLShape

class SuperQuadric(GLShape):
    def __init__(self, shader, exponents: glm.vec3 = glm.vec3(1.0,1.0,0.0), scale: glm.vec3 = glm.vec3(1.0, 1.0, 1.0), model: glm.mat4 = glm.mat4(1.0), color: glm.vec3 = glm.vec3(0.3, 0.5, 0.7)):
        
        self.exponents = exponents
        self.scale = scale
        self.color = color
        super().__init__(shader, model)

        self.center: glm.vec3 = glm.vec3(0.0, 0.0, 0.0)
        self.color: glm.vec3 = copy.deepcopy(color)
        
        self.dummy: glm.array = glm.array(glm.float32, 0.0)  # Placeholder for buffer data
        self._initialize_buffers()
        self.tess_level_inner = 8
        self.tess_level_outer = 8
        
    def _initialize_buffers(self):
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * glm.sizeof(glm.float32), None)
        glBufferData(GL_ARRAY_BUFFER, self.dummy.nbytes, self.dummy.ptr, GL_STATIC_DRAW)
        
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        
        
    def render(self, timeElapsedSinceLastFrame: int) -> None:
        self.shader.use()
        self.shader.setMat4('model', self.model)
        self.shader.setVec3('color', self.color)
        self.shader.setVec3('center', self.center)
        self.shader.setVec3('exponents', self.exponents)  # e1, e2
        self.shader.setVec3('scale', self.scale)  # x, y, z scaling factors
        self.shader.setFloat('tessLevelInner', self.tess_level_inner)
        self.shader.setFloat('tessLevelOuter', self.tess_level_outer)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        
        glPatchParameteri(GL_PATCH_VERTICES, 1)
        glDrawArrays(GL_PATCHES, 0, 1)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        
    def subdivide(self):
        
        self.tess_level_inner = min(64, self.tess_level_inner + 2)
        self.tess_level_outer = min(64, self.tess_level_outer + 2)