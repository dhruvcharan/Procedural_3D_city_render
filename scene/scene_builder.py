import random
from typing import List
import glm
from shape import *
from util import Shader

class SceneBuilder:
    def __init__(self):
        self.objects: List[Renderable] = []
        self.shaders: dict = {} 
        
        
    def add_sphere(self, shader: Shader, center: glm.vec3, radius: float, 
                  color: glm.vec3, model: glm.mat4 = glm.mat4(1.0)) -> None:
        """Add a sphere to the scene"""
        self.objects.append(Sphere(shader, center, radius, color, model))
        
    def add_mesh(self, shader: Shader, vertices: glm.array, 
                model: glm.mat4 = glm.mat4(1.0)) -> None:
        """Add a mesh to the scene"""
        self.objects.append(Mesh(shader, vertices, model))
        
    def add_tetrahedron(self, shader: Shader, vertex_file: str, 
                       model: glm.mat4 = glm.mat4(1.0)) -> None:
        """Add a tetrahedron to the scene"""
        self.objects.append(Tetrahedron(shader, vertex_file, model))
        
    def build_demo_scene(self, shaders: dict) -> None:
        """Build a demo scene with various objects"""
        # Add ground plane (large flat mesh)
        ground_vertices = self._create_ground_plane(20.0, glm.vec3(0.5, 0.5, 0.5))
        self.add_mesh(shaders['mesh'], ground_vertices)
        
        # Add spheres in a circle
        radius = 5.0
        num_spheres = 8
        for i in range(num_spheres):
            angle = (2.0 * glm.pi() * i) / num_spheres
            x = radius * glm.cos(angle)
            z = radius * glm.sin(angle)
            color = glm.vec3(
                glm.abs(glm.cos(angle)),
                0.5,
                glm.abs(glm.sin(angle))
            )
            self.add_sphere(
                shaders['sphere'],
                glm.vec3(x, 1.0, z),
                0.5,
                color
            )
        
        # Add central larger sphere
        self.add_sphere(
            shaders['sphere'],
            glm.vec3(0.0, 3.0, 0.0),
            1.0,
            glm.vec3(1.0, 1.0, 1.0)
        )
        
        # Add some tetrahedra
        tetra_positions = [
            glm.vec3(-3.0, 0.5, -3.0),
            glm.vec3(3.0, 0.5, 3.0),
            glm.vec3(-3.0, 0.5, 3.0),
            glm.vec3(3.0, 0.5, -3.0)
        ]
        
        for pos in tetra_positions:
            model = glm.translate(glm.mat4(1.0), pos)
            self.add_tetrahedron(shaders['mesh'], 'assets/tetrahedron.txt', model)
    
    def _create_ground_plane(self, size: float, color: glm.vec3) -> glm.array:
        """Create vertices for a ground plane"""
        half_size = size / 2.0
        vertices = [
            # First triangle
            -half_size, 0.0, -half_size,  0.0, 1.0, 0.0,  color.x, color.y, color.z,
            half_size, 0.0, -half_size,   0.0, 1.0, 0.0,  color.x, color.y, color.z,
            half_size, 0.0, half_size,    0.0, 1.0, 0.0,  color.x, color.y, color.z,
            # Second triangle
            -half_size, 0.0, -half_size,  0.0, 1.0, 0.0,  color.x, color.y, color.z,
            half_size, 0.0, half_size,    0.0, 1.0, 0.0,  color.x, color.y, color.z,
            -half_size, 0.0, half_size,   0.0, 1.0, 0.0,  color.x, color.y, color.z,
        ]
        return glm.array(glm.float32, *vertices)
    
    def get_mode_1_objects(self) -> List[Renderable]:
        """
        Mode 1: Display Tetrahedron, Cube, and Octahedron.
        """
        objects = []

        # Add Tetrahedron
        objects.append(
            Tetrahedron(
                self.shaders['mesh'],
                'assets/tetrahedron.txt',
                glm.translate(glm.mat4(1.0), glm.vec3(-2.0, 0.0, 0.0))
            )
        )

        # Add Cube
        cube_vertices = self._create_cube(1.0, glm.vec3(0.8, 0.2, 0.2))  # Red cube
        objects.append(
            Mesh(
                self.shaders['mesh'],
                cube_vertices,
                glm.translate(glm.mat4(1.0), glm.vec3(0.0, 0.0, 0.0))
            )
        )

        # Add Octahedron
        octahedron_vertices = self._create_octahedron(1.0, glm.vec3(0.2, 0.8, 0.2))  # Green octahedron
        objects.append(
            Mesh(
                self.shaders['mesh'],
                octahedron_vertices,
                glm.translate(glm.mat4(1.0), glm.vec3(2.0, 0.0, 0.0))
            )
        )

        return objects

    def get_mode_2_objects(self) -> List[Renderable]:
        """
        Mode 2: Display Icosahedron with Subdivision.
        """
        objects = []

        # Add Icosahedron
        icosahedron_vertices = self._create_icosahedron(1.0, glm.vec3(0.1, 0.1, 0.8))  # Blue icosahedron
        objects.append(
            Mesh(
                self.shaders['mesh'],
                icosahedron_vertices,
                glm.translate(glm.mat4(1.0), glm.vec3(0.0, 0.0, 0.0))
            )
        )

        return objects

    def get_mode_3_objects(self) -> List[Renderable]:
        """
        Mode 3: Display Ellipsoid.
        """
        objects = []

        # Add Ellipsoid
        ellipsoid_parameters = glm.vec3(1.0, 1.5, 0.5)  # x, y, z radii
        objects.append(
            Sphere(
                self.shaders['sphere'],
                glm.vec3(0.0, 0.0, 0.0),  # Center
                1.0,  # Radius
                glm.vec3(0.5, 0.7, 1.0),  # Light blue
                glm.scale(glm.mat4(1.0), ellipsoid_parameters)
            )
        )

        return objects

    def get_mode_4_objects(self) -> List[Renderable]:
        """
        Mode 4: Display Sphere, Cylinder, and Cone with tessellation.
        """
        objects = []

        # Add Sphere
        objects.append(
            Sphere(
                self.shaders['sphere'],
                glm.vec3(-2.0, 0.0, 0.0),  # Center
                1.0,
                glm.vec3(1.0, 0.5, 0.5)  # Pink
            )
        )

        # Add Cylinder
        cylinder_vertices = self._create_cylinder(1.0, 2.0, glm.vec3(0.5, 1.0, 0.5))  # Green cylinder
        objects.append(
            Mesh(
                self.shaders['mesh'],
                cylinder_vertices,
                glm.translate(glm.mat4(1.0), glm.vec3(0.0, 0.0, 0.0))
            )
        )

        # Add Cone
        cone_vertices = self._create_cone(1.0, 2.0, glm.vec3(0.5, 0.5, 1.0))  # Blue cone
        objects.append(
            Mesh(
                self.shaders['mesh'],
                cone_vertices,
                glm.translate(glm.mat4(1.0), glm.vec3(2.0, 0.0, 0.0))
            )
        )

        return objects

    def get_mode_5_objects(self) -> List[Renderable]:
        """
        Mode 5: Display Torus with tessellation or subdivision.
        """
        objects = []

        # Add Torus
        torus_vertices = self._create_torus(1.0, 0.3, glm.vec3(0.8, 0.8, 0.0))  # Yellow torus
        objects.append(
            Mesh(
                self.shaders['mesh'],
                torus_vertices,
                glm.translate(glm.mat4(1.0), glm.vec3(0.0, 0.0, 0.0))
            )
        )

        return objects

    def get_mode_6_objects(self) -> List[Renderable]:
        """
        Mode 6: Display Super-Quadrics and Dodecahedron.
        """
        objects = []

        # Add Super-Quadrics (example: ellipsoid-like shape)
        objects.append(
            Sphere(
                self.shaders['sphere'],
                glm.vec3(-2.0, 0.0, 0.0),  # Center
                1.0,  # Radius
                glm.vec3(0.8, 0.6, 0.2)  # Brownish
            )
        )

        # Add Dodecahedron
        dodecahedron_vertices = self._create_dodecahedron(1.0, glm.vec3(0.6, 0.2, 0.8))  # Purple dodecahedron
        objects.append(
            Mesh(
                self.shaders['mesh'],
                dodecahedron_vertices,
                glm.translate(glm.mat4(1.0), glm.vec3(2.0, 0.0, 0.0))
            )
        )

        return objects

    def get_objects(self) -> List[Renderable]:
        """
        Return all objects in the current scene (used for City Scene).
        """
        return self.objects
    
    
    def get_objects(self) -> List[Renderable]:
        """Return the list of objects in the scene"""
        return self.objects 
    
    def generate_city(self, shaders: dict, grid_size: int = 10, cell_size: float = 10.0):
        """Generate a city layout using a grid pattern."""
        for x in range(grid_size):
            for z in range(grid_size):
                position = glm.vec3(x * cell_size, 0.0, z * cell_size)
                # Randomly decide what to place in each cell
                choice = random.choice(["building", "stadium", "park", "road"])

                if choice == "building":
                    self._add_random_building(shaders['mesh'], position)
                elif choice == "stadium":
                    self._add_stadium(shaders['sphere'], position)
                elif choice == "park":
                    self._add_park(shaders['mesh'], position)
                    
    import random

    def generate_city_zoning(self,grid_size: int, cell_size: float, terrain_scale: float, height_scale: float):
        """Generate a city layout with zones and terrain sampling."""
        zones = [[''] * grid_size for _ in range(grid_size)]

        for x in range(grid_size):
            for z in range(grid_size):
                zone_type = random.choices(
                    ['residential', 'commercial', 'park', 'stadium'], 
                    weights=[0.5, 0.3, 0.15, 0.05]
                )[0]
                zones[x][z] = zone_type
                position = glm.vec3(x * cell_size, 0.0, z * cell_size)
                position.y = self.sample_terrain_height(position.x, position.z, terrain_scale, height_scale)

                if zone_type == 'residential':
                   self._add_random_building(position, self.shaders['mesh'])
                elif zone_type == 'commercial':
                    self._add_random_building(position, self.shaders['mesh'], high_rise=True)
                elif zone_type == 'park':
                    self._add_park(position, self.shaders['mesh'])
                elif zone_type == 'stadium':
                    self._add_stadium(position, self.shaders['sphere'])

        return zones
    
    
    def _add_random_building(self, shader: Shader, position: glm.vec3) -> None:
        """Add a random building to the scene"""
        pass
    
    def create_icosaedron(self, radius: float, color: glm.vec3) -> glm.array:
        """Create vertices for an icosahedron"""
        pass
    
    
    def _add_stadium(self, shader: Shader, position: glm.vec3) -> None:
        """Add a stadium to the scene"""
        pass

    def _add_park(self, shader: Shader, position: glm.vec3) -> None:
        """Add a park to the scene"""
        pass
    