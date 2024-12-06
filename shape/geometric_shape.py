from shape.renderable import Renderable
from util.display_mode import DisplayMode
from util.shader import Shader
import glm
from OpenGL.GL import *

class GeometricShape(Renderable):
    """Base class for all geometric shapes with display mode support"""
    def __init__(self, shader: Shader, model: glm.mat4 = glm.mat4(1.0)):
        self.shader = shader
        self.model = model
        self.display_mode = DisplayMode.SMOOTH
        self.base_tessellation_level = 32
        self.subdivision_level = 0
        self._update_tessellation_level()
        
    def _update_tessellation_level(self):
        """Update tessellation level based on subdivision level"""
        self.tessellation_level = self.base_tessellation_level * (2 ** self.subdivision_level)
        if hasattr(self, 'shader'):
            self.shader.use()
            self.shader.setInt('tessLevel', self.tessellation_level)
    
    def subdivide(self):
        """Increase subdivision level"""
        self.subdivision_level += 1
        self._update_tessellation_level()
        
    def _apply_display_mode(self):
        """Apply current display mode settings to shader"""
        self.shader.use()
        self.shader.setInt('displayMode', self.display_mode.value)
        self.shader.setMat4('model', self.model) 