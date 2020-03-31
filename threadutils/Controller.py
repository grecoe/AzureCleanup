import time
from threading import *
from threadutils.Tracking import ThreadTracking
from threadutils.ThreadExecute import ExecuteCommandAsync
from threadutils.Log import AsyncLog

class AsyncController:
    maxExecutionCount = 10

    def __init__(self, executionThreadCount = 10):
        self.threadTracking = ThreadTracking()
        self.queue = []
        self.lock = RLock()
        self.executionCount = executionThreadCount

    def queueTask(self, operation, *args):
        self.lock.acquire()
        self.queue.append(ExecuteCommandAsync(self.runQueueTasks, self.threadTracking, operation, *args))
        self.runQueueTasks()
        self.lock.release()

    def runQueueTasks(self):

        self.lock.acquire()

        current_thread_count = self.threadTracking.getThreadCount()
        while current_thread_count < self.executionCount:
            if len(self.queue) > 0:
                #AsyncLog.print("    Pushing item to execution " )
                threadToExecute = self.queue.pop(0)
                threadToExecute.start()
                current_thread_count += 1
            else:
                break

        self.lock.release()

    def waitExecution(self, seconds_timeout):
        if self.threadTracking.getThreadCount() > 0:
            time.sleep(seconds_timeout)
        
        return self.threadTracking.getThreadCount() == 0

    def getExecutionResults(self):
        return self.threadTracking.getThreadResult()