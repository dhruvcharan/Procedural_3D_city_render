#version 410 core

layout (quads, equal_spacing, ccw) in;

out vec3 ourNormal;
out vec3 ourFragPos;
out vec3 ourColor;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

uniform vec3 center;
uniform vec3 scale; // (radius, height, 0)
uniform vec3 color;

const float PI = 3.14159265358979323846;

void main() {
    vec4 WC = gl_in[0].gl_Position;
    float u = gl_TessCoord.x;
    float v = gl_TessCoord.y;
    float theta = 2 * PI * u;
    float y = scale.y * (v - 0.5);
    vec3 pos = center + vec3(scale.x * cos(theta), y, scale.x * sin(theta));
    gl_Position = projection * view * model * vec4(pos, 1.0);
    vec3 normal = normalize(vec3(cos(theta), 0, sin(theta)));
    ourNormal = vec3((transpose(inverse(model))) * vec4(normal, 1.0f));
    ourFragPos = vec3(model * vec4(pos, 1.0));
    ourColor = color;
}   