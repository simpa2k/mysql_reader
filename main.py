import argparse
import os
from threading import Thread

from pathlib import Path

from generators.angular.js.AngularJSAdminControllerGenerator import AngularJSAdminControllerGenerator
from generators.angular.js.AngularJSAppendCredentialsServiceGenerator import AngularJSAppendCredentialsServiceGenerator
from generators.angular.js.AngularJSFactoryGenerator import AngularJSFactoryGenerator
from generators.angular.js.AngularJSMainControllerGenerator import AngularJSMainControllerGenerator
from generators.angular.js.AngularJSSendObjectServiceGenerator import AngularJSSendObjectServiceGenerator
from generators.php.PhpControllerGenerator import PhpControllerGenerator

from generators.php.PhpBaseControllerGenerator import PhpBaseControllerGenerator
from generators.php.PhpBaseModelGenerator import PhpBaseModelGenerator
from generators.php.PhpConfigGenerator import PhpConfigGenerator
from generators.php.PhpDBGenerator import PhpDBGenerator
from generators.php.PhpHardCodedFileGenerator import PhpHardCodedFileGenerator
from generators.php.PhpModelGenerator import PhpModelGenerator
from generators.sql.MySqlGenerator import MySqlGenerator
from readers.JsonReader import JsonReader


def generate_angular(data, output_path):
    threads = []

    for table in data:
        angular_js_factory_generator = AngularJSFactoryGenerator(table, output_path + "services/")
        factory_thread = Thread(None, target=angular_js_factory_generator.generate)

        admin_controller_generator = AngularJSAdminControllerGenerator(table, output_path + "controllers/")
        controller_thread = Thread(None, target=admin_controller_generator.generate)

        threads.append(factory_thread)
        threads.append(controller_thread)

        factory_thread.start()
        controller_thread.start()

    send_object_service_generator = AngularJSSendObjectServiceGenerator(output_path + "services/")
    append_credentials_service_generator = AngularJSAppendCredentialsServiceGenerator(output_path + "services/")
    main_controller_generator = AngularJSMainControllerGenerator(data, output_path + "controllers/")

    send_object_thread = Thread(None, target=send_object_service_generator.generate)
    append_credentials_thread = Thread(None, target=append_credentials_service_generator.generate)
    main_controller_thread = Thread(None, target=main_controller_generator.generate)

    threads.append(send_object_thread)
    threads.append(append_credentials_thread)
    threads.append(main_controller_thread)

    send_object_thread.start()
    append_credentials_thread.start()
    main_controller_thread.start()

    for thread in threads:
        thread.join()


def generate_php(data, output_path):
    threads = []

    for table in data['tables']:
        controller_generator = PhpControllerGenerator(table, output_path + "classes/controllers/")
        model_generator = PhpModelGenerator(table, output_path + "classes/models/")

        controller_thread = Thread(None, target=controller_generator.generate)
        model_thread = Thread(None, target=model_generator.generate)

        threads.append(controller_thread)
        threads.append(model_thread)

        controller_thread.start()
        model_thread.start()

    base_controller_generator = PhpBaseControllerGenerator(output_path + "classes/controllers/")
    base_model_generator = PhpBaseModelGenerator(output_path + "classes/controllers/")
    gallery_generator = PhpHardCodedFileGenerator("generators/php/templates/gallery_template.txt",
                                                  "Gallery",
                                                  output_path + "classes/")

    base_controller_thread = Thread(None, target=base_controller_generator.generate)
    base_model_thread = Thread(None, target=base_model_generator.generate)
    gallery_generator_thread = Thread(None, target=gallery_generator.generate)

    threads.append(base_controller_thread)
    threads.append(base_model_thread)
    threads.append(gallery_generator_thread)

    base_controller_thread.start()
    base_model_thread.start()
    gallery_generator_thread.start()

    if data['config'] is not None:
        config_generator = PhpConfigGenerator(data['config'], output_path)
        config_thread = Thread(None, target=config_generator.generate)

        threads.append(config_thread)
        config_thread.start()

    db_generator = PhpDBGenerator(output_path + "classes/")
    db_generator_thread = Thread(None, db_generator.generate())

    threads.append(db_generator_thread)
    db_generator_thread.start()

    for thread in threads:
        thread.join()


