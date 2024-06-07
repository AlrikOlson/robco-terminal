import pygame
from dotenv import load_dotenv
from src.app.application import Application
from src.app.factories import ScreenFactory, FontLoaderFactory, TextRendererFactory, InputHandlerFactory
from src.app.config import Config
from src.assets.file_loader import FileLoader
import tkinter as tk
from tkinter import scrolledtext
import time

def show_error_dialog(error_message):
    root = tk.Tk()
    root.title("Error")
    
    text_area = scrolledtext.ScrolledText(root, width=80, height=20)
    text_area.insert(tk.END, error_message)
    text_area.configure(state='disabled')
    text_area.pack()
    
    def on_close():
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

def main():
    try:
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

        app = Application(screen, text_renderer, input_handler, config)
        app.run()

        pygame.quit()

    except Exception as e:
        error_message = f"An error occurred: {str(e)}".replace("\\n", "\n")
        show_error_dialog(error_message)
        
        pygame.quit()
        raise e

if __name__ == "__main__":
    main()