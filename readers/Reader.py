from abc import ABCMeta, abstractmethod
import traceback
from threading import Thread


class Reader(metaclass=ABCMeta):
    def __init__(self, path):
        self.path = path
        self.threads = []

    @abstractmethod
    def read(self):
        pass

    def run_threaded_reader_task(self, collection):
        try:
            for item in collection:
                self.start_thread(self.reader_task, (item,))
        except:
            traceback.print_exc()

    def start_thread(self, task, arguments):
        thread = Thread(None, target=task, args=arguments)
        self.threads.append(thread)
        thread.start()

    def join_threads(self):
        for thread in self.threads:
            thread.join()

    def evaluates_to_true(self, string):
        return string == "true"

    @abstractmethod
    def reader_task(self, input_data):
        pass
