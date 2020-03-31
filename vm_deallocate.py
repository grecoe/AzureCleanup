import os
import json

account_id = '8ac510a6-db5e-4a52-8b76-3543bd940029'
account_prefix = 'ag-ce'
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
            if acct['id'] == account_id:
                active_accounts.append(acct['name'])
        elif account_prefix:
            if acct['name'].lower().startswith(account_prefix.lower()):
                active_accounts.append(acct['name'])
        else:
            active_accounts.append(acct['name'])

for account in active_accounts:
    print("clearing ", account)
    perform_cli_action('az account set -s "{}"'.format(account))

    vm_list = perform_cli_action('az vm list --query "[].{Name:name, ResourceGroup:resourceGroup}" -o json')

    print("Issue dealloc on {} machines".format(len(vm_list)))
    for vm in vm_list:
        response = perform_cli_action("az vm deallocate -n {} -g {} --no-wait".format(
            vm["Name"],
            vm["ResourceGroup"]
        ))
