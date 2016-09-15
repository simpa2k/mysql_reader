from abc import ABCMeta, abstractmethod
from generators.Generator import Generator
from generators.InputBasedGenerator import InputBasedGenerator


class PhpGenerator(InputBasedGenerator):
    
    def __init__(self, data, output_directory):
        super().__init__(data, output_directory)
        self.primary_key = data['primary key']
        self.unimplementedMethodPlaceholder = '/*Not implemented*/'

    @abstractmethod
    def generate(self):
        pass
