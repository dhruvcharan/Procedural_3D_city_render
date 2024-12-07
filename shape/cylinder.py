import copy
from shape.glshape import GLShape
from shape.quadric import Quadric
import glm
from OpenGL.GL import *
import numpy as np

class Cylinder(GLShape):
    def __init__(self, shader, height: float = 1.0, radius: float = 0.5, model: glm.mat4 = glm.mat4(1.0), color: glm.vec3 = glm.vec3(0.3, 0.5, 0.7)):
        self.height = height
        self.radius = radius
        self.color = color
        super().__init__(shader, model)


        self.center : glm.vec3 = glm.vec3(0.0, 0.0, 0.0)
        self.color : glm.vec3 = copy.deepcopy(color)
        
        self.scale : glm.vec3 = glm.vec3(radius, height, 0.0)
        self.dummy : glm.array = glm.array(glm.float32, 0.0)
        self._initialize_buffers()
        
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
        self.shader.setVec3('center', self.center)
        self.shader.setVec3('scale', self.scale)
        self.shader.setVec3('color', self.color)
        
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        
        glPatchParameteri(GL_PATCH_VERTICES, 1)
        glDrawArrays(GL_PATCHES, 0, 1)
        
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
