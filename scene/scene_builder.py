import random
from typing import List
import glm
from shape import Renderable,Mesh, Sphere
from shape.cylinder import Cylinder
from shape.cone import Cone
from shape.superquadric import SuperQuadric
from shape.platonicShape import Cube, Dodecahedron, Icosahedron, Octahedron,Tetrahedron
from shape.torus import Torus
from util import Shader
import noise
class SceneBuilder:
    def __init__(self):
        self.objects: List[Renderable] = []
        self.shaders: dict = {}
        self.grid_size: int = 10
        self.cell_size: float = 15.0
        self.terrain_scale: float = 20.0
        self.height_scale: float = 5.0
        
        
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
                'var/tetrahedron.txt',
                glm.translate(glm.mat4(1.0), glm.vec3(-2.0, 0.0, 0.0)),
                color = glm.vec3(1.0, 0.25, 0.15)  # Red
            )
        )
        
        # Add Cube
        objects.append(
            Cube(
                self.shaders['mesh'],
                'var/cube.txt',
                glm.translate(glm.mat4(1.0), glm.vec3(0.0, 0.0, 0.0)),
                color = glm.vec3(0.1, .40, 0.15)  # Green
            )
        )
        
        # Add Octahedron
        
        objects.append(
            Octahedron(
                self.shaders['mesh'],
                'var/octahedron.txt',
                glm.translate(glm.mat4(1.0), glm.vec3(2.0, 0.0, 0.0)),
                color = glm.vec3(0.5, 0.5, 1.0)  # Blue
            )
        )
        return objects

    def get_mode_2_objects(self) -> List[Renderable]:
        """
        Mode 2: Display Icosahedron with Subdivision.
        """
        objects = []

        # Add Icosahedron
        objects.append(
            Icosahedron(
                self.shaders['mesh'],
                'var/icosahedron.txt',
                glm.translate(glm.mat4(1.0), glm.vec3(0.0, 0.0, 0.0)),
                color = glm.vec3(1.0, 0.5, 0.5)  # Red
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
                glm.vec3(0.0, 0.0, 0.0),  # Center
                1.0,  # Radius
                glm.vec3(0.1, 0.7, 0.1),  # Light blue
                glm.scale(glm.mat4(1.0), glm.vec3(1.0, 1.0, 1.0))
            )
        )
        
        objects.append(
            Cylinder(
                self.shaders['cylinder'],
                height = 2.0,
                radius = 0.5,
                color = glm.vec3(0.1, 0.7, 0.1),
                model = (glm.translate(glm.mat4(1.0), glm.vec3(2.0, 0.0, 0.0)))
            )
        )
        
        objects.append(
            Cone(
                self.shaders['cone'],
                height = 2.0,
                radius = 0.5,
                color = glm.vec3(0.1, 0.7, 0.1),
                model = (glm.translate(glm.mat4(1.0), glm.vec3(3.0, 0.0, 0.0))
            ))
        )
        

        
        
        return objects

    def get_mode_5_objects(self) -> List[Renderable]:
        """
        Mode 5: Display Torus with tessellation or subdivision.
        """
        objects = []
        
        objects.append(
            Torus(
                self.shaders['torus'],
                major_radius = 1.0,
                minor_radius = 0.5,
                color = glm.vec3(0.8, 0.6, 0.2)
            )
        )

        return objects

    def get_mode_6_objects(self) -> List[Renderable]:
        """
        Mode 6: Display Super-Quadrics and Dodecahedron.
        """
        objects = []
        objects.append(
            SuperQuadric(
                self.shaders['superquadric'],
                exponents = glm.vec3(0.65, .40, 0.0),
                scale = glm.vec3(2.0, 1.0, 0.5),
                color = glm.vec3(0.8, 0.6, 0.2),
                model = glm.translate(glm.mat4(1.0), glm.vec3(-4.0, -1.0, -3.0))
            )
        )

        objects.append(
            Dodecahedron(
                self.shaders['mesh'],
                'var/dodecahedron.txt',
                glm.translate(glm.mat4(1.0), glm.vec3(2.0, 0.0, 0.0)),
                color = glm.vec3(0.5, 0.5, 1.0)  
            ))

        return objects

    def get_objects(self) -> List[Renderable]:
        """
        Return all objects in the current scene (used for City Scene).
        """
        return self.objects
    
    
    
    
    
    
    def generate_terrain(self, size: int, scale: float, height_scale: float) -> glm.array:
        vertices = []
        self.height_map = [[0.0] * size for _ in range(size)]  # Shared height map for sampling
        normals = [[glm.vec3(0.0, 0.0, 0.0) for _ in range(size)] for _ in range(size)]

        for z in range(size):
            for x in range(size):
                height = noise.pnoise2(x / scale, z / scale, octaves=6, persistence=0.6, lacunarity=2.2) * height_scale
                self.height_map[z][x] = height  # Store height for later use

        for z in range(size - 1):
            for x in range(size - 1):
                # Get height from the precomputed height map
                p1 = [x * self.cell_size, self.height_map[z][x], z * self.cell_size]
                p2 = [(x + 1) * self.cell_size, self.height_map[z][x + 1], z * self.cell_size]
                p3 = [x * self.cell_size, self.height_map[z + 1][x], (z + 1) * self.cell_size]
                p4 = [(x + 1) * self.cell_size, self.height_map[z + 1][x + 1], (z + 1) * self.cell_size]

                # Color based on height
                c = [0.5, 0.35 + self.height_map[z][x] * 0.05, 0.2]
                
                # Triangle 1
                vertices.extend(p1 + [0, 1, 0] + c)
                vertices.extend(p3 + [0, 1, 0] + c)
                vertices.extend(p2 + [0, 1, 0] + c)
                
                # Triangle 2
                vertices.extend(p3 + [0, 1, 0] + c)
                vertices.extend(p4 + [0, 1, 0] + c)
                vertices.extend(p2 + [0, 1, 0] + c)

        return glm.array(glm.float32, *vertices)

    def generate_flat_terrain(self, size: int, scale: float, height_scale: float,cell_size) -> glm.array:
        vertices = []
        self.flat_height_map = [[0.0] * size for _ in range(size)]  # Shared height map for sampling
        color = glm.vec3(0.5, 0.35, 0.2)  # Brown color for the terrain
        for z in range(size - 1):
            for x in range(size - 1):
                # Four vertices for the current grid cell (each cell has 2 triangles)
                p1 = [x * cell_size, 0.0, z * cell_size]  # Bottom-left
                p2 = [(x + 1) * cell_size, 0.0, z * cell_size]  # Bottom-right
                p3 = [x * cell_size, 0.0, (z + 1) * cell_size]  # Top-left
                p4 = [(x + 1) * cell_size, 0.0, (z + 1) * cell_size]  # Top-right

                # Normals for each vertex (all pointing up for a flat terrain)
                normal = [0.0, 1.0, 0.0]

                # Color for each vertex (all vertices have the same color)
                r, g, b = color.x, color.y, color.z

                # Add two triangles per cell (p1, p3, p2) and (p3, p4, p2)
                # Triangle 1
                vertices.extend(p1 + normal + [r, g, b])  # Vertex 1
                vertices.extend(p3 + normal + [r, g, b])  # Vertex 2
                vertices.extend(p2 + normal + [r, g, b])  # Vertex 3

                # Triangle 2
                vertices.extend(p3 + normal + [r, g, b])  # Vertex 1
                vertices.extend(p4 + normal + [r, g, b])  # Vertex 2
                vertices.extend(p2 + normal + [r, g, b])  # Vertex 3

        return glm.array(glm.float32, *vertices)
                        
    
    
    def sample_terrain_height(self, x: float, z: float) -> float:
    
        grid_x = int(x // self.cell_size)
        grid_z = int(z // self.cell_size)
        
        if grid_x < 0 or grid_z < 0 or grid_x >= self.grid_size - 1 or grid_z >= self.grid_size - 1:
            return 0.0  # Out of bounds

        # Interpolate height from the four corners of the cell
        local_x = (x % self.cell_size) / self.cell_size
        local_z = (z % self.cell_size) / self.cell_size

        h1 = self.height_map[grid_z][grid_x]
        h2 = self.height_map[grid_z][grid_x + 1]
        h3 = self.height_map[grid_z + 1][grid_x]
        h4 = self.height_map[grid_z + 1][grid_x + 1]

        # Bilinear interpolation
        height_top = h1 * (1 - local_x) + h2 * local_x
        height_bottom = h3 * (1 - local_x) + h4 * local_x
        height = height_top * (1 - local_z) + height_bottom * local_z
        
        return height
    
    
    
    def generate_city_zoning(self):
        """Generate a city layout with zones and terrain sampling."""
        self.objects = []
        self.zones = [[''] * self.grid_size for _ in range(self.grid_size)]
        
        # Generate terrain with height map
        terrain_vertices = self.generate_terrain(
            size=self.grid_size, 
            scale=self.terrain_scale, 
            height_scale=self.height_scale
        )
        
        # flat_terrain_vertices = self.generate_flat_terrain(
        #     size=self.grid_size, 
        #     scale=self.terrain_scale, 
        #     height_scale=self.height_scale,
        #     cell_size=self.cell_size
        # )
       

        # Add the terrain as a mesh
        self.objects.append(
            Mesh(
                self.shaders['mesh'],
                terrain_vertices,
                glm.translate(glm.mat4(1.0), glm.vec3(0.0, 0.0, 0.0))
            )
        )
        # self.objects.append(
        #     Mesh(
        #         self.shaders['mesh'],
        #         flat_terrain_vertices,
        #         glm.translate(glm.mat4(1.0), glm.vec3(0.0, 0.0, 0.0))
        #     )
        # )
        
        # Generate city zones and objects
        for x in range(self.grid_size):
            for z in range(self.grid_size):
                # Randomly determine the type of zone
                zone_type = random.choices(
                    ['residential', 'commercial', 'park', 'stadium'], 
                    weights=[0.4, 0.3, 0.2, 0.1]
                )[0]
                self.zones[x][z] = zone_type
                
                # Sample terrain height for this grid cell
                position = glm.vec3(x * self.cell_size, 0.0, z * self.cell_size)
                # position.y = self.height_map[z][x]  # Directly read height from height_map
                position.y = self.sample_terrain_height(position.x, position.z)  # Sample accurate terrain height
                # position.y = 0.0  # Flat terrain
                # Add objects based on the zone type
                if zone_type == 'residential':
                    self._add_residential(position)
                elif zone_type == 'commercial':
                    random_high_rise = random.choice([True, False])
                    self._add_commercial(position, random_high_rise)
                elif zone_type == 'park':
                    self._add_park(position)
                elif zone_type == 'stadium':
                    self._add_stadium(position)

        return self.objects


    def _add_residential(self, position: glm.vec3) -> None:
        """Add a cluster of small houses (Cubes) at the given position."""
        block_size = int(self.cell_size // 2.5)  # Number of houses that fit into one cell
        spacing = self.cell_size / block_size 
        base_pos = position - glm.vec3((block_size-1)*spacing/2.0, 0.0, (block_size-1)*spacing/2.0)

        for i in range(block_size):
            for j in range(block_size):
                house_pos = base_pos + glm.vec3(i*spacing, 0.0, j*spacing)
                house_pos.y = self.sample_terrain_height(house_pos.x, house_pos.z)  # Sample accurate terrain height
                
                house_height = random.uniform(0.5, 1.5)
                self.objects.append(
                    Cube(
                        self.shaders['mesh'],
                        'var/cube.txt',
                        glm.translate(glm.mat4(1.0), house_pos + glm.vec3(0.0, 0.5 * house_height, 0.0)) * glm.scale(glm.mat4(1.0), glm.vec3(1.0, house_height, 1.0)),
                        color=glm.vec3(0.7, 0.6, 0.5)  # Light brown
                    ).set_shading_mode(1)
                )
                
                # Roof
                roof_height = 0.5
                roof_pos = house_pos + glm.vec3(0.0, house_height+0.5*roof_height, 0.0)
                self.objects.append(
                    Cone(
                        self.shaders['cone'],
                        height=0.5,
                        radius=0.7,
                        color=glm.vec3(0.5, 0.2, 0.1),
                        model=glm.translate(glm.mat4(1.0), roof_pos)
                    ).set_shading_mode(1)
                )


    def _add_commercial(self, position: glm.vec3, high_rise: bool = True) -> None:
        """Add a commercial building (cube or high-rise)."""
        position.y = self.sample_terrain_height(position.x, position.z)  # Sample accurate terrain height
        
        building_width = self.cell_size * 0.25
        building_height = random.uniform(0.5 * self.height_scale, 0.75 * self.height_scale)
        if high_rise:
            self.objects.append(
                Cube(
                    self.shaders['mesh'],
                    'var/cube.txt',
                    glm.translate(glm.mat4(1.0), position + glm.vec3(0.0, 0.5 * building_height, 0.0)) * glm.scale(glm.mat4(1.0), glm.vec3(building_width, building_height, building_width)),
                    color=glm.vec3(0.2, 0.2, 0.8)
                ).set_shading_mode(1)
            )

            antenna_pos = position + glm.vec3(0.0, building_height, 0.0)
            self.objects.append(
                Cylinder(
                    self.shaders['cylinder'],
                    height=2.0,
                    radius=0.1,
                    color=glm.vec3(0.2, 0.2, 0.2),
                    model=glm.translate(glm.mat4(1.0), antenna_pos)
                ).set_shading_mode(1)
            )
        else:
            building_width = self.cell_size * 0.45
            building_height = random.uniform(0.15 * self.height_scale, 0.25 * self.height_scale)
            self.objects.append(
                Cube(
                    self.shaders['mesh'],
                    'var/cube.txt',
                    glm.translate(glm.mat4(1.0), position + glm.vec3(0.0, 0.5 * building_height, 0.0)) * glm.scale(glm.mat4(1.0), glm.vec3(building_width, building_height, building_width)),
                    color=glm.vec3(0.2, 0.2, 0.2)
                ).set_shading_mode(1)
            )


    def _add_park(self, position: glm.vec3) -> None:
        """Add a park area (flat lawn) with random trees."""
        park_width = self.cell_size*0.8
        park_height = 0.1
        position.y = self.sample_terrain_height(position.x, position.z)  # Sample accurate terrain height
        # Park ground
        self.objects.append(
            Cube(
                self.shaders['mesh'],
                'var/cube.txt',
                glm.translate(glm.mat4(1.0), position + glm.vec3(0.0,0.5*park_height,0.0)) * glm.scale(glm.mat4(1.0), glm.vec3(park_width,park_height, park_width)),
                color = glm.vec3(0.1, 0.7, 0.1)  # Green lawn
            ).set_shading_mode(1)
        )

        # Add a few trees
        tree_count = random.randint(2, 5)
        for _ in range(tree_count):
            offset_x = random.uniform(-2.0, 2.0)
            offset_z = random.uniform(-2.0, 2.0)
            tree_pos = position + glm.vec3(offset_x, 0.1, offset_z)

            # Tree trunk: cylinder
            self.objects.append(
                Cylinder(
                    self.shaders['cylinder'],
                    height = 1.0,
                    radius = 0.1,
                    color = glm.vec3(0.4, 0.2, 0.1),  # Brown trunk
                    model = glm.translate(glm.mat4(1.0), tree_pos+glm.vec3(0.0, 0.5, 0.0))
                ).set_shading_mode(1)
            )
            # Tree foliage: cone on top of the trunk
            foliage_pos = tree_pos + glm.vec3(0.0, .50, 0.0)
            self.objects.append(
                Cone(
                    self.shaders['cone'],
                    height = 0.8,
                    radius = 0.5,
                    color = glm.vec3(0.0, 0.5, 0.0),  # Green foliage
                    model = glm.translate(glm.mat4(1.0), foliage_pos + glm.vec3(0.0, 0.5*0.8, 0.0))
                ).set_shading_mode(1)
            )


    def _add_stadium(self, position: glm.vec3) -> None:
        """Add a stadium with stands and a field."""
        position.y = self.sample_terrain_height(position.x, position.z)  # Sample accurate terrain height
        
        stadium_width = self.cell_size * 0.45
        stadium_model = glm.translate(glm.mat4(1.0), position+glm.vec3(0.0, 0.5, 0.0))
        stadium_model = glm.scale(stadium_model, glm.vec3(stadium_width, 1.0, stadium_width))
        stadium_model = glm.rotate(stadium_model, glm.radians(90.0), glm.vec3(1.0, 0.0, 0.0))
        
        self.objects.append(
            Torus(
                self.shaders['torus'],
                major_radius=1.0,
                minor_radius=0.3,
                color=glm.vec3(0.8, 0.8, 0.8),
                model=stadium_model
            )
        )

        field_model = glm.translate(glm.mat4(1.0), position) * glm.scale(glm.mat4(1.0), glm.vec3(stadium_width, 0.1, stadium_width))
        self.objects.append(
            Sphere(
                self.shaders['sphere'],
                center=glm.vec3(0.0, 0.0, 0.0),
                radius=1.0,
                color=glm.vec3(0.0, 0.5, 0.0),
                model=field_model
            ).set_shading_mode(1)
        )

        # # Optional: A dome (a sphere) over the stadium, semi-transparent color (if transparency is supported)
        # dome_model = glm.translate(glm.mat4(1.0), position + glm.vec3(0.0, 1.0, 0.0)) * glm.scale(glm.mat4(1.0), glm.vec3(3.0, 1.5, 3.0))
        # self.objects.append(
        #     Sphere(
        #         shader,
        #         center = glm.vec3(0.0),
        #         radius = 1.0,
        #         color = glm.vec3(0.7, 0.7, 0.9),  # Slightly bluish-white
        #         model = dome_model
        #     )
        # )    
        
    