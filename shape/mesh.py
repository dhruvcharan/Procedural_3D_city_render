import copy
import ctypes

from OpenGL.GL import *
import glm

from .glshape import GLShape
from .renderable import Renderable
from util import Shader


class Mesh(GLShape, Renderable):
    def __init__(self, 
                 shader: Shader, 
                 vertices: glm.array, 
                 model: glm.mat4 = glm.mat4(1.0),
                 color: glm.vec3 = glm.vec3(0.3, 0.5, 0.7)):
        
        self.color = color
        assert vertices.element_type == glm.float32 and vertices.length % (9 * 3) == 0, \
               'vertices should be alm.array of dtype glm.float32, ' \
               'each nine glm.flost32s constitute a vertex (pos, normal, color), ' \
               'each attribute is composed of three glm.float32s: (x, y, z) or (r, g, b), ' \
               'each three attributes denote a triangular facet'
        
        super().__init__(shader, model)
        self.vertices: glm.array = copy.deepcopy(vertices)
        
        glBindVertexArray(self.vao);
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo);

        # Vertex coordinate attribute array "layout (position = 0) in vec3 aPosition"
        glEnableVertexAttribArray(0);
        glVertexAttribPointer(0,                            # index: corresponds to "0" in "layout (position = 0)"
                              3,                            # size: each "vec3" generic vertex attribute has 3 values
                              GL_FLOAT,                     # data type: "vec3" generic vertex attributes are GL_FLOAT
                              GL_FALSE,                     # do not normalize data
                              9 * glm.sizeof(glm.float32),  # stride between attributes in VBO data
                              None)                         # offset of 1st attribute in VBO data
        
        # Normal vertex attribute array "layout (position = 1) in vec3 aNormal"
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1,
                              3,
                              GL_FLOAT,
                              GL_FALSE,
                              9 * glm.sizeof(glm.float32),
                              ctypes.c_void_p(3 * glm.sizeof(glm.float32)))
        
        # Vertex color attribute array "layout (position = 2) in vec3 aColor"
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2,
                              3,
                              GL_FLOAT,
                              GL_FALSE,
                              9 * glm.sizeof(glm.float32),
                              ctypes.c_void_p(6 * glm.sizeof(glm.float32)))

        glBufferData(GL_ARRAY_BUFFER,
                     self.vertices.nbytes,
                     self.vertices.ptr,
                     GL_STATIC_DRAW)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
    
    def render(self, timeElapsedSinceLastFrame: int) -> None:
        self.shader.use()
        self.shader.setMat4("model", self.model)
        

        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

        glDrawArrays(GL_TRIANGLES,
                     0,                          # start from index 0 in current VBO
                     self.vertices.length // 9)  # draw these number of vertice attributes

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        
    
    def subdivide(self):
        new_vertices = []

        # Each triangle has 3 vertices, each vertex has 9 floats (pos, normal, color)
        # So one triangle = 27 floats.
        for i in range(0, self.vertices.length, 27):
            # Extract the three vertices (positions, normals, colors)
            # Vertex 1
            v1 = glm.vec3(self.vertices[i],     self.vertices[i+1],  self.vertices[i+2])
            n1 = glm.vec3(self.vertices[i+3],   self.vertices[i+4],  self.vertices[i+5])
            c1 = glm.vec3(self.vertices[i+6],   self.vertices[i+7],  self.vertices[i+8])

            # Vertex 2
            v2 = glm.vec3(self.vertices[i+9],   self.vertices[i+10], self.vertices[i+11])
            n2 = glm.vec3(self.vertices[i+12],  self.vertices[i+13], self.vertices[i+14])
            c2 = glm.vec3(self.vertices[i+15],  self.vertices[i+16], self.vertices[i+17])

            # Vertex 3
            v3 = glm.vec3(self.vertices[i+18],  self.vertices[i+19], self.vertices[i+20])
            n3 = glm.vec3(self.vertices[i+21],  self.vertices[i+22], self.vertices[i+23])
            c3 = glm.vec3(self.vertices[i+24],  self.vertices[i+25], self.vertices[i+26])

            # Compute the midpoints on the unit sphere
            v12 = glm.normalize((v1 + v2) * 0.5)
            v23 = glm.normalize((v2 + v3) * 0.5)
            v31 = glm.normalize((v3 + v1) * 0.5)

            # For a perfect unit sphere, the normal is the same as the vertex position direction
            n12 = v12
            n23 = v23
            n31 = v31

            # Compute interpolated colors (simply average)
            c12 = (c1 + c2) * 0.5
            c23 = (c2 + c3) * 0.5
            c31 = (c3 + c1) * 0.5

            # Add the four new facets
            # Facet 1: (v1, v12, v31)
            new_vertices.extend([
                v1.x, v1.y, v1.z, n1.x, n1.y, n1.z, c1.x, c1.y, c1.z,
                v12.x, v12.y, v12.z, n12.x, n12.y, n12.z, c12.x, c12.y, c12.z,
                v31.x, v31.y, v31.z, n31.x, n31.y, n31.z, c31.x, c31.y, c31.z
            ])

            # Facet 2: (v2, v23, v12)
            new_vertices.extend([
                v2.x, v2.y, v2.z, n2.x, n2.y, n2.z, c2.x, c2.y, c2.z,
                v23.x, v23.y, v23.z, n23.x, n23.y, n23.z, c23.x, c23.y, c23.z,
                v12.x, v12.y, v12.z, n12.x, n12.y, n12.z, c12.x, c12.y, c12.z
            ])

            # Facet 3: (v3, v31, v23)
            new_vertices.extend([
                v3.x, v3.y, v3.z, n3.x, n3.y, n3.z, c3.x, c3.y, c3.z,
                v31.x, v31.y, v31.z, n31.x, n31.y, n31.z, c31.x, c31.y, c31.z,
                v23.x, v23.y, v23.z, n23.x, n23.y, n23.z, c23.x, c23.y, c23.z
            ])

            # Facet 4: (v12, v23, v31)
            new_vertices.extend([
                v12.x, v12.y, v12.z, n12.x, n12.y, n12.z, c12.x, c12.y, c12.z,
                v23.x, v23.y, v23.z, n23.x, n23.y, n23.z, c23.x, c23.y, c23.z,
                v31.x, v31.y, v31.z, n31.x, n31.y, n31.z, c31.x, c31.y, c31.z
            ])

        # Update the vertices array
        self.vertices = glm.array(glm.float32, *new_vertices)
        
        # Update the GPU data
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER,
                    self.vertices.nbytes,
                    self.vertices.ptr,
                    GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
    
    def translate(self, offset: glm.vec3):
        self.model = glm.translate(self.model, offset)

    def rotate(self, angle: float, axis: glm.vec3):
        self.model = glm.rotate(self.model, glm.radians(angle), axis)

    def scale_object(self, scale: glm.vec3):
        self.model = glm.scale(self.model, scale)
        
    def set_shading_mode(self, mode: int):
        self.shader.use()
        self.shader.setInt('shadingMode', mode)
        return self
