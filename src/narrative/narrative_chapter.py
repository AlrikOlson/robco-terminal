# narrative_chapter.py (Updated)
from src.narrative.base_narrative import BaseNarrative

class NarrativeChapter(BaseNarrative):
    def __init__(self, yaml_content):
        super().__init__()
        self.load_from_yaml(yaml_content)

    def get_options(self):
        if not self.conversational_mode:
            options = super().get_options()
            #if "RETURN TO MAIN MENU" not in options and "BACK TO LOG" not in options:
            options.append("[Exit]")
            return options
        else:
            return []

    def load_content(self):
        self.text = [self.nodes[self.current_node]["content"]] if self.current_node else []

    def process_selection(self, selection):
        if selection == "[Exit]":
            self.conversational_mode = False  # Reset conversational mode
            self.current_node = 'start'     # Reset to start node or any other node suitable
            self.text.append("Exiting to main menu...")
        else:
            super().process_selection(selection)
