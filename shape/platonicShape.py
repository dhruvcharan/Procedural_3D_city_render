import glm
from typing import List
from OpenGL.GL import *
import numpy as np
from shape.mesh import Mesh
from util import Shader


class PlatonicShape(Mesh):
    def __init__(self, shader: Shader, file_path: str, model: glm.mat4 = glm.mat4(1.0), color: glm.vec3 = glm.vec3(1.0, 1.0, 1.0)):
        vertices = self._load_vertices_from_file(file_path, color)
        super().__init__(shader, vertices, model)

    @staticmethod
    def _load_vertices_from_file(file_path: str, color: glm.vec3) -> glm.array:
        """Reads the file, parses the vertex data, and constructs the vertex array with calculated normals."""
        vertex_data = []
        try:
            with open(file_path, 'r') as file:
                vertices = [list(map(float, line.split())) for line in file]
                for i in range(0, len(vertices), 3):
                    v0 = glm.vec3(*vertices[i])
                    v1 = glm.vec3(*vertices[i+1])
                    v2 = glm.vec3(*vertices[i+2])
                    edge1 = v1 - v0
                    edge2 = v2 - v0
                    normal = glm.normalize(glm.cross(edge1, edge2))
                    for v in [v0, v1, v2]:
                        vertex_data.extend([v.x, v.y, v.z, normal.x, normal.y, normal.z, color.x, color.y, color.z])
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
        
        return glm.array(glm.float32, *vertex_data)


class Tetrahedron(PlatonicShape):
    pass


class Cube(PlatonicShape):
    pass


class Octahedron(PlatonicShape):
    pass


class Dodecahedron(PlatonicShape):
    # def subdivide(self):
    #     vertex_size = 9
        
    #     # Create a list to store new vertices
    #     new_vertices = []
        
    #     # Process existing vertices in triangular groups
    #     for i in range(0, len(self.vertices), vertex_size * 3):
    #         # Extract the three vertices of the current face
    #         v1 = self.vertices[i:i+vertex_size]
    #         v2 = self.vertices[i+vertex_size:i+2*vertex_size]
    #         v3 = self.vertices[i+2*vertex_size:i+3*vertex_size]
            
    #         # Extract position, normal, and color
    #         pos1 = np.array(v1[0:3])
    #         pos2 = np.array(v2[0:3])
    #         pos3 = np.array(v3[0:3])
            
    #         # Compute midpoints
    #         mid1 = (pos1 + pos2) / 2
    #         mid2 = (pos2 + pos3) / 2
    #         mid3 = (pos3 + pos1) / 2
            
    #         # Normalize midpoints to maintain spherical shape
    #         mid1 = mid1 / np.linalg.norm(mid1)
    #         mid2 = mid2 / np.linalg.norm(mid2)
    #         mid3 = mid3 / np.linalg.norm(mid3)
            
    #         # Compute normals for midpoints (same as position direction)
    #         norm1 = mid1 / np.linalg.norm(mid1)
    #         norm2 = mid2 / np.linalg.norm(mid2)
    #         norm3 = mid3 / np.linalg.norm(mid3)
            
    #         # Use color from the first vertex (you might want to interpolate)
    #         color = v1[6:9]
            
    #         # Create new vertices for each midpoint
    #         def create_vertex(pos, norm, color):
    #             return [
    #                 *pos,    # position
    #                 *norm,   # normal
    #                 *color   # color
    #             ]
            
    #         # Create new face vertices
    #         new_face_vertices = [
    #             # Original vertices
    #             *v1, *v2, *v3,
                
    #             # Midpoint vertices
    #             *create_vertex(mid1, norm1, color),
    #             *create_vertex(mid2, norm2, color),
    #             *create_vertex(mid3, norm3, color)
    #         ]
            
    #         # Add new vertices to the list
    #         new_vertices.extend(new_face_vertices)
        
    #     # Update vertices with the new, more refined set
    #     self.vertices = glm.array(glm.float32, *new_vertices)
        
    #     # Rebind the vertex data to OpenGL
    #     glBindVertexArray(self.vao)
    #     glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
    #     glBufferData(GL_ARRAY_BUFFER,
    #                  self.vertices.nbytes,
    #                  self.vertices.ptr,
    #                  GL_STATIC_DRAW)
    #     glBindBuffer(GL_ARRAY_BUFFER, 0)
    #     glBindVertexArray(0)
    pass


class Icosahedron(PlatonicShape):
    pass