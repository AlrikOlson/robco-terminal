# Updating the process_selection method in base_narrative.py
from abc import ABC, abstractmethod
import random
import yaml
import time

from src.handlers.openai_handler import (
    generate_character_response,
    get_character_by_name,
    normalize_name,
    load_characters_data,
    EventTracker,
)

class BaseNarrative(ABC):
    def __init__(self):
        self.options = []
        self.text = []
        self.nodes = {}
        self.current_node = None
        self.conversational_mode = False
        self.conversation_histories = {}  # Initialize conversation histories

        characters = list(load_characters_data().keys())
        self.state_tracker = {
            character: {
                "location": "initial",
                "physical_state": "normal",
                "mental_state": "stable",
            }
            for character in characters
        }

        self.current_agent_name = characters[random.randint(0, len(characters) - 1)]
        self.current_agent = get_character_by_name(self.current_agent_name)

        self.event_tracker = EventTracker()

    def initialize_conversation_histories(self):
        characters = list(load_characters_data().keys())
        for character in characters:
            self.conversation_histories[character] = []

    def get_options(self):
        if self.current_node and not self.conversational_mode:
            return [
                option["text"] for option in self.nodes[self.current_node]["options"]
            ]

    def load_content(self):
        pass

    def process_selection(self, selection):
        if self.conversational_mode:
            self._handle_conversational_request({"prompt": selection})
            return

        if self.current_node:
            for option in self.nodes[self.current_node]["options"]:
                if option["text"] == selection:
                    if option.get("conversational", False):
                        self.conversational_mode = True
                        self._initiate_conversational_mode(option["target"])
                    else:
                        self.conversational_mode = False
                        self.current_node = option["target"]
                        self.text = [self.nodes[self.current_node]["content"]]
                    return
            self.text.append("Invalid selection.")

    def _initiate_conversational_mode(self, character_id):
        self.current_agent_name = character_id
        self.current_agent = get_character_by_name(self.current_agent_name)
        self.text.append(f"Initializing conversational mode with {self.current_agent.name}...")
        self.text.append(f"Connecting to {self.current_agent.name}...")
        time.sleep(1)  # Simulate delay for effect
        self.text.append(f"Connected. You can now interact with {self.current_agent.name}. Type your query:")
        self.initialize_conversation_histories()

    def _handle_conversational_request(self, openai_directive):
        prompt = openai_directive["prompt"]

        # Add the user message to the current agent's conversation history
        self.text.append(prompt)
        self.conversation_histories[self.current_agent_name].append(
            {
                "role": "user",
                "sender": "user",
                "receiver": self.current_agent.name,
                "content": prompt,
            }
        )

        # Generate agent's response using `generate_character_response`
        response, responding_character = generate_character_response(
            self.current_agent_name,
            self.conversation_histories[
                self.current_agent_name
            ],  # Use specific character's history
            self.state_tracker,
            self.event_tracker,
        )

        # Add the agent's response to the current agent's conversation history
        self.conversation_histories[self.current_agent_name].append(
            {
                "role": "assistant",
                "sender": normalize_name(responding_character),
                "receiver": "user",
                "content": response,
            }
        )

        self.text.append(response)

    def get_text(self):
        return self.text

    def load_from_yaml(self, yaml_content):
        data = yaml.safe_load(yaml_content)
        normalized_nodes = {
            normalize_name(key): value for key, value in data["nodes"].items()
        }
        self.nodes = normalized_nodes
        self.current_node = "start"
        self.text = [self.nodes[self.current_node]["content"]]

