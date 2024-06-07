import OpenGL.GL as gl
import numpy as np
import ctypes


class Renderer:

    @staticmethod
    def render_texture(shader_program, time, width, height):
        bloom_fbo, bloom_texture = Renderer.create_fbo(width, height)

        # First pass: render the scene to the bloom FBO
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, bloom_fbo)
        gl.glViewport(0, 0, width, height)  # Set viewport to FBO size
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glUseProgram(shader_program)
        bloom_threshold_location = gl.glGetUniformLocation(shader_program, "BloomThreshold")
        gl.glUniform1f(bloom_threshold_location, 1)  # Adjust the threshold as needed
        Renderer._render_scene(shader_program, time)

        # Second pass: blur the bloom texture and combine with the original scene
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
        gl.glViewport(0, 0, width, height)  # Set viewport to screen size
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glUseProgram(shader_program)
        bloom_texture_location = gl.glGetUniformLocation(shader_program, "BloomTexture")
        gl.glActiveTexture(gl.GL_TEXTURE1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, bloom_texture)
        gl.glUniform1i(bloom_texture_location, 1)
        Renderer._render_scene(shader_program, time)

        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
        gl.glDeleteFramebuffers(1, [bloom_fbo])
        gl.glDeleteTextures([bloom_texture])


    @staticmethod
    def _render_scene(shader_program, time):
        # Set the time uniform
        time_uniform_location = gl.glGetUniformLocation(shader_program, "Time")
        gl.glUniform1f(time_uniform_location, time)

        vertices = Renderer._create_vertices()
        vbo = Renderer._create_vbo(vertices)
        Renderer._setup_vertex_attributes(shader_program)
        Renderer._draw_vertices()
        Renderer._cleanup_vertex_attributes(vbo, shader_program)

    @staticmethod
    def create_fbo(width, height):
        fbo = gl.glGenFramebuffers(1)
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, fbo)

        texture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, width, height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, None)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT0, gl.GL_TEXTURE_2D, texture, 0)

        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

        return fbo, texture

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
