from abc import ABCMeta, abstractmethod

class JsonGenerator(metaclass=ABCMeta):

    def __init__(self, json):
        self.json = json

    @abstractmethod
    def generate(self):
        pass
