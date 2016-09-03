from abc import ABCMeta, abstractmethod

class Generator(metaclass=ABCMeta):

    def __init__(self):
        pass
    
    @abstractmethod
    def generate(self):
        pass
