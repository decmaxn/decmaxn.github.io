# Azure Cli


[Official Reference](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli). 

## Installation

I have avoid the one command installation, and followed the step-by-step on my ubuntu client.

```bash
# Get packages needed for the install process:
sudo apt-get update
sudo apt-get install ca-certificates curl apt-transport-https lsb-release gnupg

#Download and install the Microsoft signing key:
sudo mkdir -p /etc/apt/keyrings
curl -sLS https://packages.microsoft.com/keys/microsoft.asc |
    gpg --dearmor |
    sudo tee /etc/apt/keyrings/microsoft.gpg > /dev/null
sudo chmod go+r /etc/apt/keyrings/microsoft.gpg

# Add the Azure CLI software repository:
AZ_REPO=$(lsb_release -cs)
echo "deb [arch=`dpkg --print-architecture` signed-by=/etc/apt/keyrings/microsoft.gpg] https://packages.microsoft.com/repos/azure-cli/ $AZ_REPO main" |
    sudo tee /etc/apt/sources.list.d/azure-cli.list

# Update repository information and install the azure-cli package:
sudo apt-get update
sudo apt-get install azure-cli
```

## Upgrade
The installation process above will update your Azure Cli, but it might not the latest. The following happens right after I updated it with apt command.
```bash
$ az upgrade
This command is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
Your current Azure CLI version is 2.47.0. Latest version available is 2.48.1.
Please check the release notes first: https://docs.microsoft.com/cli/azure/release-notes-azure-cli
Do you want to continue? (Y/n): y
```
### Uninstall
```bash
sudo apt-get remove -y azure-cli
# Remove it's data for security
rm -rf ~/.azure
```

## Login
After logging in, you see a list of subscriptions associated with your Azure account.
```bash
$ az login
A web browser has been opened at https://login.microsoftonline.com/organizations/oauth2/v2.0/authorize. Please continue the login in the web browser. If no web browser is available or if the web browser fails to open, use device code flow with `az login --use-device-code`.
```
## Cli auto completion
First, re-open your command prompt. It is automatically installed you just need to active it, re-open prompt will do so.
```bash
$ wc -l /etc/bash_completion.d/azure-cli
21 /etc/bash_completion.d/azure-cli
```

## Learning

interactive mode that automatically displays help information and makes it easier to select subcommands

```bash
$ az interactive
```


## Tenants, users, and subscriptions
A tenant is the Azure Active Directory entity that encompasses a whole organization.  A tenant has one or more subscriptions and users. Users are those accounts that sign in to Azure to create, manage, and use resources. A user may have access to multiple subscriptions, but a user is only associated with a single tenant. Subscriptions are the agreements with Microsoft to use cloud services, including Azure. Every resource is associated with a subscription.

```bash
az account tenant list
#  the active tenant ID and default subscription
az account show

# store the default(or another - change query) subscription  in a variable
subscriptionId="$(az account list --query "[?isDefault].id" -o tsv)"
echo $subscriptionId
```
