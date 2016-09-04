import os
from generators.Generator import Generator


class PhpBaseModelGenerator(Generator):
    def generate(self):
        with open('generators/php/templates/base_model_template.txt') as base_model_template:
            data = base_model_template.read()

            directory = 'php/classes/models/'
            os.makedirs(directory, exist_ok=True)
            with open(directory + 'BaseModel.php', 'w') as base_model_file:
                base_model_file.write(data)
