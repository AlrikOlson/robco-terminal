import os
import sys
import yaml

class FileLoader:
    def __init__(self):
        if getattr(sys, 'frozen', False):
            # Running as a bundled executable
            self.base_path = sys._MEIPASS
        else:
            # Running from source code
            self.base_path = os.path.abspath(".")

    def get_path(self, relative_path):
        return os.path.join(self.base_path, relative_path)

    def load_yaml(self, relative_path):
        yaml_path = self.get_path(relative_path)
        with open(yaml_path, 'r') as file:
            return yaml.safe_load(file)

    def load_text(self, relative_path):
        text_path = self.get_path(relative_path)
        with open(text_path, 'r') as file:
            return file.read()

    def load_binary(self, relative_path):
        binary_path = self.get_path(relative_path)
        with open(binary_path, 'rb') as file:
            return file.read()
