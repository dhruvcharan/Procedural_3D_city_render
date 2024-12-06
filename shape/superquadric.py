from shape.geometric_shape import GeometricShape
import glm
import numpy as np
from OpenGL.GL import *
class Superquadric(GeometricShape):
    """Base class for superquadric surfaces"""
    def __init__(self, shader, e1=1.0, e2=1.0, model: glm.mat4 = glm.mat4(1.0)):
        super().__init__(shader, model)
        self.e1 = e1  # East-west exponent
        self.e2 = e2  # North-south exponent
        self.tessellation_level = 32
        
    def sign(self, x):
        """Return the sign of x with the convention that sign(0) = 1"""
        return 1 if x >= 0 else -1
    
    def c(self, w, m):
        """Compute the cosine-like function"""
        return self.sign(np.cos(w)) * np.abs(np.cos(w)) ** m
    
    def s(self, w, m):
        """Compute the sine-like function"""
        return self.sign(np.sin(w)) * np.abs(np.sin(w)) ** m
        
    def generate_surface_point(self, eta, omega):
        """Generate a point on the superquadric surface"""
        x = self.c(eta, 2/self.e1) * self.c(omega, 2/self.e2)
        y = self.c(eta, 2/self.e1) * self.s(omega, 2/self.e2)
        z = self.s(eta, 2/self.e1)
        return glm.vec3(x, y, z)
        
    def calculate_normal(self, eta, omega):
        """Calculate surface normal at point (eta,omega)"""
        # Analytical normal calculation for superquadrics
        nx = (2/self.e1) * self.c(eta, 2-self.e1) * self.c(omega, 2-self.e2)
        ny = (2/self.e1) * self.c(eta, 2-self.e1) * self.s(omega, 2-self.e2)
        nz = (2/self.e2) * self.s(eta, 2-self.e2)
        return glm.normalize(glm.vec3(nx, ny, nz)) 

    def render(self, timeElapsedSinceLastFrame: int) -> None:
        self.shader.use()
        
        # Set uniforms
        self.shader.setMat4('model', self.model)
        self.shader.setVec2('exponents', glm.vec2(self.e1, self.e2))
        self.shader.setVec3('color', self.color)
        self.shader.setInt('tessLevel', self.tessellation_level)
        
        # Draw
        glBindVertexArray(self.vao)
        glPatchParameteri(GL_PATCH_VERTICES, 1)
        glDrawArrays(GL_PATCHES, 0, 1)
        glBindVertexArray(0)