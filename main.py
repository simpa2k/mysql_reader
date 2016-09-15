import argparse
from threading import Thread

from generators.angular.js.AngularJSAdminControllerGenerator import AngularJSAdminControllerGenerator
from generators.angular.js.AngularJSAppendCredentialsServiceGenerator import AngularJSAppendCredentialsServiceGenerator
from generators.angular.js.AngularJSFactoryGenerator import AngularJSFactoryGenerator
from generators.angular.js.AngularJSSendObjectServiceGenerator import AngularJSSendObjectServiceGenerator
from generators.php.PhpControllerGenerator import PhpControllerGenerator

from generators.php.PhpBaseControllerGenerator import PhpBaseControllerGenerator
from generators.php.PhpBaseModelGenerator import PhpBaseModelGenerator
from generators.php.PhpConfigGenerator import PhpConfigGenerator
from generators.php.PhpDBGenerator import PhpDBGenerator
from generators.php.PhpModelGenerator import PhpModelGenerator
from generators.sql.MySqlGenerator import MySqlGenerator
from readers.JsonReader import JsonReader


def generate_angular(data):
    threads = []

    for table in data:
        angular_js_factory_generator = AngularJSFactoryGenerator(table, "angular/js/services/")
        factory_thread = Thread(None, target=angular_js_factory_generator.generate)

        admin_controller_generator = AngularJSAdminControllerGenerator(table, "angular/js/controllers")
        controller_thread = Thread(None, target=admin_controller_generator.generate)

        threads.append(factory_thread)
        threads.append(controller_thread)

        factory_thread.start()
        controller_thread.start()

    send_object_service_generator = AngularJSSendObjectServiceGenerator("angular/js/services/")
    append_credentials_service_generator = AngularJSAppendCredentialsServiceGenerator("angular/js/services/")

    send_object_thread = Thread(None, target=send_object_service_generator.generate)
    append_credentials_thread = Thread(None, target=append_credentials_service_generator.generate)

    threads.append(send_object_thread)
    threads.append(append_credentials_thread)

    send_object_thread.start()
    append_credentials_thread.start()

    for thread in threads:
        thread.join()

    print("Done generating angular. Files can be found in angular/")

def generate_php(data):
    threads = []

    for table in data['tables']:
        controller_generator = PhpControllerGenerator(table, "php/classes/controllers/")
        model_generator = PhpModelGenerator(table, "php/classes/models/")

        controller_thread = Thread(None, target=controller_generator.generate)
        model_thread = Thread(None, target=model_generator.generate)

        threads.append(controller_thread)
        threads.append(model_thread)

        controller_thread.start()
        model_thread.start()

    base_controller_generator = PhpBaseControllerGenerator("php/classes/controllers/")
    base_model_generator = PhpBaseModelGenerator("php/classes/controllers/")

    base_controller_thread = Thread(None, target=base_controller_generator.generate)
    base_model_thread = Thread(None, target=base_model_generator.generate)

    threads.append(base_controller_thread)
    threads.append(base_model_thread)

    base_controller_thread.start()
    base_model_thread.start()

    if data['config'] is not None:
        config_generator = PhpConfigGenerator(data['config'], "php/core/")
        config_thread = Thread(None, target=config_generator.generate)

        threads.append(config_thread)
        config_thread.start()

    db_generator = PhpDBGenerator("php/classes/")
    db_generator_thread = Thread(None, db_generator.generate())

    threads.append(db_generator_thread)
    db_generator_thread.start()

    for thread in threads:
        thread.join()

    print("Done generating PHP. Files can be found in php/")


def generate_sql(data):
    threads = []

    for table in data:
        mySqlGenerator = MySqlGenerator(table, "mysql/")
        sql_thread = Thread(None, target=mySqlGenerator.generate)

        threads.append(sql_thread)
        sql_thread.start()

    for thread in threads:
        thread.join()

    print("Done generating sql. Files can be found in mysql/")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Path to a file that is to be read.')

    arguments = parser.parse_args()

    json_reader = JsonReader(arguments.path)
    data = json_reader.read()

    #php_thread = Thread(None, target=generate_php, args=(data,))
    #php_thread.start()

    #sql_thread = Thread(None, target=generate_sql, args=(data['tables'],))
    #sql_thread.start()

    angular_thread = Thread(None, target=generate_angular, args=(data['tables'],))
    angular_thread.start()

    #php_thread.join()
    #sql_thread.join()
    angular_thread.join()

    print("Done generating code.")


main()
