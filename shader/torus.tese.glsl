#version 410 core

layout (quads, equal_spacing, ccw) in;

out vec3 ourNormal;
out vec3 ourFragPos;
out vec3 ourColor;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

uniform vec3 center;
uniform vec2 radii; // x: major radius, y: minor radius
uniform vec3 color;

const float PI = 3.14159265358979323846;

void main()
{
    vec4 WC = gl_in[0].gl_Position;
    float u = gl_TessCoord.x;
    float v = gl_TessCoord.y;

    float phi = 2.0 * PI * u;
    float theta = 2.0 * PI * v;

    float x = (radii.x + radii.y * cos(theta)) * cos(phi);
    float y = (radii.x + radii.y * cos(theta)) * sin(phi);
    float z = radii.y * sin(theta);

    vec3 pos = center + vec3(x, y, z);
    gl_Position = projection * view * model * vec4(pos, 1.0);

    vec3 normal = normalize(vec3(
        cos(theta) * cos(phi),
        cos(theta) * sin(phi),
        sin(theta)
    ));
    ourNormal = vec3((transpose(inverse(model))) * vec4(normal, 1.0f));
    ourFragPos = vec3(model * vec4(pos, 1.0));
    ourColor = color;
}
