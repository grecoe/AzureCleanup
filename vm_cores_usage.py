import os
import json
import sys
from arguments import *
from utils.genericutils import *
from threadutils.Controller import AsyncController
from threadutils.Log import AsyncLog
'''
    Program gets core usage for a set of subscriptions either 
        1. Identified by a list of subs to search
        2. Identified by a prefix pattern
        3. All subs available to the caller

    For each account:
        1. Gets a list of virtual machines and collects the regions
           they reside it.
        2. Collects vm usage stats for all regions identified in step 1
        3. Reports it to cores_usage/organization

    CALLING
        Example - AGCE
        python cores_usage.py -org AG-CE -sub_prefix ag-ce

'''
def thread_fn_get_usage(region = None):
    '''
        Thread function to get the cores usage for 
        a particular region. 

        Returns a dictionary {region:{details}}
    '''
    if isinstance(region, tuple):
        if len(region) != 1:
            raise Exception("Incorrect argument count...")
        region = region[0]
    
    usage = get_vm_usage(region)

    return_data = {}
    return_data[region] = {}
    for sku in usage:
        if int(sku['Current']) > 0:
            return_data[region][sku['Type']] = int(sku['Current'])

    return return_data if len(return_data[region]) else None


'''
    Program Code
'''
print("Collecting accounts")
prog_aruments = ProgramArguments(sys.argv[1:])

active_accounts = collect_accounts(prog_aruments.subs_to_process, prog_aruments.account_prefix)
print("{} Accounts To Process".format(len(active_accounts)))

if prog_aruments.whatif:
    print(json.dumps(active_accounts, indent=4))
    quit()

'''
    Create the output directories
'''
time_stamp = get_time_stamp()
usage_dir = create_output_dir("cores_usage", prog_aruments.organization)
data_dir = create_output_dir(usage_dir, time_stamp)

global_data = []
for account in active_accounts:
    print("Process ", account)
    os.system('az account set -s {}'.format(account))

    print("Get regions....")
    vm_list = get_virtual_machines()
    regions = []
    for vm in vm_list:
        if vm["Location"] not in regions:
            regions.append(vm["Location"])

    print("Process regions...")
    controller = AsyncController (10)
    for region in regions:
        controller.queueTask(thread_fn_get_usage, region) #region["name"])

    # Wait for all the threads to finish
    while controller.waitExecution(1) == False:
        pass

    regional_data = []
    execution_results = controller.getExecutionResults()
    for result in execution_results:
        if not isinstance(result.result, Exception) and result.result:
            regional_data.append(result.result)
            global_data.append(result.result)

    file_name = "{}.json".format(account)
    file_path = os.path.join(data_dir, file_name)
    with open(file_path, "+w") as output:
        output.write(json.dumps(regional_data, indent = 4))

# Now roll up global data
ignore_sets = [
    'availabilitySets',
    'PremiumDiskCount',
    'StandardDiskCount',
    'StandardSSDDiskCount',
    'StandardSnapshotCount',
    'virtualMachineScaleSets']
global_parsed_data = {}
global_parsed_data['total_cores'] = 0
global_parsed_data['total_machines'] = 0
global_parsed_data['regions'] = []

for result in global_data:
    for region in result:

        if region not in global_parsed_data.keys():
            global_parsed_data[region] = {}
            global_parsed_data['regions'].append(region)

        for type_key in result[region]:
            if type_key in ignore_sets:
                continue
            
            if type_key == 'cores':
                global_parsed_data['total_cores'] += result[region][type_key]
            if type_key == 'virtualMachines':
                global_parsed_data['total_machines'] += result[region][type_key]


            if type_key not in global_parsed_data[region].keys():
                global_parsed_data[region][type_key] = 0
            global_parsed_data[region][type_key] += result[region][type_key]

file_name = "{}_global.json".format(time_stamp)
file_path = os.path.join(usage_dir, file_name)
with open(file_path, '+w') as global_output:
    global_output.write(json.dumps(global_parsed_data, indent=4))

