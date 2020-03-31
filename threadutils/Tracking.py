
from threading import *

class ThreadTracking:
    def __init__(self):
        self.lock = RLock()
        self.current_thread_count = 0
        self.results = []

    def getThreadCount(self):
        return_value = 0
        self.lock.acquire()
        return_value = self.current_thread_count
        self.lock.release()
        return return_value

    def modifyThreadCount(self, count):
        self.lock.acquire()
        self.current_thread_count += count
        self.lock.release()

    def addThreadResult(self, result):
        self.lock.acquire()
        self.results.append(result)
        self.lock.release()

    def getThreadResult(self):
        return_results = []
        self.lock.acquire()
        return_results = self.results.copy()
        self.results = []
        self.lock.release()
        return return_results
