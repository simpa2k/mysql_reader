import os

from formatters.MethodFormatter import MethodFormatter


class RequireJSFormatter():

    def __init__(self, input):
        self.input = input

    def format(self):

        split_input = self.input.split('\n')
        tabbed_input = ""

        for line in split_input:
            line = '\t' + line + '\n'
            tabbed_input += line

        require_js_function = "define(function() {{\n\n{}\n}});".format(tabbed_input)
        return require_js_function

        #with open(self.input, "r") as input_file:

            #data = input_file.read()

            #data = data.split('\n')
            #tabbed_data = ""

            #for line in data:
            #    line = '\t' + line + '\n'
            #    tabbed_data += line

            #tabbed_data = "define(function() {{\n\n{}\n}});".format(tabbed_data)

            #split_path = self.input_file.split('/')
            #file_name = split_path[len(split_path) - 1]

            #os.makedirs(self.output_directory, exist_ok=True)
            #with open(self.output_directory + file_name, 'w') as output_file:
            #    output_file.write(tabbed_data)
