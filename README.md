# AzureCleanup
<sub>Dan Grecoe - A Microsoft Employee</sub>

This repo has python scripts to help manage resources, particularly Virtual Machine resourses, across many subscriptions. 

Futher there is a script that can be utilized (carefully) to delete all resources in a Azure Subscription(s)

## Common Parameters
The scripts described below use a common set of arguments, though some apply to certain scripts only. The arguments can be found in arguments.py.

|Parameter|Required|Type|Description|
|---------|--------|----|-----------|
|-org|Yes|String|No space name for the org script is run for. This generally will be used for output file directory paths.|
|-sub_prefix|No|String|A case insensitive prefix to Azure Subscriptions you are trying to work with.|
|-subs|No|String|The file path of a JSON file that contains a single JSON list containing subscription Id's to work on. <br><br><b>NOTE: If a subs file is provided it trumps the sub_prefix. If neither -subs or -sub_prefix is provided it will work on ALL subscriptions available to the login. </b>|
|-processed|No|String|The file path of a JSON file that contains a single JSON list containing subscrirption ID's that have already been deleted. <b>This is valid ONLY for sub_death_ray.py</b>|
|-regions|No|String|A comma separated string of azure regions to search. This is only valid for <b>vm_in_region.py</b>, and for that script, it's required.|
|-whatif|No|Bool|If set to True, whatever action the script would normally take is truncated and prints only what might happen.|

# Scripts

### sub_death_ray.py
| | |
|-----|-----|
|Parameters|-org<br>[-subs]<br>[-sub_prefix]<br>[-processed]<br>[-whatif]|
|Description|Iterates over a series of subscriptions found using either -subs, -sub_prefix or all subscriptions (if those have not been identified).<br><br>Next it removes from that list any id it finds from the processed file, if supplied.<br><br>Finally, it iterates over those subscriptions and deletes every resource group.|
|Outputs|Outputs will end up in a directory called death_ray/[ORG] where ORG was supplied by the parameters.<br><br>Finally, a file titled [TIME_STAMP]_[ORG].json dumps out the results of the run.  |
|Example|python sub_death_ray.py <br> -org AG <br> -subs list_to_delete.json <br> -processed list_already_deleted.json|

### vm_deallocate.py
| | |
|-----|-----|
|Parameters|-org<br>[-subs]<br>[-sub_prefix]<br>[-whatif]|
|Description|Iterates over a series of subscriptions found using either -subs, -sub_prefix or all subscriptions (if those have not been identified).<br><br>It then walks each subscription and deallocates every Virtual Machine it finds.|
|Outputs|Prints to the console for each subscription how many deallocate calls will be made.|
|Example|python vm_deallocate.py <br> -org AG <br> -subs list_to_scan.json|

### vm_cores_usage.py
| | |
|-----|-----|
|Parameters|-org<br>[-subs]<br>[-sub_prefix]<br>[-whatif]|
|Description|Iterates over a series of subscriptions found using either -subs, -sub_prefix or all subscriptions (if those have not been identified).<br><br>It then walks each subscription finding the regions that have Virtual Machines deployed and on those regions collects the Virtual Machine usage in each of those regions. |
|Outputs|Outputs will end up in a directory called cores_usage/[ORG] where ORG was supplied by the parameters.<br><br>Another directory under that is created with a timestamp. In that sub directory outputs from each subscription is dumped with details on each region, number of cores, number of machines, and core types that are being used. <br><br>Finally, a file titled cores_usage/[ORG]/[TIME_STAMP]_global.json is created with the roll up usage across all subscriptions that were scanned.|
|Example|python vm_cores_usage.py <br> -org AG <br> -subs list_to_scan.json|

### vm_in_region.py
| | |
|-----|-----|
|Parameters|-org<br>[-subs]<br>[-sub_prefix]<br>[-regions]<br>[-whatif]|
|Description|Iterates over a series of subscriptions found using either -subs, -sub_prefix or all subscriptions (if those have not been identified).<br><br>Next, it collects Virtual Machine information for any machine found in the specified regions. This is used mainly for determining what is in EMEA at the moment.|
|Outputs|Outputs will end up in a directory called regional_usage/[ORG] where ORG was supplied by the parameters.<br><br>|The file is CSV and contains 4 columns<br><br>region,subscription,machine,resource_group|
|Example|python vm_in_region.py <br> -org AG <br> -subs list_to_scan.json <br> -regions eastus,westus2|

### vm_find_running.py
| | |
|-----|-----|
|Parameters|None|
|Description|Scans all Virtual Machines and checks if they are running. <br><br><b>WARNING: This takes a long time to run and might not be terribly useful until it takes parameters.</b>|
|Outputs|Prints to the console how many machines it found and how many are running.|
