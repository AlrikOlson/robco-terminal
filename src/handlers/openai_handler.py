import openai
import os
import json
import requests
import yaml
import anthropic
import logging
from fuzzywuzzy import process
from abc import ABC, abstractmethod
from src.assets.file_loader import FileLoader
from src.handlers.ai_tools.tools_builder import ToolsBuilder
from src.handlers.ai_tools.tools_clients import (
    OpenAIClient,
    AnthropicClient,
    NVIDIAClient,
)
from src.handlers.ai_tools.tools_provider import LLMProviderHandler

logging.basicConfig(
    filename="robco-terminal-errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(message)s",
)

openai.api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
nvidia_api_key = os.getenv("NVIDIA_API_KEY")

NVIDIA_LLAMA3_70B_API_URL = os.getenv(
    "NVIDIA_LLAMA3_70B_API_URL", "https://integrate.api.nvidia.com/v1"
)

try:
    client_openai = OpenAIClient(openai.OpenAI())
    client_anthropic = AnthropicClient(anthropic.Anthropic(api_key=anthropic_api_key))
    client_nvidia = NVIDIAClient(
        openai.OpenAI(base_url=NVIDIA_LLAMA3_70B_API_URL, api_key=nvidia_api_key)
    )
except (openai.OpenAIError, anthropic.APIError, openai.OpenAIError):
    client_openai = None
    client_anthropic = None
    client_nvidia = None

CONTEXT_FOLDER = os.getenv("CONTEXT_FOLDER", "support")

OLLAMA_LLAMA3_API_URL = os.getenv("OLLAMA_LLAMA3_API_URL", "http://localhost:8000")
RESPONSE_PROVIDER = os.getenv("RESPONSE_PROVIDER", "anthropic")
TRACK_EVENTS_PROVIDER = os.getenv("TRACK_EVENTS_PROVIDER", "anthropic")
UPDATE_STATE_TRACKER_PROVIDER = os.getenv("UPDATE_STATE_TRACKER_PROVIDER", "anthropic")
UPDATE_MINDSET_PARAMETERS_PROVIDER = os.getenv(
    "UPDATE_MINDSET_PARAMETERS_PROVIDER", "anthropic"
)

characters_data = None

def load_characters_data():
    if not characters_data:
        file_loader = FileLoader()
        temp_characters_data = file_loader.load_yaml(f"handlers/ai_personalities/{CONTEXT_FOLDER}/characters.yaml")
        return temp_characters_data['characters']
    return characters_data['characters']


def log_llm_interaction(provider, endpoint, request_data, response_data):
    log_message = f"Provider: {provider}, Endpoint: {endpoint}, Request: {request_data}, Response: {response_data}"
    logging.info(log_message)


# Initialize provider handlers
provider_clients = {
    "openai": client_openai,
    "anthropic": client_anthropic,
    "nvidia": client_nvidia,
}
llm_handlers = {
    provider: LLMProviderHandler(client)
    for provider, client in provider_clients.items()
}


class ConversationAnalyzer:
    @staticmethod
    def analyze(
        conversation_history, state_tracker, event_tracker, involved_characters
    ):
        filtered_events = event_tracker.get_events_for_characters(involved_characters)
        messages = [
            {
                "role": "system",
                "content": "You are an observant participant in a conversation. Given the following conversation history, the current emotional states, state tracker, and event history of the individuals, provide an analysis of the emotional impact and key points of the conversation.",
            },
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "conversation_history": conversation_history,
                        "state_tracker": state_tracker,
                        "event_history": filtered_events,
                    }
                ),
            },
            {
                "role": "user",
                "content": "Please provide a concise and focused analysis of the emotional impact and key points of the conversation.",
            },
        ]

        response = client_openai.create(
            model="gpt-4o",
            messages=messages,
            tools=[],
            tool_choice="none",
            max_tokens=1000,
            temperature=0,
        )

        response_content = response.choices[0].message.content
        print("Conversation analysis:", response_content)
        return response_content


