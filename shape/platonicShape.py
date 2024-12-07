import glm
from typing import List
from OpenGL.GL import *
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
    pass


class Icosahedron(PlatonicShape):
    pass