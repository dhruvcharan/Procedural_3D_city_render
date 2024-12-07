#version 410 core


layout (quads, equal_spacing, ccw) in;

out vec3 ourNormal;
out vec3 ourFragPos;
out vec3 ourColor;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform int shapeType;  
uniform vec3 parameters; 
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
    else if (shapeType == 2) { // Cone
        float r = parameters.x * (1.0 - v);
        float h = parameters.y;
        position = vec3(
            r * cos(u),
            r * sin(u),
            h * v
        );
    }
    else if (shapeType == 3) { // Cylinder
        float r = parameters.x;
        float h = parameters.y;
        position = vec3(
            r * cos(u),
            r * sin(u),
            h * v
        );
    }
    else if (shapeType == 4) { // Torus
        float R = parameters.x; 
        float r = parameters.y; 
        position = vec3(
            (R + r * cos(v)) * cos(u),
            (R + r * cos(v)) * sin(u),
            r * sin(v)
        );
    }
    else if (shapeType == 5) { // Superquadric
        float a1 = parameters.x;
        float a2 = parameters.y;
        float a3 = parameters.z;
        float exp1 = 2.0; 
        float exp2 = 2.0; 
        float x = a1 * sign(cos(v)) * pow(abs(cos(v)), exp1) * sign(cos(u)) * pow(abs(cos(u)), exp2);
        float y = a2 * sign(cos(v)) * pow(abs(cos(v)), exp1) * sign(sin(u)) * pow(abs(sin(u)), exp2);
        float z = a3 * sign(sin(v)) * pow(abs(sin(v)), exp1);
        position = vec3(x, y, z);
    }
    
    return position;
}

vec3 calculateNormal(float u, float v) {
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
    vec4 WC = gl_in[0].gl_Position;

    vec3 position = calculatePosition(u, v);
    vec3 normal = calculateNormal(u, v);
    
    vec4 worldPos = model * vec4(position, 1.0);
    gl_Position = projection * view * worldPos;
    
    ourFragPos = vec3(worldPos);
    ourNormal = normalize(mat3(transpose(inverse(model))) * normal);
    ourColor = color;
}