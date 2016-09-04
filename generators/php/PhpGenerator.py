from abc import ABCMeta, abstractmethod
from generators.Generator import Generator

class PhpGenerator(Generator):
    
    def __init__(self, data):
        self.table_name = data['table name'] 
        self.plural = data['plural']
        self.post = data['post']
        self.put = data['put'] 
        self.delete = data['delete']
        self.primary_key = data['primary key']
        self.unimplementedMethodPlaceholder = '/*Not implemented*/'

    def construct_name(self, suffix):
        upper_case_table_name = self.table_name.capitalize()
        plural_formatted_table_name = upper_case_table_name + 's' if self.plural else upper_case_table_name
        return plural_formatted_table_name + suffix
    
    @abstractmethod
    def generate(self):
        pass
