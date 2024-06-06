import logging
from src.handlers.ai_tools.interfaces import ILLMProviderClient, ILLMProviderHandler
from src.handlers.ai_tools.tools_clients import AnthropicClient, NVIDIAClient, OpenAIClient


class LLMProviderHandler(ILLMProviderHandler):
    def __init__(self, client: ILLMProviderClient):
        self.client = client

    def log_interaction(self, endpoint, request_data, response_data):
        log_message = f"Provider: {self.client.__class__.__name__}, Endpoint: {endpoint}, Request: {request_data}, Response: {response_data}"
        logging.info(log_message)

    def map_tool_schema(self, common_tool_schema):
        if isinstance(self.client, OpenAIClient):
            return [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.parameters,
                    },
                }
                for tool in common_tool_schema
            ]
        elif isinstance(self.client, AnthropicClient):
            return [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.parameters,
                }
                for tool in common_tool_schema
            ]
        elif isinstance(self.client, NVIDIAClient):
            return [
                {
                    "role": "system",
                    "content": f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>{tool.description}<|eot_id|>",
                }
                for tool in common_tool_schema
            ]
        else:
            raise ValueError(f"Unsupported provider: {self.client}")

    def create_tool_call(self, common_tool_schema, context):
        tool_schema = self.map_tool_schema(common_tool_schema)
        system_content = context["system_content"]
        messages = context["messages"]

        response = self.client.create(
            model=context["model"],
            messages=[{"role": "system", "content": system_content}] + messages,
            tools=tool_schema,
            tool_choice=context["tool_choice"],
            temperature=context["temperature"],
            max_tokens=context["max_tokens"],
        )

        self.log_interaction("create", {"messages": [{"role": "system", "content": system_content}] + messages}, response)

        return response.choices[0].message.tool_calls if isinstance(self.client, OpenAIClient) else response.content
