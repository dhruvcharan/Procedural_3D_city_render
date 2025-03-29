#version 410 core
layout(vertices = 1) out;
uniform float tessLevelInner;
uniform float tessLevelOuter;

void main() {
    // Hardcode tessellation levels for demonstration
    gl_TessLevelOuter[0] = tessLevelOuter;
    gl_TessLevelOuter[1] = tessLevelOuter;
    gl_TessLevelOuter[2] = tessLevelOuter;
    gl_TessLevelOuter[3] = tessLevelOuter;
    gl_TessLevelInner[0] = tessLevelInner;
    gl_TessLevelInner[1] = tessLevelInner;
    
    gl_out[gl_InvocationID].gl_Position = gl_in[gl_InvocationID].gl_Position;
}