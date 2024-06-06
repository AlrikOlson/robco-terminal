from src.scenes.bootup_scene import BootupScene
from src.scenes.login_scene import LoginScene
from src.scenes.success_scene import SuccessScene
from src.scenes.narrative_scene import NarrativeScene
from src.narrative.narrative_chapter import NarrativeChapter

class SceneFactory:
    @staticmethod
    def create_scenes(app, config):
        return {
            'bootup_scene': BootupScene(app),
            'login_scene': LoginScene(app, config.password),
            'success_scene': SuccessScene(app),
            'vault_overseer': NarrativeScene(app, SceneFactory._load_chapter('vault_overseer.yaml')),
            'research_log': NarrativeScene(app, SceneFactory._load_chapter('research_log.yaml')),
            'business_terminal': NarrativeScene(app, SceneFactory._load_chapter('business_terminal.yaml')),
        }
    
    @staticmethod
    def _load_chapter(yaml_file):
        with open(f'src/narrative/yaml/{yaml_file}', 'r') as file:
            yaml_content = file.read()
        return NarrativeChapter(yaml_content)
