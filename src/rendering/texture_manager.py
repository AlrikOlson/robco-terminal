import OpenGL.GL as gl
import pygame


class TextureManager:

    @staticmethod
    def create_texture_id(overlay):
        """
        Creates a texture ID from the overlay.

        Args:
            overlay: The overlay surface.

        Returns:
            int: The texture ID.
        """
        texture_data = pygame.image.tostring(overlay, "RGBA", True)
        texture_id = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, texture_id)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, overlay.get_width(), overlay.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, texture_data)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        return texture_id

    @staticmethod
    def bind_texture(texture_id, shader_program):
        """
        Binds the texture for rendering.

        Args:
            texture_id: The texture ID to bind.
            shader_program: The shader program.
        """
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, texture_id)
        gl.glUniform1i(gl.glGetUniformLocation(shader_program, "textureSampler"), 0)

    @staticmethod
    def cleanup(texture_id):
        """
        Cleans up by deleting the texture.

        Args:
            texture_id: The texture ID to delete.
        """
        gl.glDeleteTextures([texture_id])