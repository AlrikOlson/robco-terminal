import OpenGL.GL as gl


class OpenGLInitializer:

    def initialize(self):
        """
        Initializes basic OpenGL settings.
        """
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)