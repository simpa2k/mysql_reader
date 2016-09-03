import argparse
from readers.JsonReader import JsonReader
from readers.CreateTableReader import CreateTableReader 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Path to a file that is to be read.')

    arguments = parser.parse_args()


    json_reader = JsonReader(arguments.path)
    json_reader.read()
#    create_table_reader = CreateTableReader(arguments.path)
#    create_table_reader.read()


main()
