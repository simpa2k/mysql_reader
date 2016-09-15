import json

from .ForeignKey import ForeignKey
from .Reader import Reader


class JsonReader(Reader):

    def __init__(self, path):
        super().__init__(path)
        self.tables = []
        self.config = {}

        #For angular
        self.module_name = "coreModule"

    def read(self):
        with open(self.path, 'r') as config:
            raw_data = config.read()
            json_data = json.loads(raw_data)

            self.run_threaded_reader_task(json_data['tables'])
            self.read_config(json_data['config'])

            self.join_threads()

            return {"config": self.config, "tables": self.tables}

    def instantiate_foreign_keys(self, foreign_keys):
        instantiated_foreign_keys = []

        for foreign_key in foreign_keys:
            instantiated_foreign_keys.append(ForeignKey(foreign_key))

        return instantiated_foreign_keys

    def reader_task(self, table):
        table_name = table['name']

        plural = self.evaluates_to_true(table['plural'])
        post = self.evaluates_to_true(table['post'])
        put = self.evaluates_to_true(table['put'])
        delete = self.evaluates_to_true(table['delete'])
        columns = table['fields']
        primary_key = table['primary key']
        unique_key = table['unique key'] if 'unique key' in table else None
        foreign_keys = self.instantiate_foreign_keys(table['foreign key']) if 'foreign key' in table else None

        self.tables.append({
                "table name": table_name,
                "plural": plural,
                "post": post,
                "put": put,
                "delete": delete,
                "columns": columns,
                "primary key": primary_key,
                "unique key": unique_key,
                "foreign keys": foreign_keys,
                "module name": self.module_name
                })

    def read_config(self, config):
        self.config = {
            "host": config["host"],
            "username": config["username"],
            "password": config["password"],
            "db": config["db"]
        }

    


