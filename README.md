# ROBCO Termlink Emulator

![ROBCO Termlink Emulator Screenshot](screenshot.png)

As a fan of the Fallout series, I wanted to try my hand at recreating the iconic in-game terminal interface. This project is a simple attempt to capture some of the retro-style look and feel of those terminals using Python, Pygame, and OpenGL. It includes basic CRT effects and experimental AI functionality powered by models from OpenAI, Anthropic, and Meta (via NVIDIA Build).

This emulator is still a work in progress, and I've received a lot of helpful guidance from AI assistants like GPT-4 and Claude 3 Opus along the way. While it may not be perfect, I hope it provides a fun and nostalgic experience for fellow Fallout enthusiasts.

## Features

- Recreation of some elements of the Fallout terminal interface
- CRT effects for a retro look
- Basic AI-driven interactions and content generation
- YAML-based configuration for easy content management

## Installation

If you'd like to give this a try, here are the steps to set it up:

1. Clone the repository:
   ```bash
   git clone https://github.com/AlrikOlson/robco-terminal.git
   ```

2. Navigate to the project directory:
   ```bash
   cd robco-terminal
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the necessary API keys in the `.env` file:
   ```bash
   OPENAI_API_KEY=YOUR_OPENAI_API_KEY
   ANTHROPIC_API_KEY=YOUR_ANTHROPIC_API_KEY
   ```

5. Run the emulator:
   ```bash
   python src/app/main.py
   ```

## Usage

- Use the arrow keys to navigate the terminal interface
- Press Enter to select options or interact with the terminal
- Modify the configuration files to tweak the emulator's behavior and appearance

## Environment Variables

You can customize the emulator by setting these environment variables in the `.env` file:

- `OPENAI_API_KEY` (required): The API key for OpenAI's GPT models.
- `ANTHROPIC_API_KEY` (required): The API key for Anthropic's models.
- `RESPONSE_PROVIDER` (optional, default: `anthropic`): The provider for generating responses. Options include `openai`, `anthropic`, `nvidia`, and `ollama`.
- `TRACK_EVENTS_PROVIDER` (optional, default: `anthropic`): The provider for tracking narrative events. Options include `openai`, `anthropic`, and `nvidia`.
- `UPDATE_STATE_TRACKER_PROVIDER` (optional, default: `anthropic`): The provider for updating state trackers. Options include `openai`, `anthropic`, and `nvidia`.
- `UPDATE_MINDSET_PARAMETERS_PROVIDER` (optional, default: `anthropic`): The provider for updating mindset parameters. Options include `openai`, `anthropic`, and `nvidia`.
- `OLLAMA_LLAMA3_API_URL` (optional, default: `http://localhost:11434`): The URL for the Ollama LLaMA3 model API.
- `CONTEXT_FOLDER` (optional, default: `test`): The folder with context-related configuration files and narratives.

## Customization

- Adjust emulator settings in `src/app/config.py`
- Implement custom AI handlers in `src/handlers/`
- Modify terminal rendering and effects in `src/rendering/`
- Define narrative content and interactions in `src/narrative/yaml/`

## Narrative YAML System

The YAML narrative system allows for some customizable storytelling. Here's a brief overview.

### Structure of a Narrative YAML File

Each narrative YAML file consists of nodes that map out the story's flow. Here’s a simple example:

```yaml
nodes:
  start:
    content: |
      [Overseer's Log - Entry 1]
      The vault's main doors have been sealed. All residents are accounted for, and the initial orientation is underway. Today's priorities include finalizing the resource management plan and a routine inspection of the water purification system.
    options:
      - text: "[Entry 2]"
        target: entry_2
      - text: "[Resource Management Plan]"
        target: resource_management
  entry_2:
    content: |
      [Overseer's Log - Entry 2]
      Everything is going smoothly. The residents are adjusting well to their new life underground, and our engineering team resolved a minor issue with the air filtration units.
    options:
      - text: "[Entry 3]"
        target: entry_3
      - text: "[Back to Entry 1]"
        target: start
  resource_management:
    content: |
      [Resource Management Plan]
      - Food: Adequate supplies for 100 residents for 20 years
      - Water: Purification system operational
      - Energy: Reactor functioning normally
      - Medical Supplies: Stocked as per needs
    options:
      - text: "[Back to Entry 1]"
        target: start
```

### Elements of a Node

- `content`: The text to show to the player for that node.
- `options`: Choices for the player, each with:
  - `text`: The option's text.
  - `target`: The node to go to when selected.
  - `conversational` (optional): Enables conversational mode if set to `true`.

### Loading and Processing Narrative

Narratives are managed using classes derived from `BaseNarrative`. Here's a general flow:

1. **Loading from YAML**: The YAML content is parsed and loaded into nodes.
2. **Navigating Nodes**: Selecting an option updates the content to reflect the new node.

### Conversational Mode

This mode allows for dynamic, free-form text input and integrates with AI models to generate character responses. Here's a general overview:

1. **Enabling Conversational Mode**: Set this mode in the YAML file for dynamic interactions.
2. **Processing Input**: Player input is processed and sent to an AI model to generate responses.

## AI Context YAML Files

The AI context YAML files provide the necessary setup for character and setting definitions. They are located in the `src/handlers/ai_personalities` folder.

### Characters YAML File

Defines characters for AI conversations with attributes like:

- `name`: Character's name.
- `backstory`: A brief background.
- `base_emotions`: Initial emotional state.
- `triggers`: Emotional triggers.
- `coping_mechanisms`: Coping mechanisms.

### Setting YAML File

Defines the background and setting for AI interactions:

- `background`: General context and environment.
- `setting`: Specific description of the interaction setting.

## Contributing

If you’d like to contribute, here are some steps:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Commit your changes and push the branch to your fork
4. Open a pull request with a detailed description of your changes
