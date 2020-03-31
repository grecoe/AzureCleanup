import os
import json

account_prefix = None
# There are two issues with this one....
#account_id = '8ac510a6-db5e-4a52-8b76-3543bd940029'
# This one was already empty
#account_id = '4cfc694d-97a1-48dc-966b-b8636e5390c7'
# Vault error
#account_id = "453ff118-d69a-4adb-bdcf-f6479476eaa0"
# Vault error, DF error
# account_id = '942065c3-a8bb-4e17-814a-a8dc6c8552fd'
# VNet Errors
#account_id = '8f68184c-a55f-4f10-95ee-2390743611b5'
# OK canclelled (one more that didn't need the script)
#account_id = '35c07377-46b0-4bc1-bb6f-58e5e3bdaa09'
# Cancelled
#account_id = 'd446582a-f3fe-4c09-ae0f-9a90c006abc3'
# 14 day soft delete
# account_id = 'cd3fffc3-927c-465c-93f9-2ef50f2aea3d'
# Cancelled
# account_id ='85f52460-657a-48ff-a758-2e36537d51da'
'''
account_id = [
    CANCELLED "e0356ff7-7160-423f-9747-2092138dfb6a",
    CANCELLED "1593b9d8-236d-48ab-800e-754e1611f964",
    CANCELLED "34005063-9537-4dbb-b943-e4795c62f37f",
    CANCELLED "e384b434-b159-4b37-9039-aeec33fc4e04",
    CANCELLED "20e03067-3c7b-4539-accf-bbd74914471d",
    CANCELLED "7489afca-19a9-4ddf-824c-d5e99cbf035b",
    CANCELLED"8e58ff0b-e895-4c02-9f83-e9c64c80533e"    
]
'''
account_id = []

active_accounts = []

def perform_cli_action(command):
    stm = os.popen(command)
    content = "".join(stm.readlines())
    if not len(content):
        return None
    return json.loads(content)


'''
    Code here
'''
print("Collect Accounts...")
acct_generic = perform_cli_action("az account list --all")
for acct in acct_generic:
    if acct['state'] == 'Enabled':
        if account_id:
            #if acct['id'] == account_id:
            if acct['id'] in account_id:
                active_accounts.append(acct['name'])
        elif account_prefix:
            if acct['name'].lower().startswith(account_prefix.lower()):
                active_accounts.append(acct['name'])
        else:
            active_accounts.append(acct['name'])

print(active_accounts)
#quit()

for account in active_accounts:
    perform_cli_action('az account set -s "{}"'.format(account))

    group_list = perform_cli_action('az group list -o json')

    print("Listing groups")
    for group in group_list:
        print("Deleting group ", group["name"])
        #az group delete -n MyResourceGroup --no-wait -y
        response = perform_cli_action("az group delete -n {} --no-wait -y".format(
            group["name"]
        ))
        if response:
            print(response)
    '''
    for vm in vm_list:
        print("Deallocate")
        response = perform_cli_action("az vm deallocate -n {} -g {} --no-wait".format(
            vm["Name"],
            vm["ResourceGroup"]
        ))
    '''