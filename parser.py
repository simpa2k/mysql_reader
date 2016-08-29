import argparse
import re
import threading
from statement.StatementThread import StatementThread

parser = argparse.ArgumentParser()
parser.add_argument('path', help='Path to a file with create table statements.')

arguments = parser.parse_args()

statements = []
parsedStatements = []

with open(arguments.path, 'r') as file:
        data = file.read()
        statements = data.split(';')
        
        for index, statement in enumerate(statements):
            try:
                thread = StatementThread(index, statement)
                thread.run()
            except:
                print("Unable to start thread")

