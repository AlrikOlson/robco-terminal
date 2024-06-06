from src.handlers.ai_tools.interfaces import ILLMProviderClient


class OpenAIClient(ILLMProviderClient):
    def __init__(self, client):
        self.client = client

    def create(self, model, messages, tools, tool_choice, temperature, max_tokens):
        # Check if tools are provided
        if not tools:
            return self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        return self.client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            temperature=temperature,
            max_tokens=max_tokens,
        )


class AnthropicClient(ILLMProviderClient):
    def __init__(self, client):
        self.client = client

    def create(self, model, messages, tools, tool_choice, temperature, max_tokens):
        if not tools:
            return self.client.messages.create(
                system=messages[0]["content"],
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=messages[1:],
            )
        return self.client.messages.create(
            system=messages[0]["content"],
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            tools=tools,
            messages=messages[1:],
            tool_choice=tool_choice,
        )


class NVIDIAClient(ILLMProviderClient):
    def __init__(self, client):
        self.client = client

    def create(self, model, messages, tools, tool_choice, temperature, max_tokens):
        formatted_messages = [
            {
                "role": "system",
                "content": f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>{messages[0]['content']}<|eot_id|>",
            }
        ]
        for msg in messages[1:]:
            formatted_messages.append(
                {
                    "role": msg["role"],
                    "content": f"<|start_header_id|>{msg['role']}<|end_header_id|>{msg['content']}<|eot_id|>",
                }
            )

        if not tools:
            return self.client.chat.completions.create(
                model=model,
                messages=formatted_messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=False,
            )

        return self.client.chat.completions.create(
            model=model,
            messages=formatted_messages,
            tools=tools,
            tool_choice=tool_choice,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=False,
        )
