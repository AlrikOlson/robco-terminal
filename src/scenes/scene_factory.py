from src.assets.file_loader import FileLoader
from src.scenes.bootup_scene import BootupScene
from src.scenes.login_scene import LoginScene
from src.scenes.vault_scene import VaultScene
from src.scenes.success_scene import SuccessScene
from src.scenes.narrative_scene import NarrativeScene
from src.scenes.data_logs_scene import DataLogsScene
from src.scenes.personnel_records_scene import PersonnelRecordsScene
from src.scenes.security_controls_scene import SecurityControlsScene
from src.scenes.power_management_scene import PowerManagementScene
from src.scenes.view_all_personnel_scene import ViewAllPersonnelScene
from src.scenes.search_personnel_scene import SearchPersonnelScene
from src.narrative.narrative_chapter import NarrativeChapter

class SceneFactory:
    @staticmethod
    def create_scenes(app, config):
        return {
            'bootup_scene': BootupScene(app),
            'login_scene': LoginScene(app, config.password),
            'success_scene': SuccessScene(app),
            'data_logs': DataLogsScene(app),
            'personnel_records': PersonnelRecordsScene(app),
            'security_controls': SecurityControlsScene(app),
            'power_management': PowerManagementScene(app),
            'view_all_personnel': ViewAllPersonnelScene(app),
            'search_personnel': SearchPersonnelScene(app),
            'vault_overseer': NarrativeScene(app, SceneFactory._load_chapter('vault_overseer.yaml')),
            'research_log': NarrativeScene(app, SceneFactory._load_chapter('research_log.yaml')),
            'business_terminal': NarrativeScene(app, SceneFactory._load_chapter('business_terminal.yaml')),
            'vault149_medical_terminal': NarrativeScene(app, SceneFactory._load_chapter('vault149/medical_terminal.yaml')),
            'vault149_overseer_terminal': NarrativeScene(app, SceneFactory._load_chapter('vault149/overseer_terminal.yaml')),
            'vault149_security_terminal': NarrativeScene(app, SceneFactory._load_chapter('vault149/security_terminal.yaml')),
            'vault_scene': VaultScene(app),
        }

    @staticmethod
    def _load_chapter(yaml_file):
        file_loader = FileLoader()
        yaml_content = file_loader.load_text(f'narrative/yaml/{yaml_file}')
        return NarrativeChapter(yaml_content)

