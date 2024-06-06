import OpenGL.GL as gl
import numpy as np


import ctypes


class Renderer:

    @staticmethod
    def render_texture(shader_program):
        """
        Renders the texture using OpenGL.

        Args:
            shader_program: The shader program.
        """
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glUseProgram(shader_program)
        vertices = Renderer._create_vertices()
        vbo = Renderer._create_vbo(vertices)
        Renderer._setup_vertex_attributes(shader_program)
        Renderer._draw_vertices()
        Renderer._cleanup_vertex_attributes(vbo, shader_program)

    @staticmethod
    def _create_vertices():
        """
        Creates vertex data for a quad.

        Returns:
            np.array: Vertex data for the quad.
        """
        return np.array([
            -1, -1, 0, 0,
            1, -1, 1, 0,
            -1,  1, 0, 1,
            1,  1, 1, 1,
        ], dtype=np.float32)

    @staticmethod
    def _create_vbo(vertices):
        """
        Creates a Vertex Buffer Object (VBO) for the vertices.

        Args:
            vertices: Vertex data.

        Returns:
            int: The VBO ID.
        """
        vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_STATIC_DRAW)
        return vbo

    @staticmethod
    def _setup_vertex_attributes(shader_program):
        """
        Sets up vertex attributes for rendering.
        """
        position = gl.glGetAttribLocation(shader_program, "in_position")
        tex_coord = gl.glGetAttribLocation(shader_program, "in_texCoord")
        gl.glEnableVertexAttribArray(position)
        gl.glVertexAttribPointer(position, 2, gl.GL_FLOAT, False, 4 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(tex_coord)
        gl.glVertexAttribPointer(tex_coord, 2, gl.GL_FLOAT, False, 4 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(2 * ctypes.sizeof(ctypes.c_float)))

    @staticmethod
    def _draw_vertices():
        """
        Draws the vertices as a triangle strip.
        """
        gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, 4)

    @staticmethod
    def _cleanup_vertex_attributes(vbo, shader_program):
        """
        Cleans up vertex attributes and deletes the VBO.

        Args:
            vbo: The Vertex Buffer Object ID.
            shader_program: The shader program.
        """
        gl.glDisableVertexAttribArray(gl.glGetAttribLocation(shader_program, "in_position"))
        gl.glDisableVertexAttribArray(gl.glGetAttribLocation(shader_program, "in_texCoord"))
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glDeleteBuffers(1, [vbo])