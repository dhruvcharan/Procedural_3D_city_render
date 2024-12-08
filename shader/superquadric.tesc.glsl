#version 410 core
layout(vertices = 1) out;

void main() {
    // Hardcode tessellation levels for demonstration
    gl_TessLevelOuter[0] = 64.0;
    gl_TessLevelOuter[1] = 64.0;
    gl_TessLevelOuter[2] = 64.0;
    gl_TessLevelOuter[3] = 64.0;
    gl_TessLevelInner[0] = 64.0;
    gl_TessLevelInner[1] = 64.0;
    
    gl_out[gl_InvocationID].gl_Position = gl_in[gl_InvocationID].gl_Position;
}