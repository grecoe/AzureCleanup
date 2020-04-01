import os
import time
import json
import collections

from datetime import datetime, timedelta

from threadutils.Controller import AsyncController
from threadutils.Log import AsyncLog
from utils.genericutils import * 

vm_target = collections.namedtuple('vm_target', 'name resource_group')
vm_status = collections.namedtuple('vm_status', 'name resource_group running')


def collect_vms():
    result = perform_cli_action('az resource list --resource-type "Microsoft.Compute/virtualMachines"')

    return_list = []
    for res in result:
        return_list.append(vm_target(res["name"], res["resourceGroup"]))
    return return_list

def parse_vm(vm_name = None, resource_group=None, shut_down=False):
    '''
        IF it's a tuple then it's a threaded call from the controller 
        and we need to unpack it. Otherwise we expect 
        the parameters to be set. 
    '''
    if isinstance(vm_name, tuple):
        if len(vm_name) != 3:
            raise Exception("Incorrect argument count...")
        shut_down = vm_name[2]
        resource_group = vm_name[1]
        vm_name = vm_name[0]

    if not resource_group or not vm_name:
        raise Exception("Parameter exception")

    instance_cmd = 'az vm get-instance-view --name {} --resource-group {}'.format(vm_name, resource_group)
    vm_inst = perform_cli_action(instance_cmd)
    running = False

    if vm_inst :
        for status in vm_inst["instanceView"]["statuses"]:
            if status["code"] == 'PowerState/running':
                running = True

        if running and shut_down:
            AsyncLog.print("Deallocating {}".format(vm_name))
            #print("Deallocating",vm_name)
            shut_down_cmd = "az vm deallocate -n {} -g {} --no-wait".format(vm_name, resource_group)
            os.system(shut_down_cmd)

        rg = vm_inst["resourceGroup"]
        sz = vm_inst["hardwareProfile"]["vmSize"]

    return vm_status(vm_name, resource_group, running)

'''
    Code
'''

'''
    Thread it...
'''
print("Threading...")

running_machines = 0
total_machines = 0
force_deallocation = False

start = datetime.now()
accounts = collect_accounts()
quit()

for account in accounts:
    asyncController = AsyncController(15)
    
    print("Process ", account)
    os.system('az account set -s {}'.format(account))

    print("Collecting VM's")
    vm_list = collect_vms()

    if not len(vm_list):
        continue
    
    print("Checking {} machines".format(len(vm_list)))
    for vm in vm_list:
        asyncController.queueTask(parse_vm, vm.name, vm.resource_group, force_deallocation)

    while asyncController.waitExecution(1) == False:
        pass

    execution_results = asyncController.getExecutionResults()
    total_machines += len(execution_results)
    for result in execution_results:
        if not isinstance(result.result, Exception) and result.result.running:
            running_machines += 1
            print("   ", result.result.name)
        elif isinstance(result.result, Exception) :
            print(result.result)

stop = datetime.now()

print("Threaded Execution Time: ", stop - start)
print("Total: {} Running: {}".format(total_machines, running_machines))
quit()

