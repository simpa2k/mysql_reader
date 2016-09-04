import os
from generators.Generator import Generator


class PhpBaseControllerGenerator(Generator):
    def generate(self):
        with open('generators/php/templates/base_controller_template.txt') as base_controller_template:
            data = base_controller_template.read()

            directory = 'php/classes/controllers/'
            os.makedirs(directory, exist_ok=True)
            with open(directory + 'BaseController.php', 'w') as base_controller_file:
                base_controller_file.write(data)
