from abc import ABCMeta, abstractmethod
from statement import CreateTableStatement

class CreateTableGenerator (metaclass=ABCMeta):

    def __init__(self, CreateTableStatement):
        self.table_name = CreateTableStatement.table_name.capitalize()
        self.columns = CreateTableStatement.columns

    @abstractmethod
    def generate(self):
        pass