class EventTracker:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def get_events_for_characters(self, characters):
        # Filter events relevant to the provided characters
        return [
            event
            for event in self.events
            if any(char in event["characters"] for char in characters)
        ]


def get_characters_in_conversation(conversation_history):
    character_names = list(load_characters_data().keys())
    involved_characters = set()
    for msg in conversation_history:
        role = msg["role"]
        if role != "system":
            normalized_name = normalize_name(role)
            if normalized_name in map(normalize_name, character_names):
                involved_characters.add(normalized_name)
    return list(involved_characters)


class Character(ABC):
    def __init__(self, character_id, character_data):
        self.id = character_id
        self.name = character_data["name"]
        self.backstory = character_data["backstory"]
        self.base_emotions = character_data["base_emotions"]
        self.triggers = character_data["triggers"]
        self.coping_mechanisms = character_data["coping_mechanisms"]
        self.mindset = ""

    def generate_mindset(self):
        emotions = self.base_emotions
        mindset = (
            self.backstory
            + f"Your paranoia level is {emotions['paranoia']}/10, stress level is {emotions['stress']}/10, empathy level is {emotions['empathy']}/10, "
            f"confidence level is {emotions['confidence']}/10, optimism is {emotions['optimism']}/10, curiosity is {emotions['curiosity']}/10, caution level is {emotions['caution']}/10, "
            f"morale is {emotions['morale']}/10, focus is {emotions['focus']}/10, sociability level is {emotions['sociability']}/10, trust is {emotions['trust']}/10, "
            f"patience is {emotions['patience']}/10, creativity level is {emotions['creativity']}/10, resilience is {emotions['resilience']}/10, decisiveness is {emotions['decisiveness']}/10. "
            + "Keep in mind the following triggers: "
            + ", ".join(self.triggers)
            + ". "
            + "Your coping mechanisms include: "
            + ", ".join(self.coping_mechanisms)
            + "."
        )
        self.mindset = mindset
        return mindset

    def analyze_conversation(self, conversation_history, state_tracker, event_tracker):
        involved_characters = get_characters_in_conversation(conversation_history)
        return ConversationAnalyzer.analyze(
            conversation_history, state_tracker, event_tracker, involved_characters
        )

    def adjust_mindset(self, conversation_analysis, state_tracker, event_tracker):
        return adjust_mindset_helper(
            self, conversation_analysis, state_tracker, event_tracker
        )

    def generate_response(
        self,
        conversation_history,
        conversation_analysis,
        state_tracker,
        all_characters,
        event_tracker,
    ):
        return generate_response_helper(
            self,
            conversation_history,
            conversation_analysis,
            state_tracker,
            all_characters,
            event_tracker,
        )


def get_character_by_name(name):
    normalized_name = normalize_name(name)
    character_names = list(load_characters_data().keys())
    normalized_character_names = [normalize_name(c_name) for c_name in character_names]

    # Find the closest match to the normalized name
    closest_match, _ = process.extractOne(normalized_name, normalized_character_names)

    # Map back to the original names
    original_name = character_names[normalized_character_names.index(closest_match)]

    return Character(original_name, load_characters_data()[original_name])


def adjust_mindset_helper(
    character, conversation_analysis, state_tracker, event_tracker
):
    update_mindset_parameters(character, conversation_analysis, state_tracker)
    update_state_tracker(character, conversation_analysis, state_tracker)
    track_events(conversation_analysis, event_tracker)


