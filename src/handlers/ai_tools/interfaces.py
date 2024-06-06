from abc import ABC, abstractmethod
import logging
import json

class Tool:
    def __init__(self, name, description, parameters):
        self.name = name
        self.description = description
        self.parameters = parameters


class IToolsBuilder(ABC):
    @abstractmethod
    def add_tool(self, name, description):
        pass

    @abstractmethod
    def add_parameter(self, param_name, param_type, description, required=True):
        pass

    @abstractmethod
    def build_tool(self):
        pass

    @abstractmethod
    def build(self):
        pass


class ILLMProviderClient(ABC):
    @abstractmethod
    def create(self, model, messages, tools, tool_choice, temperature, max_tokens):
        pass


class ILLMProviderHandler(ABC):
    @abstractmethod
    def create_tool_call(self, common_tool_schema, context):
        pass
