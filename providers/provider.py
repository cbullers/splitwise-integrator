from abc import ABC, abstractmethod
from datetime import datetime

class Provider(ABC):

    @abstractmethod
    def get_current_cost(self):
        pass

    def get_description(self):
        # Return date as MM/YYYY
        return " | " + datetime.now().strftime("%m/%Y")

    def __init__(self, config):
        self.config = config