from shape.quadric import Quadric
import glm
import numpy as np

class Torus(Quadric):
    def __init__(self, shader, 
                 R: float = 1.0,  # Major radius (distance from center to tube center)
                 r: float = 0.25, # Minor radius (tube radius)
                 model: glm.mat4 = glm.mat4(1.0),
                 color: glm.vec3 = glm.vec3(0.3, 0.5, 0.7)):
        super().__init__(shader, model)
        self.R = R
        self.r = r
        self.color = color
        self._setup_buffers()
        
    def _setup_buffers(self):
        """Setup vertex buffers for the torus"""
        # Generate parametric surface points
        u, v = self.generate_parametric_surface([0, 2*np.pi], [0, 2*np.pi])
        
        vertices = []
        for i in range(self.tessellation_level - 1):
            for j in range(self.tessellation_level - 1):
                # Calculate vertices for current quad
                p1 = self._calculate_point(u[i,j], v[i,j])
                p2 = self._calculate_point(u[i+1,j], v[i+1,j])
                p3 = self._calculate_point(u[i+1,j+1], v[i+1,j+1])
                p4 = self._calculate_point(u[i,j+1], v[i,j+1])
                
                # Calculate normals
                n1 = self.calculate_normal(u[i,j], v[i,j])
                n2 = self.calculate_normal(u[i+1,j], v[i+1,j])
                n3 = self.calculate_normal(u[i+1,j+1], v[i+1,j+1])
                n4 = self.calculate_normal(u[i,j+1], v[i,j+1])
                
                # Add two triangles for the quad
                vertices.extend(self._create_vertex_data([p1, p2, p3], [n1, n2, n3]))
                vertices.extend(self._create_vertex_data([p1, p3, p4], [n1, n3, n4]))
        
        self.vertices = glm.array(glm.float32, *vertices)
        
    def _calculate_point(self, u, v):
        """Calculate point on torus surface"""
        x = (self.R + self.r * np.cos(v)) * np.cos(u)
        y = (self.R + self.r * np.cos(v)) * np.sin(u)
        z = self.r * np.sin(v)
        return glm.vec3(x, y, z)
        
    def calculate_normal(self, u, v):
        """Calculate surface normal at point (u,v)"""
        # Normal is just the vector from the center of the tube to the point
        center_to_surface = glm.vec3(
            np.cos(v) * np.cos(u),
            np.cos(v) * np.sin(u),
            np.sin(v)
        )
        return glm.normalize(center_to_surface) 