def update_mindset_parameters(character, conversation_analysis, state_tracker):
    initial_state = character.base_emotions.copy()

    tools_builder = ToolsBuilder()
    tools_builder.add_tool(
        "update_mindset_parameters",
        "Reflect changes in mindset parameters based on the conversation history, the psychologist's assessment, "
        "the tendencies of the personality, the current emotional state of the character in question, and the state tracker. "
        f"Current character mindset: {json.dumps(character.base_emotions, indent=4)}"
        "Note: The adjustments are provided as differences rather than absolute values and are not necessarily positive or helpful, but rather realistic based on the impacts observed.",
    ).add_parameter(
        "diffs",
        "object",
        "The differences in emotional levels as a result of the conversation.",
        items={
            "type": "object",
            "properties": {
                "paranoia": {
                    "type": "number",
                    "description": "Change in paranoia level",
                },
                "stress": {"type": "number", "description": "Change in stress level"},
                "empathy": {"type": "number", "description": "Change in empathy level"},
                "confidence": {
                    "type": "number",
                    "description": "Change in confidence level",
                },
                "optimism": {
                    "type": "number",
                    "description": "Change in optimism level",
                },
                "curiosity": {
                    "type": "number",
                    "description": "Change in curiosity level",
                },
                "caution": {"type": "number", "description": "Change in caution level"},
                "morale": {"type": "number", "description": "Change in morale level"},
                "focus": {"type": "number", "description": "Change in focus level"},
                "sociability": {
                    "type": "number",
                    "description": "Change in sociability level",
                },
                "trust": {"type": "number", "description": "Change in trust level"},
                "patience": {
                    "type": "number",
                    "description": "Change in patience level",
                },
                "creativity": {
                    "type": "number",
                    "description": "Change in creativity level",
                },
                "resilience": {
                    "type": "number",
                    "description": "Change in resilience level",
                },
                "decisiveness": {
                    "type": "number",
                    "description": "Change in decisiveness level",
                },
            },
            "required": [
                "paranoia",
                "stress",
                "empathy",
                "confidence",
                "optimism",
                "curiosity",
                "caution",
                "morale",
                "focus",
                "sociability",
                "trust",
                "patience",
                "creativity",
                "resilience",
                "decisiveness",
            ],
        },
        required=True,
    ).add_parameter(
        "reason", "string", "The reason for the adjustments."
    ).build_tool()

    messages = [
        {"role": "user", "content": conversation_analysis},
    ]

    context = {
        "system_content": (
            "You are a mindset adjustment assistant. Analyze the conversation history, current emotional state, "
            "personality traits, and state tracker to provide realistic reflections on how the character's emotions and state are impacted. "
            "Provide reasons for any reflections. The adjustments should focus on reflecting the psychological impact realistically, not necessarily in a positive or helpful manner."
        ),
        "model": "gpt-4o",
        "messages": messages,
        "tool_choice": "required",
        "temperature": 0,
        "max_tokens": 500,
    }

    llm_handler = llm_handlers[UPDATE_MINDSET_PARAMETERS_PROVIDER]
    response = llm_handler.create_tool_call(tools_builder.build(), context)

    try:
        result = (
            response[0].input
            if UPDATE_MINDSET_PARAMETERS_PROVIDER == "anthropic"
            else json.loads(response[0].function.arguments)
        )
        diffs = result["diffs"]

        for key in diffs:
            change = diffs[key]
            new_value = max(
                0, min(10, character.base_emotions[key] + change)
            )  # Ensure value is between 0 and 10
            character.base_emotions[key] = new_value

        adjusted_state = character.base_emotions
        diff = {
            k: (adjusted_state[k] - initial_state[k], adjusted_state[k])
            for k in initial_state
        }
        diff_formatted = {k: f"{v[1]} ({v[0]:+d})" for k, v in diff.items()}
        print("New mindset:", json.dumps(diff_formatted, indent=4))
        print("Adjustment reason:", result["reason"])

    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"Failed to process tool call: {e}")
        # Log the error as well
        log_llm_interaction(
            UPDATE_MINDSET_PARAMETERS_PROVIDER,
            "tool_call.error",
            context,
            str(e),
        )
        raise e


