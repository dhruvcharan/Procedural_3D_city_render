import copy

from OpenGL.GL import *
from glfw.GLFW import *
from glfw import _GLFWwindow as GLFWwindow
import glm
from scene.scene_builder import SceneBuilder
from shape.geometric_shape import GeometricShape
from .window import Window
from shape import Line, Mesh, Renderable, Sphere
from shape.tetrahedron import Tetrahedron2
from util import Camera, Shader
from util.display_mode import DisplayMode


class App(Window):
    def __init__(self):
        self.windowName: str = 'hw3'
        self.windowWidth: int = 1000
        self.windowHeight: int = 1000
        self.flight_time = 20.0
        self.flight_speed = 0.5
        self.flight_radius = 10.0
        self.flight_height = 5.0
        self.current_display_mode = DisplayMode.SMOOTH
        super().__init__(self.windowWidth, self.windowHeight, self.windowName)

        # GLFW boilerplate.
        glfwSetWindowUserPointer(self.window, self)
        glfwSetCursorPosCallback(self.window, self.__cursorPosCallback)
        glfwSetFramebufferSizeCallback(
            self.window, self.__framebufferSizeCallback)
        glfwSetKeyCallback(self.window, self.__keyCallback)
        glfwSetMouseButtonCallback(self.window, self.__mouseButtonCallback)
        glfwSetScrollCallback(self.window, self.__scrollCallback)

        # Global OpenGL pipeline settings.
        glViewport(0, 0, self.windowWidth, self.windowHeight)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glLineWidth(1.0)
        glPointSize(1.0)

        # Only for 3D scenes!
        # Also remember to clear GL_DEPTH_BUFFER_BIT, or OpenGL won't display anything...
        glEnable(GL_DEPTH_TEST)

        # Program context.

        # Shaders.
        self.lineShader: Shader = \
            Shader(vert='shader/line.vert.glsl',
                   tesc=None,
                   tese=None,
                   frag='shader/line.frag.glsl')

        self.meshShader: Shader = \
            Shader(vert='shader/mesh.vert.glsl',
                   tesc=None,
                   tese=None,
                   frag='shader/phong.frag.glsl')

        self.sphereShader: Shader = \
            Shader(vert='shader/sphere.vert.glsl',
                   tesc='shader/sphere.tesc.glsl',
                   tese='shader/sphere.tese.glsl',
                   frag='shader/phong.frag.glsl')
            
        self.torusShader: Shader = \
            Shader(vert='shader/sphere.vert.glsl',
                   tesc = 'shader/sphere.tesc.glsl',
                   tese = 'shader/torus.tese.glsl',
                   frag = 'shader/phong.frag.glsl')
            
        self.cylinderShader: Shader = \
            Shader(vert='shader/sphere.vert.glsl',
                   tesc = 'shader/sphere.tesc.glsl',
                   tese = 'shader/cylinder.tese.glsl',
                   frag = 'shader/phong.frag.glsl')
            
        self.coneShader: Shader = \
            Shader(vert='shader/sphere.vert.glsl',
                   tesc = 'shader/sphere.tesc.glsl',
                   tese = 'shader/cone.tese.glsl',
                   frag = 'shader/phong.frag.glsl')
            
        self.ellipsoidShader: Shader = \
            Shader(vert='shader/sphere.vert.glsl',
                   tesc = 'shader/sphere.tesc.glsl',
                   tese = 'shader/ellipsoid.tese.glsl',
                   frag = 'shader/phong.frag.glsl')
            
        self.super_quadric_shader: Shader = \
            Shader(vert = 'shader/sphere.vert.glsl',
                   tesc = 'shader/superquadric.tesc.glsl',
                   tese = 'shader/superquadric.tese.glsl',
                   frag = 'shader/phong.frag.glsl')
            
        self.shapes: list[Renderable] = []

        self.shapes.append(
            Line(
                self.lineShader,
                glm.array(
                    # dtype
                    glm.float32,
                    # pos (x y z)   # color (r g b)
                    0.0, 0.0, 0.0,  1.0, 0.0, 0.0,
                    3.0, 0.0, 0.0,  1.0, 0.0, 0.0,
                    0.0, 0.0, 0.0,  0.0, 1.0, 0.0,
                    0.0, 3.0, 0.0,  0.0, 1.0, 0.0,
                    0.0, 0.0, 0.0,  0.0, 0.0, 1.0,
                    0.0, 0.0, 3.0,  0.0, 0.0, 1.0,
                ),
                glm.mat4(1.0)
            )
        )

        self.shapes.append(
            Mesh(
                self.meshShader,
                glm.array(
                    # dtype
                    glm.float32,
                    # pos (x y z)        # normal (x y z)   # color (r g b)
                    -0.5,  -0.5,  0.0,   0.0, 0.0, 1.0,     1.0, 0.0, 0.0,
                    0.5,  -0.5,  0.0,   0.0, 0.0, 1.0,     0.0, 1.0, 0.0,
                    0.0,   0.5,  0.0,   0.0, 0.0, 1.0,     0.0, 0.0, 1.0,
                ),
                glm.rotate(
                    glm.translate(glm.mat4(1.0), glm.vec3(2.0, 0.0, 0.0)),
                    glm.radians(45.0), glm.vec3(0.0, 1.0, 0.0))
            )
        )

        self.shapes.append(
            Tetrahedron2(
                self.meshShader,
                'var/tetrahedron.txt',
                glm.translate(glm.mat4(1.0), glm.vec3(-2.0, 0.0, 0.0))
            )
        )

        self.shapes.append(
            Sphere(
                self.sphereShader,
                glm.vec3(0.0, 0.0, 0.0),   # center (x y z)
                1.0,                       # radius
                glm.vec3(1.0, 0.0, 0.0),  # color (r g b)
                glm.mat4(1.0)
            )
        )

        # Viewing
        self.camera: Camera = Camera(glm.vec3(0.0, 0.0, 10.0))
        self.view: glm.mat4 = glm.mat4(1.0)
        self.projection: glm.mat4 = glm.mat4(1.0)

        self.lightColor: glm.vec3 = glm.vec3(1.0, 1.0, 1.0)
        self.lightPos: glm.vec3 = glm.vec3(10.0, 10.0, 10.0)

        # Frontend GUI
        self.timeElapsedSinceLastFrame: float = 0.0
        self.lastFrameTimeStamp: float = 0.0
        self.mousePressed: bool = False
        self.mousePos: glm.dvec2 = glm.dvec2(0.0, 0.0)

        self.debugMousePos: bool = False

        # Note lastMouseLeftClickPos is different from lastMouseLeftPressPos.
        # If you press left button (and hold it there) and move the mouse,
        # lastMouseLeftPressPos gets updated to the current mouse position
        # (while lastMouseLeftClickPos, if there is one, remains the original value).
        self.lastMouseLeftClickPos: glm.dvec2 = glm.dvec2(0.0, 0.0)
        self.lastMouseLeftPressPos: glm.dvec2 = glm.dvec2(0.0, 0.0)

        self.scene_builder = SceneBuilder()
        self.scene_builder.shaders = {'sphere': self.sphereShader,
                                      'torus': self.torusShader,
                                      'cylinder': self.cylinderShader,
                                      'cone': self.coneShader,
                                      'ellipsoid': self.ellipsoidShader,
                                      'mesh': self.meshShader,
                                      'superquadric': self.super_quadric_shader}
        self.flight_mode = False
        self.flight_vertical = False

    def run(self) -> None:
        while not glfwWindowShouldClose(self.window):
            # Per-frame logic
            self.__perFrameTimeLogic(self.window)
            self.__processKeyInput(self.window)

            # Send render commands to OpenGL server
            glClearColor(0.2, 0.3, 0.3, 1.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            self.__render()

            # Check and call events and swap the buffers
            glfwSwapBuffers(self.window)
            glfwPollEvents()

    @staticmethod
    def __cursorPosCallback(window: GLFWwindow, xpos: float, ypos: float) -> None:
        app: App = glfwGetWindowUserPointer(window)

        app.mousePos.x = xpos
        app.mousePos.y = app.windowHeight - ypos

        if app.debugMousePos:
            print(f'cursor @ {app.mousePos}')

        if app.mousePressed:
            # Note: Must calculate offset first, then update lastMouseLeftPressPos.
            # Also MUST explivitly use copy here!
            # C++: copy assign is copy; Python: it's reference!
            offset: glm.dvec2 = app.mousePos - app.lastMouseLeftPressPos

            if app.debugMousePos:
                print(f'mouse drag offset {offset}')

            app.lastMouseLeftPressPos = copy.deepcopy(app.mousePos)
            app.camera.processMouseMovement(offset.x, offset.y)

    @staticmethod
    def __framebufferSizeCallback(window: GLFWwindow, width: int, height: int) -> None:
        glViewport(0, 0, width, height)

    @staticmethod
    def __keyCallback(window: GLFWwindow, key: int, scancode: int, action: int, mods: int) -> None:
        app: App = glfwGetWindowUserPointer(window)

        if action == GLFW_PRESS:
            # Check for '+' key
            if key == GLFW_KEY_EQUAL and (mods & GLFW_MOD_SHIFT):
                for shape in app.shapes:
                    if isinstance(shape, GeometricShape) or isinstance(shape, Mesh):
                        shape.subdivide()

    @staticmethod
    def __mouseButtonCallback(window: GLFWwindow, button: int, action: int, mods: int) -> None:
        app: App = glfwGetWindowUserPointer(window)

        if button == GLFW_MOUSE_BUTTON_LEFT:
            if action == GLFW_PRESS:
                app.mousePressed = True

                # NOTE: MUST explivitly use copy here!
                # C++: copy assign is copy; Python: it's reference!
                app.lastMouseLeftClickPos = copy.deepcopy(app.mousePos)
                app.lastMouseLeftPressPos = copy.deepcopy(app.mousePos)

                if app.debugMousePos:
                    print(f'mouseLeftPress @ {app.mousePos}')

            elif action == GLFW_RELEASE:
                app.mousePressed = False

                if app.debugMousePos:
                    print(f'mouseLeftRelease @ {app.mousePos}')

    @staticmethod
    def __scrollCallback(window: GLFWwindow, xoffset: float, yoffset: float) -> None:
        app: App = glfwGetWindowUserPointer(window)
        app.camera.processMouseScroll(yoffset)

    @staticmethod
    def __perFrameTimeLogic(window: GLFWwindow) -> None:
        app: App = glfwGetWindowUserPointer(window)

        currentFrame: float = glfwGetTime()
        app.timeElapsedSinceLastFrame = currentFrame - app.lastFrameTimeStamp
        app.lastFrameTimeStamp = currentFrame

    @staticmethod
    def __processKeyInput(window: GLFWwindow) -> None:
        # Camera control
        app: App = glfwGetWindowUserPointer(window)

        if glfwGetKey(window, GLFW_KEY_F1) == GLFW_PRESS:
            app.current_display_mode = DisplayMode.WIREFRAME
            
        elif glfwGetKey(window, GLFW_KEY_F2) == GLFW_PRESS:
            app.current_display_mode = DisplayMode.FLAT
        elif glfwGetKey(window, GLFW_KEY_F3) == GLFW_PRESS:
            app.current_display_mode = DisplayMode.NORMAL
        elif glfwGetKey(window, GLFW_KEY_F4) == GLFW_PRESS:
            app.current_display_mode = DisplayMode.SMOOTH

        if glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS:
            app.camera.processKeyboard(
                Camera.Movement.kLeft, app.timeElapsedSinceLastFrame)

        if glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS:
            app.camera.processKeyboard(
                Camera.Movement.kRight, app.timeElapsedSinceLastFrame)

        if glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS:
            app.camera.processKeyboard(
                Camera.Movement.kBackWard, app.timeElapsedSinceLastFrame)

        if glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS:
            app.camera.processKeyboard(
                Camera.Movement.kForward, app.timeElapsedSinceLastFrame)

        if glfwGetKey(window, GLFW_KEY_UP) == GLFW_PRESS:
            app.camera.processKeyboard(
                Camera.Movement.kUp, app.timeElapsedSinceLastFrame)

        if glfwGetKey(window, GLFW_KEY_DOWN) == GLFW_PRESS:
            app.camera.processKeyboard(
                Camera.Movement.kDown, app.timeElapsedSinceLastFrame)

        # Mode 1: Tetrahedron, Cube, Octahedron
        if glfwGetKey(window, GLFW_KEY_1) == GLFW_PRESS:
            app.shapes = app.scene_builder.get_mode_1_objects()
        elif glfwGetKey(window, GLFW_KEY_2) == GLFW_PRESS:  # Mode 2: Icosahedron
            app.shapes = app.scene_builder.get_mode_2_objects()
        elif glfwGetKey(window, GLFW_KEY_3) == GLFW_PRESS:  # Mode 3: Ellipsoid
            app.shapes = app.scene_builder.get_mode_3_objects()
        elif glfwGetKey(window, GLFW_KEY_4) == GLFW_PRESS:  # Mode 4: Sphere, Cylinder, Cone
            app.shapes = app.scene_builder.get_mode_4_objects()
        elif glfwGetKey(window, GLFW_KEY_5) == GLFW_PRESS:  # Mode 5: Torus
            app.shapes = app.scene_builder.get_mode_5_objects()
        # Mode 6: Super-Quadrics, Dodecahedron
        elif glfwGetKey(window, GLFW_KEY_6) == GLFW_PRESS:
            app.shapes = app.scene_builder.get_mode_6_objects()
        elif glfwGetKey(window, GLFW_KEY_7) == GLFW_PRESS:  # Mode 7: City Scene
            app.shapes = app.scene_builder.generate_city()
            app.flight_mode = True

        if glfwGetKey(window, GLFW_KEY_V) == GLFW_PRESS:
            app.flight_vertical = not app.flight_vertical

        if glfwGetKey(window, GLFW_KEY_LEFT_BRACKET) == GLFW_PRESS:
            app.current_display_mode = DisplayMode.WIREFRAME
        elif glfwGetKey(window, GLFW_KEY_RIGHT_BRACKET) == GLFW_PRESS:
            app.current_display_mode = DisplayMode.FLAT
        elif glfwGetKey(window, GLFW_KEY_BACKSLASH) == GLFW_PRESS:
            app.current_display_mode = DisplayMode.SMOOTH

    def __updateFlightCamera(self, deltaTime: float) -> None:
        """Update camera position for flight simulation"""
        if not self.flight_mode:
            return

        self.flight_time += deltaTime * self.flight_speed

        if self.flight_vertical:
            # Vertical circular flight
            x = self.flight_radius * glm.cos(self.flight_time)
            y = self.flight_height + self.flight_radius * \
                glm.sin(self.flight_time)
            z = 0.0

            # Calculate look-at point (always looking at center)
            self.camera.position = glm.vec3(x, y, z)
            target = glm.vec3(0.0, self.flight_height, 0.0)

        else:
            # Horizontal circular flight
            x = self.flight_radius * glm.cos(self.flight_time)
            y = self.flight_height
            z = self.flight_radius * glm.sin(self.flight_time)

            # Calculate look-at point (always looking at center)
            self.camera.position = glm.vec3(x, y, z)
            target = glm.vec3(0.0, 0.0, 0.0)

        # Update camera orientation to look at the center
        direction = glm.normalize(target - self.camera.position)
        self.camera.front = direction

        # Update camera's right and up vectors
        self.camera.right = glm.normalize(
            glm.cross(direction, glm.vec3(0.0, 1.0, 0.0)))
        self.camera.up = glm.normalize(glm.cross(self.camera.right, direction))

    def __render(self) -> None:
        t: float = self.timeElapsedSinceLastFrame

        if self.flight_mode:
            self.__updateFlightCamera(t)

        # Update shader uniforms.
        self.view = self.camera.getViewMatrix()
        self.projection = glm.perspective(glm.radians(self.camera.zoom),
                                          self.windowWidth / self.windowHeight,
                                          0.01,
                                          100.0)

        self.lineShader.use()
        self.lineShader.setMat4('view', self.view)
        self.lineShader.setMat4('projection', self.projection)

        self.meshShader.use()
        self.meshShader.setMat4('view', self.view)
        self.meshShader.setMat4('projection', self.projection)
        self.meshShader.setVec3('ViewPos', self.camera.position)
        self.meshShader.setVec3('lightPos', self.lightPos)
        self.meshShader.setVec3('lightColor', self.lightColor)
        if self.current_display_mode == DisplayMode.WIREFRAME:
            self.meshShader.setInt('shadingMode', 2)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        elif self.current_display_mode == DisplayMode.FLAT:
            self.meshShader.setInt('shadingMode', 1)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else: 
            self.meshShader.setInt('shadingMode', 0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        self.sphereShader.use()
        self.sphereShader.setMat4('view', self.view)
        self.sphereShader.setMat4('projection', self.projection)
        self.sphereShader.setVec3('ViewPos', self.camera.position)
        self.sphereShader.setVec3('lightPos', self.lightPos)
        self.sphereShader.setVec3('lightColor', self.lightColor)
        if self.current_display_mode == DisplayMode.WIREFRAME:
            self.sphereShader.setInt('shadingMode', 2)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        elif self.current_display_mode == DisplayMode.FLAT:
            self.sphereShader.setInt('shadingMode', 1)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else: 
            self.sphereShader.setInt('shadingMode', 0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            
        self.cylinderShader.use()
        self.cylinderShader.setMat4('view', self.view)
        self.cylinderShader.setMat4('projection', self.projection)
        self.cylinderShader.setVec3('ViewPos', self.camera.position)
        self.cylinderShader.setVec3('lightPos', self.lightPos)
        self.cylinderShader.setVec3('lightColor', self.lightColor)
        if self.current_display_mode == DisplayMode.WIREFRAME:
            self.cylinderShader.setInt('shadingMode', 2)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        elif self.current_display_mode == DisplayMode.FLAT:
            self.cylinderShader.setInt('shadingMode', 1)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else: 
            self.cylinderShader.setInt('shadingMode', 0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            
        self.coneShader.use()
        self.coneShader.setMat4('view', self.view)
        self.coneShader.setMat4('projection', self.projection)
        self.coneShader.setVec3('ViewPos', self.camera.position)
        self.coneShader.setVec3('lightPos', self.lightPos)
        self.coneShader.setVec3('lightColor', self.lightColor)
        if self.current_display_mode == DisplayMode.WIREFRAME:
            self.coneShader.setInt('shadingMode', 2)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        elif self.current_display_mode == DisplayMode.FLAT:
            self.coneShader.setInt('shadingMode', 1)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else: 
            self.coneShader.setInt('shadingMode', 0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            
        self.torusShader.use()
        self.torusShader.setMat4('view', self.view)
        self.torusShader.setMat4('projection', self.projection)
        self.torusShader.setVec3('ViewPos', self.camera.position)
        self.torusShader.setVec3('lightPos', self.lightPos)
        self.torusShader.setVec3('lightColor', self.lightColor)
        if self.current_display_mode == DisplayMode.WIREFRAME:
            self.torusShader.setInt('shadingMode', 2)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        elif self.current_display_mode == DisplayMode.FLAT:
            self.torusShader.setInt('shadingMode', 1)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else: 
            self.torusShader.setInt('shadingMode', 0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
        # self.coneShader.use()
        # self.coneShader.setMat4('view', self.view)
        # self.coneShader.setMat4('projection', self.projection)
        # self.coneShader.setVec3('ViewPos', self.camera.position)
        # self.coneShader.setVec3('lightPos', self.lightPos)
        # self.coneShader.setVec3('lightColor', self.lightColor)
        
        self.super_quadric_shader.use()
        self.super_quadric_shader.setMat4('view', self.view)
        self.super_quadric_shader.setMat4('projection', self.projection)
        self.super_quadric_shader.setVec3('ViewPos', self.camera.position)
        self.super_quadric_shader.setVec3('lightPos', self.lightPos)
        self.super_quadric_shader.setVec3('lightColor', self.lightColor)
        if self.current_display_mode == DisplayMode.WIREFRAME:
            self.super_quadric_shader.setInt('shadingMode', 2)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        elif self.current_display_mode == DisplayMode.FLAT:
            self.super_quadric_shader.setInt('shadingMode', 1)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            self.super_quadric_shader.setInt('shadingMode', 0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
        
        for s in self.shapes:
            s.render(t)

   