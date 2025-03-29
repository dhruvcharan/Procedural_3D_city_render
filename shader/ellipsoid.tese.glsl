#version 410 core

layout (quads, equal_spacing, ccw) in;

out vec3 ourNormal;
out vec3 ourFragPos;
out vec3 ourColor;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

uniform vec3 center;
uniform vec3 scale; // x: radius_x, y: radius_y, z: radius_z
uniform vec3 color;

const float PI = 3.14159265358979323846;

void main()
{
    vec4 WC = gl_in[0].gl_Position;
    float u = gl_TessCoord.x;
    float v = gl_TessCoord.y;

    float phi = 2.0 * PI * u;
    float theta = PI * v;

    vec3 pos = center + vec3(
        scale.x * sin(theta) * cos(phi),
        scale.y * cos(theta),
        scale.z * sin(theta) * sin(phi)
    );
    gl_Position = projection * view * model * vec4(pos, 1.0);

    vec3 normal = normalize(vec3(
        sin(theta) * cos(phi) / scale.x,
        cos(theta) / scale.y,
        sin(theta) * sin(phi) / scale.z
    ));
    ourNormal = vec3((transpose(inverse(model))) * vec4(normal, 1.0f));
    ourFragPos = vec3(model * vec4(pos, 1.0));
    ourColor = color;
}
