from abc import ABC, abstractmethod

class Tab(ABC):


    def __init__(self, app, window, backend) -> None:
        self.app = app
        self.window = window
        self.backend = backend

        self.set_interaction_logic()

    @abstractmethod
    def set_interaction_logic(self):
        pass


