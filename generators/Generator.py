from abc import ABCMeta, abstractmethod

class Generator(metaclass=ABCMeta):

    def __init__(self, output_directory):
        self.output_directory = output_directory

    def convert_function_list_to_string(self, function_list):
        functions = ""

        for function in function_list:
            functions += function.retrieve()

        return functions

    @abstractmethod
    def generate(self):
        pass
