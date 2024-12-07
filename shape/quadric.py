# from shape.geometric_shape import GeometricShape
# import glm
# import numpy as np
# from OpenGL.GL import *

# class Quadric(GeometricShape):
#     """Base class for quadric surfaces"""
#     def __init__(self, shader, model: glm.mat4 = glm.mat4(1.0)):
#         super().__init__(shader, model)
        
#     def render(self, timeElapsedSinceLastFrame: int) -> None:
#         self.shader.use()
        
#         # Set uniforms
#         self.shader.setMat4('model', self.model)
#         self.shader.setInt('shapeType', self.shape_type)
#         self.shader.setVec3('parameters', self.get_parameters())
#         self.shader.setVec3('color', self.color)
#         self.shader.setInt('tessLevel', self.tessellation_level)
        
#         # Draw
#         glBindVertexArray(self.vao)
#         glPatchParameteri(GL_PATCH_VERTICES, 1)
#         glDrawArrays(GL_PATCHES, 0, 1)
#         glBindVertexArray(0)
        
#     def generate_parametric_surface(self, u_range, v_range):
#         """Generate parametric surface points"""
#         u = np.linspace(u_range[0], u_range[1], self.tessellation_level)
#         v = np.linspace(v_range[0], v_range[1], self.tessellation_level)
#         return np.meshgrid(u, v)
        
#     def calculate_normal(self, u, v):
#         """Calculate surface normal at point (u,v)"""
#         # Will be implemented by specific quadric surfaces
#         pass

#     def _create_vertex_data(self, points, normals):
#         """Create vertex data from points and normals."""
#         vertex_data = []
#         for point, normal in zip(points, normals):
#             # Assuming each point and normal is a glm.vec3
#             vertex_data.extend([point.x, point.y, point.z])
#             vertex_data.extend([normal.x, normal.y, normal.z])
#             vertex_data.extend([self.color.x, self.color.y, self.color.z])  # Add color
#         return vertex_data

# class Sphere(Quadric):
#     def __init__(self, shader, radius=1.0, model: glm.mat4 = glm.mat4(1.0)):
#         super().__init__(shader, model)
#         self.radius = radius
        
#     def calculate_normal(self, u, v):
#         x = self.radius * np.sin(v) * np.cos(u)
#         y = self.radius * np.sin(v) * np.sin(u)
#         z = self.radius * np.cos(v)
#         return glm.normalize(glm.vec3(x, y, z))

# class Cylinder(Quadric):
#     def __init__(self, shader, radius=1.0, height=2.0, model: glm.mat4 = glm.mat4(1.0)):
#         super().__init__(shader, model)
#         self.radius = radius
#         self.height = height
        
#     def calculate_normal(self, u, v):
#         x = np.cos(u)
#         y = 0
#         z = np.sin(u)
#         return glm.normalize(glm.vec3(x, y, z))

# class Cone(Quadric):
#     def __init__(self, shader, radius=1.0, height=2.0, model: glm.mat4 = glm.mat4(1.0)):
#         super().__init__(shader, model)
#         self.radius = radius
#         self.height = height 
        


from OpenGL.GL import *
import glm
from util.shader import Shader
from shape.geometric_shape import GeometricShape


