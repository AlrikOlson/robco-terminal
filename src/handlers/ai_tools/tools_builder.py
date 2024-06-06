# Updated tools_builder.py file with items schema for character_states parameter
from src.handlers.ai_tools.interfaces import IToolsBuilder, Tool


class ToolsBuilder(IToolsBuilder):
    def __init__(self):
        self.tools = []

    def add_tool(self, name, description):
        self.current_tool = {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        }
        return self

    def add_parameter(
        self, param_name, param_type, description, required=True, items=None
    ):
        self.current_tool["parameters"]["properties"][param_name] = {
            "type": param_type,
            "description": description,
        }
        if items and param_type == "object":
            self.current_tool["parameters"]["properties"][param_name] = items
        elif items and param_type == "array":
            self.current_tool["parameters"]["properties"][param_name]["items"] = items
        if required:
            self.current_tool["parameters"]["required"].append(param_name)
        return self

    def build_tool(self):
        self.tools.append(
            Tool(
                self.current_tool["name"],
                self.current_tool["description"],
                self.current_tool["parameters"],
            )
        )
        self.current_tool = None
        return self

    def build(self):
        return self.tools
