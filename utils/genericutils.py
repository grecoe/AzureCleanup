import os
import json
import datetime

def get_time_stamp():
    now = datetime.datetime.now() 
    time_stamp = now.strftime("%Y_%m_%d_%H_%M")
    return time_stamp

def create_output_dir(base_operation, organization):
    output_dir = os.path.join(base_operation, organization)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def perform_cli_action(command):
    stm = os.popen(command)
    content = "".join(stm.readlines())
    if not len(content):
        return None
    return json.loads(content)

def collect_accounts(subid_list = None, prefix = None, data_type = 'id'):
    return_accounts = []
    acct_generic = perform_cli_action("az account list --all")
    for acct in acct_generic:
        if acct['state'] == 'Enabled':
            if subid_list:
                if acct['id'] in subid_list:
                    return_accounts.append(acct[data_type])
            elif prefix:
                if acct['name'].lower().startswith(prefix.lower()):
                    return_accounts.append(acct[data_type])
            else:
                return_accounts.append(acct[data_type])
    return return_accounts

def get_virtual_machines():
    return perform_cli_action('az vm list --query "[].{Location:location, Name:name, ResourceGroup:resourceGroup}" -o json')
  
def get_vm_usage(region):
    command = 'az vm list-usage -l ' + region + ' --query "[].{Current:currentValue, Limit:limit, Type:name.value}" -o json'
    return perform_cli_action(command)