import argparse
from threading import Thread

from generators.php.PhpControllerGenerator import PhpControllerGenerator

from generators.php.PhpBaseControllerGenerator import PhpBaseControllerGenerator
from generators.php.PhpBaseModelGenerator import PhpBaseModelGenerator
from generators.php.PhpConfigGenerator import PhpConfigGenerator
from generators.php.PhpDBGenerator import PhpDBGenerator
from generators.php.PhpModelGenerator import PhpModelGenerator
from generators.sql.MySqlGenerator import MySqlGenerator
from readers.JsonReader import JsonReader


def generate_php(data):
    threads = []

    for table in data['tables']:
        controller_generator = PhpControllerGenerator(table)
        model_generator = PhpModelGenerator(table)

        controller_thread = Thread(None, target=controller_generator.generate)
        model_thread = Thread(None, target=model_generator.generate)

        threads.append(controller_thread)
        threads.append(model_thread)

        controller_thread.start()
        model_thread.start()

    base_controller_generator = PhpBaseControllerGenerator()
    base_model_generator = PhpBaseModelGenerator()

    base_controller_thread = Thread(None, target=base_controller_generator.generate)
    base_model_thread = Thread(None, target=base_model_generator.generate)

    threads.append(base_controller_thread)
    threads.append(base_model_thread)

    base_controller_thread.start()
    base_model_thread.start()

    if data['config'] is not None:
        config_generator = PhpConfigGenerator(data['config'])
        config_thread = Thread(None, target=config_generator.generate)

        threads.append(config_thread)
        config_thread.start()

    db_generator = PhpDBGenerator()
    db_generator_thread = Thread(None, db_generator.generate())

    threads.append(db_generator_thread)
    db_generator_thread.start()

    for thread in threads:
        thread.join()

    print("Done generating PHP. Files can be found in php/")


def generate_sql(data):
    threads = []

    for table in data:
        mySqlGenerator = MySqlGenerator(table)
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

    php_thread = Thread(None, target=generate_php, args=(data,))
    php_thread.start()

    sql_thread = Thread(None, target=generate_sql, args=(data['tables'],))
    sql_thread.start()

    php_thread.join()
    sql_thread.join()

    print("Done generating code.")


main()
