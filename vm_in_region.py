import os
import json
import sys
from arguments import *
from utils.genericutils import *

'''
    CALLING
        Example - AGCE
        python vm_in_region.py -org AG-CE -sub_prefix ag-ce -regions westeurope,northeurope

'''

'''
    Program Code
'''
print("Collecting accounts")
prog_aruments = ProgramArguments(sys.argv[1:])

active_accounts = collect_accounts(prog_aruments.subs_to_process, prog_aruments.account_prefix,'name')
print("{} Accounts To Process".format(len(active_accounts)))
print("Regions", prog_aruments.regions)

if prog_aruments.whatif:
    print(json.dumps(active_accounts, indent=4))
    quit()

'''
    Create the output directories
'''

regional_information = []
regional_information.append("region,subscription,machine,resource_group")
for account in active_accounts:
    print("Process ", account)
    os.system('az account set -s {}'.format(account))

    print("Get machines....")
    vm_list = get_virtual_machines()
    for vm in vm_list:
        if vm["Location"] in prog_aruments.regions:
            data = "{},{},{},{}".format(
                vm["Location"],
                account,
                vm["Name"],
                vm["ResourceGroup"]
            )
            regional_information.append(data)

time_stamp = get_time_stamp()
usage_dir = create_output_dir("regional_usage", prog_aruments.organization)
file_name = "{}.csv".format(time_stamp)
file_name = os.path.join(usage_dir, file_name)
with open(file_name, "+w") as output_file:
    for entry in regional_information:
        output_file.write("{}\n".format(entry))


