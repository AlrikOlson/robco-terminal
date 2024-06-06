import OpenGL.GL as gl
import OpenGL.GL.shaders as shaders


class ShaderFactory:

    @staticmethod
    def create_curvature_shader():
        """
        Creates and compiles the curvature shader for CRT effect.

        Returns:
            shader_program: The compiled shader program.
        """
        vertex_shader = """
        #version 460 core
        in vec2 in_position;
        in vec2 in_texCoord;
        out vec2 fragTexCoord;

        void main() {
            fragTexCoord = in_texCoord;
            gl_Position = vec4(in_position, 0.0, 1.0);
        }
        """

        fragment_shader = """
        #version 460 core
        in vec2 fragTexCoord;
        out vec4 fragColor;
        uniform sampler2D textureSampler;
        uniform float curvature;
        uniform float alpha;
        uniform float glowIntensity;
        uniform float glowSize;
        uniform vec4 bezelColor;
        uniform bool useBezelColor;
        uniform float vignetteIntensity;
        uniform float colorDistortion;

        void main() {
            if (useBezelColor) {
                fragColor = bezelColor;
            } else {
                vec2 uv = fragTexCoord;
                uv -= 0.5;
                float dist = length(uv);
                uv *= 1.0 + (dist * dist * curvature);
                uv += 0.5;
                uv = clamp(uv, vec2(0.0), vec2(1.0));
                vec4 baseColor = texture(textureSampler, uv);

                // Apply vignette effect
                float vignette = smoothstep(0.8, 0.5, dist * vignetteIntensity);
                baseColor.rgb *= vignette;
                
                // Apply color distortion
                vec2 distortedUV = uv + vec2(sin(uv.y * 10.0) * colorDistortion, 0.0);
                vec4 distortedColor = texture(textureSampler, clamp(distortedUV, 0.0, 1.0));
                baseColor.rgb = mix(baseColor.rgb, distortedColor.rgb, colorDistortion);
                
                // Compute the glow effect
                vec4 glow = vec4(0.0);
                float kernel[9] = float[](
                    1.0, 2.0, 1.0,
                    2.0, 4.0, 2.0,
                    1.0, 2.0, 1.0
                );
                int glowRadius = 1;
                for (int x = -glowRadius; x <= glowRadius; x++) {
                    for (int y = -glowRadius; y <= glowRadius; y++) {
                        vec2 offset = vec2(float(x), float(y)) * glowSize / 100.0;
                        glow += texture(textureSampler, clamp(uv + offset, vec2(0.0), vec2(1.0))) * kernel[(y+1)*3 + (x+1)];
                    }
                }
                glow /= 16.0;
                
                vec3 finalColor = mix(baseColor.rgb, glow.rgb * glowIntensity, glow.a * glowIntensity);
                fragColor = vec4(finalColor, baseColor.a * alpha);
            }
        }
        """

        vertex_shader_compiled = shaders.compileShader(vertex_shader, gl.GL_VERTEX_SHADER)
        fragment_shader_compiled = shaders.compileShader(fragment_shader, gl.GL_FRAGMENT_SHADER)
        shader_program = shaders.compileProgram(vertex_shader_compiled, fragment_shader_compiled)

        gl.glUseProgram(shader_program)
        gl.glUniform1f(gl.glGetUniformLocation(shader_program, "curvature"), 0.3)
        gl.glUniform1f(gl.glGetUniformLocation(shader_program, "alpha"), 1)
        gl.glUniform1f(gl.glGetUniformLocation(shader_program, "glowIntensity"), 1.0)
        gl.glUniform1f(gl.glGetUniformLocation(shader_program, "glowSize"), 1.0)
        gl.glUniform1f(gl.glGetUniformLocation(shader_program, "vignetteIntensity"), 1.0)
        gl.glUniform1f(gl.glGetUniformLocation(shader_program, "colorDistortion"), 0.01)

        return shader_program