def update_state_tracker(character, conversation_analysis, state_tracker):
    character_names = list(load_characters_data().keys())
    normalized_character_names = [normalize_name(c_name) for c_name in character_names]

    tools_builder = ToolsBuilder()
    tools_builder.add_tool(
        "update_state_tracker",
        "Update the state tracker based on the conversation history, the psychologist's assessment, "
        "the tendencies of the personality, and the current emotional state of the character in question. "
        "The state tracker should include detailed information about the character's current location, "
        "physical state, mental state, and any other relevant contextual information. "
        "The changes made to any state should be directly related to the actual conversation and the character's emotional state, as well as any events that have occurred.",
    ).add_parameter(
        "character_states",
        "array",
        "List of character states to update.",
        items={
            "type": "object",
            "properties": {
                "character_id": {
                    "type": "string",
                    "description": "The ID of the character.",
                },
                "location": {
                    "type": "string",
                    "description": "The current location of the character.",
                },
                "physical_state": {
                    "type": "string",
                    "description": "The current physical state of the character.",
                },
                "mental_state": {
                    "type": "string",
                    "description": "The current mental state of the character.",
                },
            },
            "required": ["character_id", "location", "physical_state", "mental_state"],
        },
        required=True,
    ).add_parameter(
        "reason", "string", "The reason for the state tracker updates."
    ).build_tool()

    messages = [
        {"role": "user", "content": conversation_analysis},
    ]

    context = {
        "system_content": (
            "You are responsible for updating the state tracker based on the conversation history, the psychologist's assessment, "
            "the tendencies of the personality, and the current emotional state of the character in question. The state tracker should include "
            "detailed information about the character's current location, physical state, mental state, and any other relevant contextual information. "
            "The changes made to any state should be directly related to the actual conversation, the character's emotional state, and any events that have occurred. "
            "Provide reasons for any state updates."
        ),
        "model": "gpt-4o",
        "messages": messages,
        "tool_choice": "required",
        "temperature": 0,
        "max_tokens": 500,
    }

    llm_handler = llm_handlers[UPDATE_STATE_TRACKER_PROVIDER]
    response = llm_handler.create_tool_call(tools_builder.build(), context)

    try:
        result = (
            response[0].input
            if UPDATE_STATE_TRACKER_PROVIDER == "anthropic"
            else json.loads(response[0].function.arguments)
        )
        character_states = result["character_states"]

        for character_state in character_states:
            matched_name, _ = process.extractOne(
                normalize_name(character_state["character_id"]),
                normalized_character_names,
            )
            original_name = character_names[
                normalized_character_names.index(matched_name)
            ]
            character_state["character_id"] = original_name

            state_tracker[original_name].update(
                {
                    "location": character_state["location"],
                    "physical_state": character_state["physical_state"],
                    "mental_state": character_state["mental_state"],
                }
            )

            print(
                f"Updated state tracker for character: {original_name}",
                json.dumps(state_tracker[original_name], indent=4),
            )
        print("Update reason:", result["reason"])

    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"Failed to process tool call: {e}")
        # Log the error as well
        log_llm_interaction(
            UPDATE_STATE_TRACKER_PROVIDER,
            "tool_call.error",
            context,
            str(e),
        )


def track_events(conversation_analysis, event_tracker):
    tools_builder = ToolsBuilder()
    tools_builder.add_tool(
        "track_events",
        "Track any events that have occurred based on the conversation history, state tracker and conversation analysis. "
        "The events should reflect meaningful occurrences that might impact the storyline or character states.",
    ).add_parameter(
        "events",
        "array",
        "List of events to track.",
        items={
            "type": "object",
            "properties": {
                "event_id": {"type": "string", "description": "The ID of the event."},
                "event_description": {
                    "type": "string",
                    "description": "A description of the event.",
                },
                "characters": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Characters involved in the event.",
                },
                "timestamp": {
                    "type": "string",
                    "description": "The timestamp of the event.",
                },
            },
            "required": ["event_id", "event_description", "characters", "timestamp"],
        },
        required=True,
    ).add_parameter(
        "reason", "string", "The reason for tracking these events."
    ).build_tool()

    messages = [
        {"role": "user", "content": conversation_analysis},
    ]

    context = {
        "system_content": (
            "You are an event tracking assistant. Analyze the conversation history, the current state of the characters, "
            "and the storyline to identify and track significant events. Your analysis should focus on the impact of these events on the characters and the overall plot."
            f"Events so far: {json.dumps(event_tracker.events, indent=4)}"
            "You should only track events that haven't been tracked yet."
        ),
        "model": "gpt-4o",
        "messages": messages,
        "tool_choice": "required",
        "temperature": 0,
        "max_tokens": 500,
    }

    llm_handler = llm_handlers[TRACK_EVENTS_PROVIDER]
    response = llm_handler.create_tool_call(tools_builder.build(), context)

    try:
        result = (
            response[0].input
            if TRACK_EVENTS_PROVIDER == "anthropic"
            else json.loads(response[0].function.arguments)
        )
        events = result["events"]

        for event in events:
            event_tracker.add_event(event)

        print("Tracked events:", json.dumps(events, indent=4))
        print("Tracking reason:", result["reason"])

    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"Failed to process tool call: {e}")
        # Log the error as well
        log_llm_interaction(
            TRACK_EVENTS_PROVIDER,
            "tool_call.error",
            context,
            str(e),
        )


