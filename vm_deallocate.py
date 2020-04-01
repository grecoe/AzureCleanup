import os
import json
import sys
from arguments import *
from utils.genericutils import *

'''
    Arguments typically required
    -org        : Organization name, used for outputs.
    -sub_prefix : If you want all subs by prefix
    -subs       : If you want a particular set of subscripitons 

    NOTE: 
        -subs, a list of subs to process, takes precedence over
        the argument -sub_prefix if both are set. 

        -whatif, if set, will get the accounts only. 
'''

'''
    CALLING
        Example - AGCE
        python vm_deallocate.py -org AG-CE -sub_prefix ag-ce
'''
active_accounts = []

prog_aruments = ProgramArguments(sys.argv[1:])

print("Collecting accounts")
active_accounts = collect_accounts(prog_aruments.subs_to_process, prog_aruments.account_prefix)
print("{} Accounts To Process".format(len(active_accounts)))

if prog_aruments.whatif:
    quit()

for account in active_accounts:
    print("Processing ", account)
    continue

    perform_cli_action('az account set -s "{}"'.format(account))

    vm_list = perform_cli_action('az vm list --query "[].{Name:name, ResourceGroup:resourceGroup}" -o json')

    print("Issue dealloc on {} machines".format(len(vm_list)))
    for vm in vm_list:
        response = perform_cli_action("az vm deallocate -n {} -g {} --no-wait".format(
            vm["Name"],
            vm["ResourceGroup"]
        ))
