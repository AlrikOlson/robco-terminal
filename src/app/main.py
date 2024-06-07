import pygame
from dotenv import load_dotenv
from src.app.application import Application
from src.app.factories import ScreenFactory, FontLoaderFactory, TextRendererFactory, InputHandlerFactory
from src.app.config import Config
from src.assets.file_loader import FileLoader

def main():
    file_loader = FileLoader()
    dotenv_path = file_loader.get_path('.env')
    load_dotenv(dotenv_path)

    pygame.init()

    config = Config()
    
    screen = ScreenFactory.create_screen(config)
    font_loader = FontLoaderFactory.create_font_loader(config)
    font = font_loader.load()
    text_renderer = TextRendererFactory.create_text_renderer(screen, font)
    input_handler = InputHandlerFactory.create_input_handler()

    app = Application(screen, font_loader, text_renderer, input_handler, config)
    app.run()

    pygame.quit()

if __name__ == "__main__":
    main()
