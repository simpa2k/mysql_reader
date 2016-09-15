from abc import ABCMeta, abstractmethod

class Generator(metaclass=ABCMeta):

    def __init__(self, output_directory):
        self.output_directory = output_directory

    @abstractmethod
    def generate(self):
        pass
