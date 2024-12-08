import glm
import numpy as np
import glm
from OpenGL.GL import *
import numpy as np
from shape.glshape import GLShape
import copy
from shape.geometric_shape import GeometricShape

class Torus(GeometricShape):
    
    def __init__(self, shader, major_radius: float = 1.0, minor_radius: float = 0.5, model: glm.mat4 = glm.mat4(1.0), color: glm.vec3 = glm.vec3(0.3, 0.5, 0.7)):
        self.major_radius = major_radius
        self.minor_radius = minor_radius
        self.color = color
        super().__init__(shader, model,color)
        
        self.center : glm.vec3 = glm.vec3(0.0, 0.0, 0.0)
        self.color : glm.vec3 = copy.deepcopy(color)
        
        self.radii : glm.vec2 = glm.vec2(major_radius, minor_radius)
        self.dummy : glm.array = glm.array(glm.float32, 0.0)
        
        self.tess_level_inner = 8
        self.tess_level_outer = 8
        
        self._initialize_buffers()

    def _initialize_buffers(self):
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * glm.sizeof(glm.float32), None)
        glBufferData(GL_ARRAY_BUFFER, self.dummy.nbytes, self.dummy.ptr, GL_STATIC_DRAW)
        
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0) 
        
    def render(self, timeElapsedSinceLastFrame: int) -> None:
        self.shader.use()
        self.shader.setMat4('model', self.model)
        self.shader.setVec3('center', self.center)
        self.shader.setVec2('radii', self.radii)
        self.shader.setVec3('color', self.color)
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