def build_main_directive(
    character_name, personality_traits, current_mindset, recent_events
):
    """
    Builds a customized main directive for the language model based on the provided character attributes and context.

    Args:
        character_name (str): The name of the character.
        personality_traits (dict): A dictionary containing personality traits of the character.
        current_mindset (dict): A dictionary containing the current emotional and mental state of the character.
        recent_events (list): A list of recent events impacting the character.

    Returns:
        str: A customized main directive.
    """
    # Base directive structure
    directive = [
        "VERY IMPORTANT:",
        "1. The response should be short, with a maximum of 50 words.",
        f"2. Ensure the tone is natural, believable, and fitting {character_name}'s personality and current emotional state.",
        f"3. Use creative, uncensored language, including profanity, when it fits {character_name}'s persona.",
        "4. Responses should be proactive, suggesting new ideas or actions relevant to the storyline.",
        "5. Ensure high quality and introduce new plot elements and vivid actions.",
        "6. Include graphic descriptions within single asterisks (*) to highlight vivid actions.",
        f"7. Align all descriptions with {character_name}'s backstory, recent events, and emotional state.",
        "8. Reflect non-verbal actions, such as gestures, facial expressions, and body language, where appropriate.",
        "9. Avoid repetitive phrases or clichés.",
        "10. Ensure the response does not contradict established facts about the storyline.",
    ]

    # Additional customization based on recent events
    if recent_events:
        events_str = "Recent significant events: " + ", ".join(recent_events)
        directive.append(
            f"11. Consider the following recent events while generating the response: {events_str}"
        )

    # Compile the directive into a single string
    formatted_directive = "\n".join(directive)
    return formatted_directive


def build_system_prompt(
    character, conversation_analysis, state_tracker, event_tracker, conversation_history
):
    dynamic_mindset = character.generate_mindset()
    dynamic_mindset += f" Recent conversation analysis: {conversation_analysis}"

    # Include the states of all characters
    for char in character.all_characters:
        dynamic_mindset += f" {char.name} state: {json.dumps(state_tracker[char.id])}"

    # Include the event history
    dynamic_mindset += f" Event history: {json.dumps(event_tracker.events)}"

    dynamic_mindset += "\n\n" + get_setting_and_background()

    # Build the main directive
    main_directive = build_main_directive(
        character.name,
        character.base_emotions,
        state_tracker[character.id],
        [event["event_description"] for event in event_tracker.events],
    )
    dynamic_mindset += " " + main_directive

    formatted_messages = [
        {
            "role": msg["role"] if msg["role"] != character.name else "assistant",
            "content": msg["content"],
        }
        for msg in conversation_history
    ]

    return dynamic_mindset, formatted_messages


