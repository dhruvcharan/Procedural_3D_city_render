import glm
from mesh import Mesh
from shader import Shader


class Dodecahedron(Mesh):
    color: glm.vec3 = glm.vec3(0.7, 0.3, 0.3)
    
    def __init__(self, shader: Shader, tessellation_level: int = 32):
        super().__init__(shader, tessellation_level)
        
    def render(self, timeElapsedSinceLastFrame: int) -> None:
        self.shader.use()
        self.shader.setVec3('color', self.color)
        super().render(timeElapsedSinceLastFrame)
        