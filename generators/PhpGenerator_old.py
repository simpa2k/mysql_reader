from abc import ABCMeta, abstractmethod
from  .CreateTableGenerator import CreateTableGenerator

class PhpGenerator (CreateTableGenerator):

    def generate(self):
        self.generate_controller()

    def generate_controller(self):
        controller_name = self.table_name + 'Controller'
        controller_path = 'php/' + controller_name + '.php'
        
#        s = 'class {0} extends BaseController'
#        s = s.format(controller_name)
#        print(type(s))

        with open('generators/controller_template.txt', 'r') as controller_template:
            data = controller_template.read()
            data = data.format(controller_name)
            print(data)
