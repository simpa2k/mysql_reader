import json
from generators.MySqlGenerator import MySqlGenerator
from generators.PhpGenerator import PhpGenerator 

with open('config.json', 'r') as config:
    raw_data = config.read()
    json_data = json.loads(raw_data)

    for table in json_data['tables']:
        mysqlGenerator = MySqlGenerator(table)
        mysqlGenerator.generate()

        phpGenerator = PhpGenerator(table)
        phpGenerator.generate()
