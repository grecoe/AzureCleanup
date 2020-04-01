import os
import json
import sys
from arguments import *
from utils.genericutils import *
'''
    Program gets core usage for a set of subscriptions either 
        1. Identified by a list of subs to search
        2. Identified by a prefix pattern
        3. All subs available to the caller

    For each account:
        1. Iterates every resource group and deletes it (or tries to)

    CALLING
        Example - AGCE
        python sub_death_ray.py -org AG -subs subs_to_delete.json -processed cancelled_subs.json

'''

'''
    Collect accounts then strip out any that are already processed
'''
prog_aruments = ProgramArguments(sys.argv[1:])

reporting_data = {}
reporting_data["SubscriptionPrefix"] = prog_aruments.account_prefix
reporting_data["SubscriptionFile"] = prog_aruments.sub_file
reporting_data["SubscriptionCount"] = len(prog_aruments.subs_to_process)
reporting_data["ProcessedSubscriptionFile"] = prog_aruments.sub_processed_file
reporting_data["ProcessedSubscriptionCount"] = len(prog_aruments.subs_already_processed)
reporting_data["SubscriptionProcessingCount"] = 0
reporting_data["DeletedResourceGroupCount"] = 0

print("Collecting accounts")
active_accounts = collect_accounts(prog_aruments.subs_to_process, prog_aruments.account_prefix)

print(len(active_accounts))

if len(prog_aruments.subs_already_processed):
    print("Clearing already processed subscriptions")
    for processed in prog_aruments.subs_already_processed:
        if processed in active_accounts:
            idx = active_accounts.index(processed)
            popped = active_accounts.pop(idx)
            print("Skipping processed account {}".format(popped))

print("{} Accounts To Process".format(len(active_accounts)))
reporting_data["SubscriptionProcessingCount"] = len(active_accounts)

if prog_aruments.whatif:
    print(json.dumps(active_accounts, indent=4))
    quit()

for account in active_accounts:
    perform_cli_action('az account set -s "{}"'.format(account))

    group_list = perform_cli_action('az group list -o json')

    print("Listing groups")
    for group in group_list:
        print("Deleting group ", group["name"])
        reporting_data["DeletedResourceGroupCount"] += 1
        response = perform_cli_action("az group delete -n {} --no-wait -y".format(
            group["name"]
        ))

        if response:
            print(response)

# Dump out some content
usage_dir = create_output_dir("death_ray", prog_aruments.organization)
time_stamp = get_time_stamp()
file_name = "{}_{}.json".format(time_stamp, prog_aruments.organization)
file_name = os.path.join(usage_dir, file_name)
with open(file_name,"+w") as output_file:
    output_file.write(json.dumps(reporting_data, indent=4))