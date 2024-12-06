#version 410 core

layout (quads, equal_spacing, ccw) in;

out vec3 ourNormal;
out vec3 ourFragPos;
out vec3 ourColor;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform int shapeType;  // 0: sphere, 1: ellipsoid, 2: torus, etc.
uniform vec3 parameters; // Shape-specific parameters (radii, etc.)
uniform vec3 color;

const float PI = 3.14159265359;

vec3 calculatePosition(float u, float v) {
    vec3 position;
    if (shapeType == 0) { // Sphere
        float r = parameters.x;
        position = vec3(
            r * sin(v) * cos(u),
            r * sin(v) * sin(u),
            r * cos(v)
        );
    }
    else if (shapeType == 1) { // Ellipsoid
        position = vec3(
            parameters.x * sin(v) * cos(u),
            parameters.y * sin(v) * sin(u),
            parameters.z * cos(v)
        );
    }
    else if (shapeType == 2) { // Torus
        float R = parameters.x; // Major radius
        float r = parameters.y; // Minor radius
        position = vec3(
            (R + r * cos(v)) * cos(u),
            (R + r * cos(v)) * sin(u),
            r * sin(v)
        );
    }
    return position;
}

vec3 calculateNormal(float u, float v) {
    // Calculate normal using partial derivatives
    float delta = 0.001;
    
    vec3 pos = calculatePosition(u, v);
    vec3 du = calculatePosition(u + delta, v) - pos;
    vec3 dv = calculatePosition(u, v + delta) - pos;
    
    return normalize(cross(du, dv));
}

void main()
{
    float u = 2.0 * PI * gl_TessCoord.x;
    float v = PI * gl_TessCoord.y;
    
    vec3 position = calculatePosition(u, v);
    vec3 normal = calculateNormal(u, v);
    
    // Transform position and normal
    vec4 worldPos = model * vec4(position, 1.0);
    gl_Position = projection * view * worldPos;
    
    ourFragPos = vec3(worldPos);
    ourNormal = normalize(mat3(transpose(inverse(model))) * normal);
    ourColor = color;
} 