# Azure DevOps Pipeline


## Azure CLI extensions for Devops
First install azure devops extension, creat PAT token and az login from Azure Cloud Shell
```bash
az extension add --name azure-devops
az extension list --query "[].name" | grep azure-devops
```
Following [Azure Official Reference](https://learn.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops&tabs=Windows#create-a-pat) to create your own personal access token - PAT. Then login to azure devops and configure the default org.
```
az devops login
az devops configure --list
az devops configure --defaults organization=https://dev.azure.com/<my org name>
```
## Discover ADO release pipelines
```
PJ="MyProject"
az pipelines build definition list --project "$PJ" | jq '.|length'
az pipelines build definition list --project "$PJ" --query "[].name"
az pipelines release definition list --project "$PJ"| jq '.|length'
az pipelines release definition list --project "$PJ" --query "[].name"
```
For release pipeline, let's duplicate an existing stage:
```
az pipelines release definition list --project "$PJ" --query "[].name"
RL="MyRlease"
az pipelines release definition show --project "$PJ" --name "$RL"
```
There are only 2 commands to work with release definitions: list and show. 
