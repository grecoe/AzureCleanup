# Replace <my-resource-group> with the name of your resource group
RES_GROUP=$1

# Replace <my_vnet_name> with the name of your VNet name
VNET_NAME=$2

# Replace <my_subnet_name> with the name of your subnet name
SUBNET_NAME=virtual-node-aci

# Get network profile ID
NETWORK_PROFILE_ID=$(az network profile list --resource-group $RES_GROUP --query [0].id --output tsv)

# Delete the network profile
az network profile delete --id $NETWORK_PROFILE_ID -y

# Get the service association link (SAL) ID
SAL_ID=$(az network vnet subnet show --resource-group $RES_GROUP --vnet-name $VNET_NAME --name $SUBNET_NAME --query id --output tsv)/providers/Microsoft.ContainerInstance/serviceAssociationLinks/default

# Delete the default SAL ID for the subnet
az resource delete --ids $SAL_ID --api-version 2018-07-01

# Delete the subnet delegation to Azure Container Instances
az network vnet subnet update --resource-group $RES_GROUP --vnet-name $VNET_NAME --name $SUBNET_NAME--remove delegations 0

# Delete the subnet
az network vnet subnet delete --resource-group $RES_GROUP --vnet-name $VNET_NAME --name $SUBNET_NAME

# Delete virtual network
az network vnet delete --resource-group $RES_GROUP --name $VNET_NAME