def generate_response_helper(
    character,
    conversation_history,
    conversation_analysis,
    state_tracker,
    all_characters,
    event_tracker,
):
    character.all_characters = all_characters
    dynamic_mindset, formatted_messages = build_system_prompt(
        character,
        conversation_analysis,
        state_tracker,
        event_tracker,
        conversation_history,
    )

    max_tokens = 200
    temperature = 0

    response_content = ""
    if RESPONSE_PROVIDER == "openai":
        response = client_openai.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": dynamic_mindset}]
            + formatted_messages,
            tools=[],
            tool_choice="none",
            max_tokens=max_tokens,
            temperature=temperature,
        )
        response_content = response.choices[0].message.content
        # Log the interaction
        log_llm_interaction(
            "openai",
            "chat.completions.create",
            {
                "messages": [{"role": "system", "content": dynamic_mindset}]
                + formatted_messages
            },
            response_content,
        )
    elif RESPONSE_PROVIDER == "anthropic":
        response = client_anthropic.create(
            model="claude-3-opus-20240229",
            messages=[{"role": "system", "content": dynamic_mindset}]
            + formatted_messages,
            tools=[],
            tool_choice="none",
            max_tokens=max_tokens,
            temperature=temperature,
        )
        response_content = response.content[0].text
        # Log the interaction
        log_llm_interaction(
            "anthropic",
            "messages.create",
            {
                "messages": [{"role": "system", "content": dynamic_mindset}]
                + formatted_messages
            },
            response_content,
        )
    elif RESPONSE_PROVIDER == "ollama":
        response = requests.post(
            OLLAMA_LLAMA3_API_URL + "/api/chat",
            json={
                "model": "llama3",
                "messages": [{"role": "system", "content": dynamic_mindset}]
                + formatted_messages,
                "options": {"num_predict": max_tokens, "temperature": temperature},
                "stream": False,
            },
        ).json()
        response_content = response["message"]["content"]
        # Log the interaction
        log_llm_interaction(
            "ollama",
            "/api/chat",
            {
                "model": "llama3",
                "messages": [{"role": "system", "content": dynamic_mindset}]
                + formatted_messages,
                "options": {"num_predict": max_tokens, "temperature": temperature},
            },
            response_content,
        )
    elif RESPONSE_PROVIDER == "nvidia":
        # Formatting system and each message according to NVIDIA's required format
        formatted_messages_nvidia = [
            {
                "role": "system",
                "content": f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>{dynamic_mindset}<|eot_id|>",
            }
        ]
        for msg in formatted_messages:
            formatted_messages_nvidia.append(
                {
                    "role": msg["role"],
                    "content": f"<|start_header_id|>{msg['role']}<|end_header_id|>{msg['content']}<|eot_id|>",
                }
            )

        response = client_nvidia.create(
            model="meta/llama3-70b-instruct",
            messages=formatted_messages_nvidia,
            tools=[],
            tool_choice="none",
            max_tokens=max_tokens,
            temperature=0.5,
        )
        response_content = response.choices[0].message.content
        # Log the interaction
        log_llm_interaction(
            "nvidia",
            "chat.completions.create",
            {"messages": formatted_messages_nvidia},
            response_content,
        )

    return response_content


def get_setting_and_background():
    file_loader = FileLoader()
    setting_data = file_loader.load_yaml(f"handlers/ai_personalities/{CONTEXT_FOLDER}/setting.yaml")
    background = setting_data["background"]
    setting = setting_data["setting"]
    return f"Background: {background}\n\nSetting: {setting}"

def normalize_name(name):
    return name.replace(" ", "_").lower()


def generate_character_response(
    initial_character_id, conversation_history, state_tracker, event_tracker
):
    normalized_initial_id = normalize_name(initial_character_id)
    conversation_analysis = ""

    selected_character = get_character_by_name(normalized_initial_id)
    selected_character_id = normalized_initial_id

    conversation_analysis = selected_character.analyze_conversation(
        conversation_history, state_tracker, event_tracker
    )

    selected_character.adjust_mindset(
        conversation_analysis, state_tracker, event_tracker
    )

    all_characters = [get_character_by_name(name) for name in load_characters_data().keys()]

    character_response = selected_character.generate_response(
        conversation_history,
        conversation_analysis,
        state_tracker,
        all_characters,
        event_tracker,
    )

    return character_response, selected_character_id