class Quadric(GeometricShape):
    """
    Base class for general-purpose quadrics (spheres, ellipsoids, cones, cylinders, torus, superquadrics, etc.)
    """

    def __init__(self, 
                 shader: Shader, 
                 shape_type: int, 
                 parameters: glm.vec3, 
                 model: glm.mat4 = glm.mat4(1.0), 
                 color: glm.vec3 = glm.vec3(1.0, 0.0, 0.0), 
                 base_tessellation_level: int = 32):
        """
        :param shader: The shader to be used for rendering the quadric.
        :param shape_type: Integer to define the type of the shape (0: Sphere, 1: Ellipsoid, 2: Cone, etc.).
        :param parameters: Shape-specific parameters (radius, height, etc.) as a glm.vec3.
        :param model: Transformation matrix (for scaling, rotation, and translation) as a glm.mat4.
        :param color: Color of the quadric.
        :param base_tessellation_level: Base tessellation level for this shape (default is 32).
        """
        super().__init__(shader, model)
        self.shape_type = shape_type  # Shape identifier (0 = Sphere, 1 = Ellipsoid, etc.)
        self.parameters = parameters  # Parameters for the shape, such as [radius, height, etc.]
        self.color = color  # Shape color
        self.base_tessellation_level = base_tessellation_level  # Base tessellation level for the shape
        self._setup_buffers()  # Set up the VAO and any required buffers

    def _setup_buffers(self):
        """Create the VAO for the quadric."""
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        glBindVertexArray(0)

    def set_tessellation_level(self, level: int):
        """Set the tessellation level for the quadric."""
        self.tessellation_level = max(1, level)  # Ensure at least 1 tessellation
        self._update_tessellation_level()

    def set_parameters(self, parameters: glm.vec3):
        """Update the parameters for the quadric (like radius, height, etc.)."""
        self.parameters = parameters

    def set_color(self, color: glm.vec3):
        """Set the color of the quadric."""
        self.color = color

    def set_model_matrix(self, model: glm.mat4):
        """Set the model matrix for the quadric."""
        self.model = model

    def render(self, timeElapsedSinceLastFrame: int = 0) -> None:
        """
        Render the quadric using tessellation.
        """
        self._apply_display_mode()  # Apply the display mode (wireframe, smooth, etc.)
        
        # Activate the shader program and set uniforms
        self.shader.use()
        
        # Set the model, view, and projection uniforms
        self.shader.setMat4('model', self.model)
        # self.shader.setMat4('view', self.view)
        # self.shader.setMat4('projection', self.projection)
        
        # Pass quadric-specific uniforms
        self.shader.setInt('shapeType', self.shape_type)  # Type of shape (0 = Sphere, 1 = Ellipsoid, etc.)
        self.shader.setVec3('parameters', self.parameters)  # Shape parameters (radius, height, etc.)
        self.shader.setVec3('color', self.color)  # Shape color
        self.shader.setInt('tessLevel', self.tessellation_level)  # Tessellation level
        
        # Render the patch using tessellation
        glBindVertexArray(self.vao)
        glPatchParameteri(GL_PATCH_VERTICES, 4)  # Define the patch to have 4 control points
        glDrawArrays(GL_PATCHES, 0, 1)  # Draw 1 patch
        glBindVertexArray(0)
        
class QEllipsoid(Quadric):
    def __init__(self, shader, a=1.0, b=2.0, c=1.5, model=glm.mat4(1.0), color=glm.vec3(1.0, 0.5, 0.2)):
        super().__init__(shader, shape_type=1, parameters=glm.vec3(a, b, c), model=model, color=color)
        
class QCone(Quadric):
    def __init__(self, shader, radius=1.0, height=2.0, model=glm.mat4(1.0), color=glm.vec3(1.0, 0.5, 0.2)):
        super().__init__(shader, shape_type=2, parameters=glm.vec3(radius, height, 0), model=model, color=color)
        
class QCylinder(Quadric):
    def __init__(self, shader, radius=1.0, height=2.0, model=glm.mat4(1.0), color=glm.vec3(1.0, 0.5, 0.2)):
        super().__init__(shader, shape_type=3, parameters=glm.vec3(radius, height, 0), model=model, color=color)
        
class QTorus(Quadric):
    def __init__(self, shader, major_radius=1.0, minor_radius=0.5, model=glm.mat4(1.0), color=glm.vec3(1.0, 0.5, 0.2)):
        super().__init__(shader, shape_type=4, parameters=glm.vec3(major_radius, minor_radius, 0), model=model, color=color)
        
class QSuperquadric(Quadric):
    def __init__(self, shader, a=1.0, b=1.0, c=1.0, n1=1.0, n2=1.0, model=glm.mat4(1.0), color=glm.vec3(1.0, 0.5, 0.2)):
        super().__init__(shader, shape_type=5, parameters=glm.vec3(a, b, c), model=model, color=color)
        
