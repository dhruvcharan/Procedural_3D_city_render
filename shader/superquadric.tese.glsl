#version 410 core

layout (quads, equal_spacing, ccw) in;

out vec3 ourNormal;
out vec3 ourFragPos;
out vec3 ourColor;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

uniform vec3 center;
uniform vec3 color;
uniform vec3 exponents; // e1,e2, 0
uniform vec3 scale;

const float PI = 3.14159265358979323846;

float safepow(float base, float exp) {
    float magnitude = abs(base);
    float powered = pow(magnitude, exp);
    return (base < 0.0) ? -powered : powered;
}

void main() {
    float u = gl_TessCoord.x * PI - PI / 2.0;
    float v = gl_TessCoord.y * 2.0 * PI;

    float e1 = exponents.x;
    float e2 = exponents.y;

    float x = safepow(cos(u), e1) * safepow(cos(v), e2);
    float y = safepow(cos(u), e1) * safepow(sin(v), e2);
    float z = safepow(sin(u), e1);
    vec3 pos = vec3(scale.x * x, scale.y * y, scale.z * z);
    gl_Position = projection * view * model * vec4(pos, 1.0);
    ourColor = color;
    
    ourNormal = normalize(vec3((transpose(inverse(model))) * vec4(normalize(pos), 0.0)));
    ourFragPos = vec3(model * vec4(pos, 1.0));
}