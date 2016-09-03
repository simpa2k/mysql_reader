from abc import ABCMeta, abstractmethod
import traceback
from threading import Thread

class Reader(metaclass=ABCMeta):

    def __init__(self, path):
        self.path = path

    @abstractmethod
    def read(self):
        pass

#    def runThread(self, thread_id, thread):
#        try:
#            thread.run()
#        except:
#            print("Unable to instantiate thread {}".format(thread_id))

    def run_threads(self, collection):
        try:
            for item in collection:
                thread = Thread(None, self.read_table(item))
                thread.start()
        except:
            traceback.print_exc()

    def evaluatesToTrue(self, string):
        return string == "true"

    @abstractmethod
    def read_table(item):
        pass
