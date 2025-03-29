import noise  # Simplex/Perlin noise library
import numpy as np
import glm
from scene import Scene


from util.shader import Shader

def generate_terrain(shader: Shader, size: int, scale: float, height_scale: float) -> glm.array:
    """Generate a terrain mesh using Perlin noise."""
    vertices = []
    for z in range(size):
        for x in range(size):
            # Generate Perlin noise value for the vertex height
            height = noise.pnoise2(x * scale, z * scale) * height_scale
            vertices.extend([
                x, height, z,          # Position
                0.0, 1.0, 0.0,         # Normal (simplified)
                0.3, 0.6, 0.2          # Color (greenish terrain)
            ])
    
    indices = []  
    
    return glm.array(glm.float32, *vertices)

# Add terrain to the scene
