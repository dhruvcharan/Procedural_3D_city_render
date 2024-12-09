#version 410

layout (vertices = 1) out;

uniform float tess_level_inner;
uniform float tess_level_outer;

void main()
{
    gl_TessLevelOuter[0] = tess_level_outer;
    gl_TessLevelOuter[1] = tess_level_outer;
    gl_TessLevelOuter[2] = tess_level_outer;
    gl_TessLevelOuter[3] = tess_level_outer;

    gl_TessLevelInner[0] = tess_level_inner;
    gl_TessLevelInner[1] = tess_level_inner;  

    gl_out[gl_InvocationID].gl_Position = gl_in[gl_InvocationID].gl_Position;
}



