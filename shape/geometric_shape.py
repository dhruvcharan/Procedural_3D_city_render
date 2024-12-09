import copy
from shape.renderable import Renderable
from util.display_mode import DisplayMode
from util.shader import Shader
import glm
from OpenGL.GL import *

class GeometricShape(Renderable):
    def __init__(self, shader: Shader, model: glm.mat4 = glm.mat4(1.0),color: glm.vec3 = glm.vec3(0.50, 0.20, 0.40)):
        self.shader = shader
        self.model = model
        self.color = copy.deepcopy(color)
        self.tess_level_inner = 32
        self.tess_level_outer = 32
        
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        

    def render(self, timeElapsedSinceLastFrame: int) -> None:
        self.shader.use()
        self.shader.setMat4('model', self.model)
        self.shader.setVec3('center', self.center)
        self.shader.setFloat('tessLevelInner', self.tess_level_inner)
        self.shader.setFloat('tessLevelOuter', self.tess_level_outer)
        self.shader.setVec3('color', self.color)
        

        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glPatchParameteri(GL_PATCH_VERTICES, 1)
        glDrawArrays(GL_PATCHES, 0, 1)
        
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def set_display_mode(self, display_mode: DisplayMode):
        self.display_mode = display_mode
        
    def subdivide(self):
        self.tess_level_inner = min(64, self.tess_level_inner + 2)
        self.tess_level_outer = min(64, self.tess_level_outer + 2)
        
    def rotate(self, angle: float, axis: glm.vec3 = glm.vec3(0.0, 1.0, 0.0)):
        self.model = glm.rotate(self.model, glm.radians(angle), axis)
        
    def translate(self, offset: glm.vec3):
        self.model = glm.translate(self.model, offset)
        
    def scale_object(self, scale: glm.vec3):
        self.model = glm.scale(self.model, scale)
    
    def set_shading_mode(self, mode: int):
        self.shader.use()
        self.shader.setInt('shadingMode', mode)
        return self
    