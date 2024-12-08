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
const float EPSILON = 0.000000001;

void main() {
    vec4 WC = gl_in[0].gl_Position;
    float u = gl_TessCoord.x;
    float v = gl_TessCoord.y;
    vec3 pos;
    vec3 normal;
    float theta = 2 * PI * u;

    if (gl_TessCoord.y < EPSILON) {
        pos = center + vec3(v*scale.x * cos(theta), -scale.y/2.0, v*scale.x * sin(theta));
        normal = vec3(0.0, -1.0, 0.0);
    } else if (abs(gl_TessCoord.y - 1.0) < EPSILON) {
            float r = (1-v) * scale.x;
            float theta = 2 * PI * u;
            pos = center + vec3(r * cos(theta), scale.y/2.0, r * sin(theta));
            normal = vec3(0.0, 1.0, 0.0);
    } else {
        float y = scale.y*(v-0.5);
        pos = center + vec3(scale.x * cos(theta), y, scale.x * sin(theta));
        normal = normalize(vec3(cos(theta), 0.0, sin(theta)));
    }


    gl_Position = projection * view * model * vec4(pos, 1.0);
    ourNormal = vec3((transpose(inverse(model))) * vec4(normal, 0.0f));
    ourFragPos = vec3(model * vec4(pos, 1.0));
    ourColor = color;
}   