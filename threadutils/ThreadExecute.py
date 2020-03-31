import collections
from threading import *
from datetime import datetime, timedelta
from threadutils.Tracking import ThreadTracking
from threadutils.Log import AsyncLog

class ExecuteCommandAsync(Thread):
    ExecutionResult = collections.namedtuple('ExecutionResult', 'latency result')

    '''
        Thread class used when processing items - parseObject() because in VM's it can create a secondary call
        that is incredibly slow. 
    '''
    def __init__(self, callback, expansion_tracking, operation, *args):
        Thread.__init__(self)
        self.tracking = expansion_tracking
        self.executionFunction = operation
        self.executionArguments = args
        self.callback = callback

    def run(self):
        self.tracking.modifyThreadCount(1)


        start = datetime.now()
        execution_result = None
        try:
            execution_result = self.executionFunction(self.executionArguments)
        except Exception as ex:
            execution_result = ex
        end = datetime.now()

        result = ExecuteCommandAsync.ExecutionResult(latency = (end-start), result = execution_result)

        self.tracking.addThreadResult(result)
        self.tracking.modifyThreadCount(-1)


        if self.callback:
            self.callback()
