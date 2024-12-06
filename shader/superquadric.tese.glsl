#version 410 core

layout (quads, equal_spacing, ccw) in;

out vec3 ourNormal;
out vec3 ourFragPos;
out vec3 ourColor;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform vec2 exponents;  // e1, e2 parameters
uniform vec3 color;

const float PI = 3.14159265359;

float sign(float x) {
    return x >= 0.0 ? 1.0 : -1.0;
}

float supercos(float w, float m) {
    return sign(cos(w)) * pow(abs(cos(w)), m);
}

float supersin(float w, float m) {
    return sign(sin(w)) * pow(abs(sin(w)), m);
}

vec3 calculatePosition(float eta, float omega) {
    float e1 = exponents.x;
    float e2 = exponents.y;
    
    return vec3(
        supercos(eta, 2.0/e1) * supercos(omega, 2.0/e2),
        supercos(eta, 2.0/e1) * supersin(omega, 2.0/e2),
        supersin(eta, 2.0/e1)
    );
}

vec3 calculateNormal(float eta, float omega) {
    float e1 = exponents.x;
    float e2 = exponents.y;
    
    return normalize(vec3(
        (2.0/e1) * supercos(eta, 2.0-e1) * supercos(omega, 2.0-e2),
        (2.0/e1) * supercos(eta, 2.0-e1) * supersin(omega, 2.0-e2),
        (2.0/e2) * supersin(eta, 2.0-e2)
    ));
}

void main()
{
    float eta = PI * (gl_TessCoord.x - 0.5);
    float omega = 2.0 * PI * gl_TessCoord.y;
    
    vec3 position = calculatePosition(eta, omega);
    vec3 normal = calculateNormal(eta, omega);
    
    vec4 worldPos = model * vec4(position, 1.0);
    gl_Position = projection * view * worldPos;
    
    ourFragPos = vec3(worldPos);
    ourNormal = normalize(mat3(transpose(inverse(model))) * normal);
    ourColor = color;
} 