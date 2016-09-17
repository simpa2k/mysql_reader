import re


class JavaScriptVariable():

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def retrieve_definition(self):
        return self.name + " = " + self.value + ";"

    def retrieve_reference(self):

        variable_identifier = self.name

        match = re.match(".*\s(.*)", self.name)
        if match:
            variable_identifier = match.group(1)

        return variable_identifier