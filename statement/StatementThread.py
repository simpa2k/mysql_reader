import threading
from .CreateTableStatement import CreateTableStatement
from generators.PhpGenerator import PhpGenerator

class StatementThread (threading.Thread):

    def __init__(self, thread_id, statement):
        self.thread_id = thread_id
        self.statement = statement

    def run(self):
        create_table_statement = CreateTableStatement(self.statement)
        create_table_statement.parse_statement()

        php_generator = PhpGenerator(create_table_statement) 
        php_generator.generate()

