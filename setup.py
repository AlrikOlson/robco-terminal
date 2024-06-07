import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "pygame", "OpenGL", "numpy", "yaml"],
    "excludes": ["tkinter"],
    "include_files": [
        "src/assets",
        "src/handlers",
        "src/narrative",
        "src/rendering",
        "src/scenes",
        "src/app"
    ],
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="RobcoTerminal",
    version="0.0.3",
    description="ROBCO Termlink Emulator",
    options={"build_exe": build_exe_options},
    executables=[Executable("src/app/main.py", base=base)],
)
