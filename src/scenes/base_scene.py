import abc

class BaseScene(abc.ABC):
    def __init__(self, app):
        self.app = app

    @abc.abstractmethod
    def handle_event(self, event):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def render(self):
        pass