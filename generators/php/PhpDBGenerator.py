import os

from generators.Generator import Generator


class PhpDBGenerator(Generator):

    def generate(self):
        with open('generators/php/templates/db_template.txt') as db_template:
            data = db_template.read()

            directory = 'php/classes/'
            os.makedirs(directory, exist_ok=True)
            with open(directory + 'DB.php', 'w') as db_file:
                db_file.write(data)