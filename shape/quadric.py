from shape.geometric_shape import GeometricShape
import glm
import numpy as np
from OpenGL.GL import *

class Quadric(GeometricShape):
    """Base class for quadric surfaces"""
    def __init__(self, shader, model: glm.mat4 = glm.mat4(1.0)):
        super().__init__(shader, model)
        
    def render(self, timeElapsedSinceLastFrame: int) -> None:
        self.shader.use()
        
        # Set uniforms
        self.shader.setMat4('model', self.model)
        self.shader.setInt('shapeType', self.shape_type)
        self.shader.setVec3('parameters', self.get_parameters())
        self.shader.setVec3('color', self.color)
        self.shader.setInt('tessLevel', self.tessellation_level)
        
        # Draw
        glBindVertexArray(self.vao)
        glPatchParameteri(GL_PATCH_VERTICES, 1)
        glDrawArrays(GL_PATCHES, 0, 1)
        glBindVertexArray(0)
        
    def generate_parametric_surface(self, u_range, v_range):
        """Generate parametric surface points"""
        u = np.linspace(u_range[0], u_range[1], self.tessellation_level)
        v = np.linspace(v_range[0], v_range[1], self.tessellation_level)
        return np.meshgrid(u, v)
        
    def calculate_normal(self, u, v):
        """Calculate surface normal at point (u,v)"""
        # Will be implemented by specific quadric surfaces
        pass

class Sphere(Quadric):
    def __init__(self, shader, radius=1.0, model: glm.mat4 = glm.mat4(1.0)):
        super().__init__(shader, model)
        self.radius = radius
        
    def calculate_normal(self, u, v):
        x = self.radius * np.sin(v) * np.cos(u)
        y = self.radius * np.sin(v) * np.sin(u)
        z = self.radius * np.cos(v)
        return glm.normalize(glm.vec3(x, y, z))

class Cylinder(Quadric):
    def __init__(self, shader, radius=1.0, height=2.0, model: glm.mat4 = glm.mat4(1.0)):
        super().__init__(shader, model)
        self.radius = radius
        self.height = height
        
    def calculate_normal(self, u, v):
        x = np.cos(u)
        y = 0
        z = np.sin(u)
        return glm.normalize(glm.vec3(x, y, z))

class Cone(Quadric):
    def __init__(self, shader, radius=1.0, height=2.0, model: glm.mat4 = glm.mat4(1.0)):
        super().__init__(shader, model)
        self.radius = radius
        self.height = height 