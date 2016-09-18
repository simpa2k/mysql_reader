import os

from formatters.MethodFormatter import MethodFormatter


class RequireJSFormatter():

    def __init__(self, input_file):
        self.input_file = input_file

    def format(self):

        with open(self.input_file, "r") as input_file:

            data = input_file.read()

            data = data.split('\n')
            tabbed_data = ""

            for line in data:
                line = '\t' + line + '\n'
                tabbed_data += line

            tabbed_data = "define(function() {{\n\n{}\n}});".format(tabbed_data)

            split_path = self.input_file.split('/')
            file_name = split_path[len(split_path) - 1]

            os.makedirs("requirejs", exist_ok=True)
            with open("requirejs/" + file_name, 'w') as output_file:
                output_file.write(tabbed_data)
