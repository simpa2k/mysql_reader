import re

from generators.php.PhpGenerator import PhpGenerator
from .Reader import Reader


class CreateTableReader(Reader):

    def __init__(self, path):
        super().__init__(path)

    def read(self):
        statements = []
        parsedStatements = []

        with open(self.path, 'r') as file:
                data = file.read()
                statements = data.split(';')

                self.run_threaded_reader_task(statements)
                
    def reader_task(self, statement):
        self.start_php_generator(statement)

    def match_regex(self, pattern, string):
        match = re.search(pattern, string, re.DOTALL)

        if match:
            found = match.group(1)
            return found

    def parse_statement(self, statement):
        # Removing the create table bit
        pattern = "create table\s*(.*)"
        self.statement = self.match_regex(pattern, statement)

        self.table_name = self.parse_table_name(statement)
        self.columns = self.parse_columns(statement)

    def parse_table_name(self, statement):
        return statement.split('(')[0]
    
    def parse_columns(self, statement):
        pattern = "\((.*\))"

        column_declarations = self.match_regex(pattern, statement)
        columns = column_declarations.split(',')

        for index, column in enumerate(columns):
            columns[index] = column.strip()

        self.columns = columns
        
    def start_php_generator(self, statement):
        self.parse_statement(statement)
        phpGenerator = PhpGenerator(self.table_name, False, True, True, True)

    
