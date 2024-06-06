import OpenGL.GL as gl


class BezelDrawer:

    @staticmethod
    def draw_bezel(screen_width, shader_program):
        """
        Draws a bezel around the screen.

        Args:
            screen_width: The width of the screen.
            shader_program: The shader program.
        """
        bezel_color = (0.08, 0.08, 0.08, 1)  # Dark gray
        bezel_thickness = 30  # Thickness in pixels
        t = bezel_thickness / screen_width * 2
        gl.glUseProgram(shader_program)
        BezelDrawer._set_bezel_color(bezel_color, shader_program)
        BezelDrawer._draw_bezel_quads(t)
        BezelDrawer._reset_bezel_color_usage(shader_program)

    @staticmethod
    def _set_bezel_color(bezel_color, shader_program):
        """
        Sets the bezel color for drawing.

        Args:
            bezel_color: The RGBA color of the bezel.
            t: The thickness ratio of the bezel.
            shader_program: The shader program.
        """
        color_location = gl.glGetUniformLocation(shader_program, "bezelColor")
        use_bezel_color_location = gl.glGetUniformLocation(shader_program, "useBezelColor")
        gl.glUniform1i(use_bezel_color_location, 1)
        gl.glUniform4f(color_location, *bezel_color)

    @staticmethod
    def _draw_bezel_quads(t):
        """
        Draws the bezel quads around the screen.

        Args:
            t: The thickness ratio of the bezel.
        """
        gl.glBegin(gl.GL_QUADS)
        BezelDrawer._draw_top_bezel(t)
        BezelDrawer._draw_bottom_bezel(t)
        BezelDrawer._draw_left_bezel(t)
        BezelDrawer._draw_right_bezel(t)
        gl.glEnd()

    @staticmethod
    def _draw_top_bezel(t):
        """
        Draws the top bezel quad.

        Args:
            t: The thickness ratio of the bezel.
        """
        gl.glVertex2f(-1, 1)
        gl.glVertex2f(1, 1)
        gl.glVertex2f(1, 1 - t)
        gl.glVertex2f(-1, 1 - t)

    @staticmethod
    def _draw_bottom_bezel(t):
        """
        Draws the bottom bezel quad.

        Args:
            t: The thickness ratio of the bezel.
        """
        gl.glVertex2f(-1, -1)
        gl.glVertex2f(1, -1)
        gl.glVertex2f(1, -1 + t)
        gl.glVertex2f(-1, -1 + t)

    @staticmethod
    def _draw_left_bezel(t):
        """
        Draws the left bezel quad.

        Args:
            t: The thickness ratio of the bezel.
        """
        gl.glVertex2f(-1, 1)
        gl.glVertex2f(-1 + t, 1)
        gl.glVertex2f(-1 + t, -1)
        gl.glVertex2f(-1, -1)

    @staticmethod
    def _draw_right_bezel(t):
        """
        Draws the right bezel quad.

        Args:
            t: The thickness ratio of the bezel.
        """
        gl.glVertex2f(1, 1)
        gl.glVertex2f(1 - t, 1)
        gl.glVertex2f(1 - t, -1)
        gl.glVertex2f(1, -1)

    @staticmethod
    def _reset_bezel_color_usage(shader_program):
        """
        Resets the usage of bezel color.

        Args:
            shader_program: The shader program.
        """
        use_bezel_color_location = gl.glGetUniformLocation(shader_program, "useBezelColor")
        gl.glUniform1i(use_bezel_color_location, 0)