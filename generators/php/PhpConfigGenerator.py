import os

from generators.Generator import Generator


class PhpConfigGenerator(Generator):
    def __init__(self, config, output_directory):
        super().__init__(output_directory)
        self.host = config['host']
        self.username = config['username']
        self.password = config['password']
        self.db = config['db']

    def generate(self):
        with open('generators/php/templates/config_template.txt') as config_template:
            data = config_template.read()

            directory = 'php/classes/'
            os.makedirs(directory, exist_ok=True)
            with open(directory + 'Config.php', 'w') as config_file:
                config_file.write(data)

        with open('generators/php/templates/init_template.txt') as init_template:
            data = init_template.read()
            data = data.format(host=self.host, username=self.username, password=self.password, db=self.db)

            directory = 'php/core/'
            os.makedirs(directory, exist_ok=True)
            with open(directory + 'init.php', 'w') as init_file:
                init_file.write(data)
