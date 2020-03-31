from threadutils.Controller import AsyncController
from threadutils.Log import AsyncLog
from utils.genericutils import *

def thread_fn_get_usage(region = None):
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

    WARNING WARNING WARNING
    This is SUPER slow as it has to scan per region for VM usage
    and there are a LOT of regions. This could be made MUCH better
    if we limited the number of regions to search. 
'''
print("Collecting accounts")
account_id = '8ac510a6-db5e-4a52-8b76-3543bd940029'
accounts = collect_accounts(account_id, 'ag-ce')

regions_of_interest = ['westus', 'northeurope', 'southcentralus', 'eastus2', 'eastus', 'westus2', 'southeastasia', 'westeurope', 'australiacentral', 'canadacentral', 'australiaeast', 'centralus']
global_data = []

for account in accounts:
    print("Process ", account)
    os.system('az account set -s {}'.format(account))

    print("Get regions....")
    #regions = perform_cli_action('az account list-locations')

    print("Process regions...")
    controller = AsyncController (10)
    for region in regions_of_interest:
        controller.queueTask(thread_fn_get_usage, region) #region["name"])

    while controller.waitExecution(1) == False:
        pass

    regional_data = []
    execution_results = controller.getExecutionResults()
    for result in execution_results:
        if not isinstance(result.result, Exception) and result.result:
            regional_data.append(result.result)
            global_data.append(result.result)

    with open("{}_usage.json".format(account), "+w") as output:
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
for result in global_data:
    for key in result:

        if key not in global_parsed_data.keys():
            global_parsed_data[key] = {}

        for type_key in result[key]:
            if type_key in ignore_sets:
                continue

            if type_key not in global_parsed_data[key].keys():
                global_parsed_data[key][type_key] = 0
            global_parsed_data[key][type_key] += result[key][type_key]

with open("global_usage.json", '+w') as global_output:
    global_output.write(json.dumps(global_parsed_data, indent=4))

