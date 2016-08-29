from abc import ABCMeta, abstractmethod
from statement import CreateTableStatement

class Generator (metaclass=ABCMeta):

    def __init__(self, CreateTableStatement):
        self.table_name = CreateTableStatement.table_name.capitalize()
        self.columns = CreateTableStatement.columns

    @abstractmethod
    def generate(self):
        pass
