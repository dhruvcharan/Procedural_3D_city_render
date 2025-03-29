#version 410 core

layout (quads, equal_spacing, ccw) in;

out vec3 ourNormal;
out vec3 ourFragPos;
out vec3 ourColor;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

uniform vec3 center;
uniform vec3 scale;   // (radius, height, 0)
uniform vec3 color;

const float PI = 3.14159265358979323846;

void main() {

    vec4 WC = gl_in[0].gl_Position;

    float u = gl_TessCoord.x;
    float v = gl_TessCoord.y;
    float theta = 2 * PI * u;
    vec3 pos;
    vec3 normal;
    float EPSILON = 0.000000001;
    
    if (v < EPSILON) {
        float radius = v * scale.x; // Scale v (from 0 to 1) to the radius
        pos = center + vec3(radius* cos(theta), -scale.y / 2.0, radius*sin(theta));
        normal = vec3(0.0, -1.0, 0.0); // Flat normal pointing down
    } 
    
    else {
        float r = (1.0 - v) * scale.x; // Interpolate radius from base to tip
        float y = scale.y * (v - 0.5); // Center the cone on the y-axis
        pos = center + vec3(r * cos(theta), y, r * sin(theta));
        
        vec3 tangent = vec3(-sin(theta), 0.0, cos(theta)); // Tangent along the circle's edge
        vec3 slope = vec3(0.0, scale.x / scale.y, 0.0); // Slope of the cone's side
        normal = normalize(vec3(cos(theta), scale.x / scale.y, sin(theta)));
    }
    gl_Position = projection * view * model * vec4(pos, 1.0);
    ourNormal = vec3((transpose(inverse(model))) * vec4(normal, 1.0f));
    ourFragPos = vec3(model * vec4(pos, 1.0));
    ourColor = color;
}