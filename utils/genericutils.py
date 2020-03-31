import os
import json

def perform_cli_action(command):
    stm = os.popen(command)
    content = "".join(stm.readlines())
    if not len(content):
        return None
    return json.loads(content)

def collect_accounts(subid = None, prefix = None):
    return_accounts = []
    acct_generic = perform_cli_action("az account list --all")
    for acct in acct_generic:
        if acct['state'] == 'Enabled':
            if subid:
                if acct['id']== subid:
                    return_accounts.append(acct['id'])
            elif prefix:
                if acct['name'].lower().startswith(prefix.lower()):
                    return_accounts.append(acct['id'])
            else:
                return_accounts.append(acct['id'])
    return return_accounts

def get_virtual_machines():
    return perform_cli_action('az vm list --query "[].{Name:name, ResourceGroup:resourceGroup}" -o json')
  
def get_vm_usage(region):
    command = 'az vm list-usage -l ' + region + ' --query "[].{Current:currentValue, Limit:limit, Type:name.value}" -o json'
    return perform_cli_action(command)