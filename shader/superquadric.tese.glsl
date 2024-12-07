#version 410 core

layout (quads, equal_spacing, ccw) in;

out vec3 ourNormal;
out vec3 ourFragPos;
out vec3 ourColor;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

uniform vec3 center;
uniform vec3 scale;
uniform float e1;
uniform float e2;
uniform vec3 color;

const float PI = 3.14159265358979323846;

float sgn(float x) {
    return (x < 0.0) ? -1.0 : 1.0;
}

float superquadric(float angle, float exponent) {
    return sgn(sin(angle)) * pow(abs(sin(angle)), exponent);
}

void main()
{
    vec4 WC = gl_in[0].gl_Position;

    float u = gl_TessCoord.x;
    float v = gl_TessCoord.y;

    float phi = 2.0 * PI * u;
    float theta = PI * v;

    vec3 pos = center + scale * vec3(
        superquadric(phi, e2) * superquadric(theta, e1),
        superquadric(phi, e2) * superquadric(theta, e1),
        superquadric(theta, e1)
    );

    gl_Position = projection * view * model * vec4(pos, 1.0);

    ourFragPos = vec3(model * vec4(pos, 1.0));
    ourNormal = normalize(vec3(transpose(inverse(model)) * vec4(pos, 1.0)));
    ourColor = color;
}
