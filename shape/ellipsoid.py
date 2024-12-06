from shape.quadric import Quadric
import glm
import numpy as np

class Ellipsoid(Quadric):
    def __init__(self, shader, 
                 a: float = 1.0,  # x-axis radius
                 b: float = 0.75, # y-axis radius
                 c: float = 0.5,  # z-axis radius
                 model: glm.mat4 = glm.mat4(1.0),
                 color: glm.vec3 = glm.vec3(0.7, 0.2, 0.2)):
        super().__init__(shader, model)
        self.a = a
        self.b = b
        self.c = c
        self.color = color
        self._setup_buffers()
        
    def _setup_buffers(self):
        """Setup vertex buffers for the ellipsoid"""
        # Generate parametric surface points
        u, v = self.generate_parametric_surface([0, 2*np.pi], [0, np.pi])
        
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
        """Calculate point on ellipsoid surface"""
        x = self.a * np.sin(v) * np.cos(u)
        y = self.b * np.sin(v) * np.sin(u)
        z = self.c * np.cos(v)
        return glm.vec3(x, y, z)
        
    def calculate_normal(self, u, v):
        """Calculate surface normal at point (u,v)"""
        x = (np.sin(v) * np.cos(u)) / (self.a * self.a)
        y = (np.sin(v) * np.sin(u)) / (self.b * self.b)
        z = np.cos(v) / (self.c * self.c)
        return glm.normalize(glm.vec3(x, y, z))
        
    def _create_vertex_data(self, points, normals):
        """Create vertex data for a triangle"""
        data = []
        for p, n in zip(points, normals):
            data.extend([p.x, p.y, p.z])  # Position
            data.extend([n.x, n.y, n.z])  # Normal
            data.extend([self.color.x, self.color.y, self.color.z])  # Color
        return data 