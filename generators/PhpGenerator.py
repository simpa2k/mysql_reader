from abc import ABCMeta, abstractmethod
from .Generator import Generator

class PhpGenerator(Generator):
    
    def __init__(self, table_name, plural, post, put, delete):

        self.table_name = table_name
        self.plural = plural
        self.post = post
        self.put = put
        self.delete = delete
        self.unimplementedMethodPlaceholder = '/*Not implemented*/'

    def construct_name(self, suffix):
        upper_case_table_name = self.table_name.capitalize()
        plural_formatted_table_name = upper_case_table_name + 's' if self.plural else upper_case_table_name
        return plural_formatted_table_name + suffix
    
    @abstractmethod
    def generate(self):
        pass