def check_user_input(input):
    if input == "yes" or input == "y":
        return True
    elif input == "no" or input == "n":
        return False


def remove_file(file_path):
    print("Removing file.")
    os.remove(file_path)


def generate_sql(data, output_path):

    output_file_name = "statements.sql"
    output_file_path = output_path + output_file_name
    output_file = Path(output_file_path)

    if output_file.is_file():
        message = ("There is already an sql file at {output_path}.\n"
                   "If it is not removed the new statements will simply be appended to the old file.\n"
                   "It is recommended that the old file is removed before proceeding.\n"
                   "Would you like to remove {output_file_path}?\n".
                   format(output_path=output_path,
                          output_file_path=output_file_path))

        confirmation = input(message)

        confirmation = confirmation.lower()
        while True:
            if check_user_input(confirmation):
                remove_file(output_file_path)
                break
            else:
                extra_confirmation = input("This will lead to termination of the sql generation. Are you sure?\n")
                if check_user_input(extra_confirmation):
                    return
                else:
                    remove_file(output_file_path)
                    break

    threads = []

    for table in data:
        my_sql_generator = MySqlGenerator(table, output_path, output_file_name)
        sql_thread = Thread(None, target=my_sql_generator.generate)

        threads.append(sql_thread)
        sql_thread.start()

    for thread in threads:
        thread.join()


def check_output_path(default_path, argument_to_check, base_output_directory):

    base_output_directory = base_output_directory if base_output_directory is not None else ""
    output_path = default_path

    if argument_to_check is not None:

        output_path = argument_to_check

        if not output_path.endswith('/'):
            output_path += '/'

    return base_output_directory + output_path


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Path to a file that is to be read.')
    parser.add_argument('-php',
                        help='Generate php.',
                        action='store_true')
    parser.add_argument('-phpo', '--php_output_directory',
                        help='Output directory for generated php code.')
    parser.add_argument('-sql',
                        help='Generate sql.',
                        action='store_true')
    parser.add_argument('-sqlo', '--sql_output_directory',
                        help='Output directory for generated sql statements.')
    parser.add_argument('-angular',
                        help='Generate angular.',
                        action='store_true')
    parser.add_argument('-angularo', '--angular_output_directory',
                        help='Output directory for generated angular code.')
    parser.add_argument('-baseo', '--base_output_directory',
                        help='Base output directory, the path of which will be prepended to all other paths specified')

    arguments = parser.parse_args()

    json_reader = JsonReader(arguments.path)
    data = json_reader.read()

    threads = []
    generated_formats = {}

    if arguments.php:

        output_path = check_output_path("php/",
                                        arguments.php_output_directory,
                                        arguments.base_output_directory)

        php_thread = Thread(None, target=generate_php, args=(data, output_path))
        threads.append(php_thread)
        php_thread.start()

        generated_formats['php'] = output_path

    if arguments.sql:

        output_path = check_output_path("sql/",
                                        arguments.sql_output_directory,
                                        arguments.base_output_directory)

        sql_thread = Thread(None, target=generate_sql, args=(data['tables'], output_path))
        threads.append(sql_thread)
        sql_thread.start()

        generated_formats['sql'] = output_path

    if arguments.angular:

        output_path = check_output_path("angular/",
                                        arguments.angular_output_directory,
                                        arguments.base_output_directory)

        angular_thread = Thread(None, target=generate_angular, args=(data['tables'], output_path))
        threads.append(angular_thread)
        angular_thread.start()

        generated_formats['angular'] = output_path

    for thread in threads:
        thread.join()

    formats_and_output_paths = ""

    first = True
    for code_format in generated_formats:

        if first:
            first = False
        else:
            formats_and_output_paths += ",\n"

        formats_and_output_paths += code_format + " at " + generated_formats[code_format]

    print("Done generating code. The following was generated:\n\n{}".format(formats_and_output_paths))

main()
