from threading import *

class AsyncLog:
    LogLock = RLock()

    @staticmethod
    def print(content):
        AsyncLog.LogLock.acquire()
        print(content)
        AsyncLog.LogLock.release()

    