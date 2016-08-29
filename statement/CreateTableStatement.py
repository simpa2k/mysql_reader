import re

class CreateTableStatement:

    def __init__(self, statement):
        self.statement = statement

    def match_regex(self, pattern):
        match = re.search(pattern, self.statement, re.DOTALL)

        if match:
            found = match.group(1)
            return found

    def parse_statement(self):
        # Removing the create table bit
        pattern = "create table\s*(.*)"
        self.statement = self.match_regex(pattern)

        self.table_name = self.parse_table_name()
        self.columns = self.parse_columns()

    def parse_table_name(self):
        return self.statement.split('(')[0]
    
    def parse_columns(self):
        pattern = "\((.*\))"

        column_declarations = self.match_regex(pattern)
        columns = column_declarations.split(',')

        for index, column in enumerate(columns):
            columns[index] = column.strip()

        self.columns = columns
    
