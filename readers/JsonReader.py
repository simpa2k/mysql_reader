import json

from abc import ABCMeta, abstractmethod

from .Reader import Reader

from generators.MySqlGenerator import MySqlGenerator
from generators.PhpGenerator import PhpGenerator 
from generators.PhpControllerGenerator import PhpControllerGenerator 
from threading import Thread

class JsonReader(Reader):

    def __init__(self, path):
        super().__init__(path)

    def read(self):
        with open(self.path, 'r') as config:
            raw_data = config.read()
            json_data = json.loads(raw_data)

            self.run_threads(json_data['tables'])

#            for table in json_data['tables']:
#                thread = Thread(None, self.read_table(table))
#                thread.start()

    def read_table(self, table):
        self.start_mysql_generator(table)
        self.start_php_generator(table)
    
    def start_mysql_generator(self, table):
        table_name = table['name']
        columns = table['fields']
        primary_key = table['primary key']
        unique_key = table['unique key'] if 'unique key' in table else None
        foreign_key = table['foreign key'] if 'foreign key' in table else None

        mysqlGenerator = MySqlGenerator(table_name, 
                                        columns, 
                                        primary_key, 
                                        unique_key, 
                                        foreign_key)
        mysqlGenerator.generate()

    def start_php_generator(self, table):
        table_name = table['name']
        plural = self.evaluatesToTrue(table['plural'])
        post = self.evaluatesToTrue(table['post'])
        put = self.evaluatesToTrue(table['put'])
        delete = self.evaluatesToTrue(table['delete'])

#        phpGenerator = PhpGenerator(table_name,
#                                    plural,
#                                    post,
#                                    put,
#                                    delete)
#        phpGenerator.generate()
        
        phpControllerGenerator = PhpControllerGenerator(table_name,
                                                        plural,
                                                        post,
                                                        put,
                                                        delete)
        phpControllerGenerator.generate()



