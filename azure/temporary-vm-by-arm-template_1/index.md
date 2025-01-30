# Temporary Vm by Arm Template_1


# Creat a VM with misc resources by ARM Template
To create a smiple VM to be accessable, we need to create a resource group, a virtual network, a subnet, a public IP, and a VM. 

## ARM template to create a VM with its dependencies
```json
{
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
      "vmName": {
        "type": "string",
        "metadata": {
          "description": "Name of the virtual machine."
        }
      },
      "adminUsername": {
        "type": "string",
        "metadata": {
          "description": "Username for the VM."
        }
      },
      "adminPassword": {
        "type": "securestring",
        "metadata": {
          "description": "Password for the VM."
        }
      },
      "location": {
        "type": "string",
        "defaultValue": "[resourceGroup().location]",
        "metadata": {
          "description": "Location for the VM."
        }
      }
    },
    "variables": {
      "storageAccountName": "[concat(uniqueString(resourceGroup().id), 'storage')]",
      "nicName": "[concat(parameters('vmName'), '-nic')]",
      "publicIPAddressName": "[concat(parameters('vmName'), '-ip')]",
      "subnetRef": "[resourceId('Microsoft.Network/virtualNetworks/subnets', 'myVnet', 'default')]"
    },
    "resources": [
      {
        "type": "Microsoft.Network/publicIPAddresses",
        "apiVersion": "2020-11-01",
        "name": "[variables('publicIPAddressName')]",
        "location": "[parameters('location')]",
        "properties": {
          "publicIPAllocationMethod": "Dynamic"
        }
      },
      {
        "type": "Microsoft.Network/networkInterfaces",
        "apiVersion": "2020-11-01",
        "name": "[variables('nicName')]",
        "location": "[parameters('location')]",
        "dependsOn": [
          "[resourceId('Microsoft.Network/networkSecurityGroups', concat(parameters('vmName'), '-nsg'))]",
          "[resourceId('Microsoft.Network/virtualNetworks', 'myVnet')]",
          "[resourceId('Microsoft.Network/publicIPAddresses', variables('publicIPAddressName'))]"
        ],
        "properties": {
          "networkSecurityGroup": {
            "id": "[resourceId('Microsoft.Network/networkSecurityGroups', concat(parameters('vmName'), '-nsg'))]"
          },
          "ipConfigurations": [
            {
              "name": "ipconfig1",
              "properties": {
                "subnet": {
                  "id": "[variables('subnetRef')]"
                },
                "publicIPAddress": {
                  "id": "[resourceId('Microsoft.Network/publicIPAddresses', variables('publicIPAddressName'))]"
                }
              }
            }
          ]
        }
      },
      {
        "type": "Microsoft.Compute/virtualMachines",
        "apiVersion": "2021-03-01",
        "name": "[parameters('vmName')]",
        "location": "[parameters('location')]",
        "dependsOn": [
          "[resourceId('Microsoft.Network/networkInterfaces', variables('nicName'))]"
        ],
        "properties": {
          "hardwareProfile": {
            "vmSize": "Standard_B1s"
          },
          "osProfile": {
            "computerName": "[parameters('vmName')]",
            "adminUsername": "[parameters('adminUsername')]",
            "adminPassword": "[parameters('adminPassword')]",
            "linuxConfiguration": {
              "disablePasswordAuthentication": false
            }
          },
          "storageProfile": {
            "imageReference": {
              "publisher": "Canonical",
              "offer": "0001-com-ubuntu-server-jammy",
              "sku": "22_04-lts-gen2",
              "version": "latest"
            },
            "osDisk": {
              "createOption": "FromImage",
              "diskSizeGB": 128
            }
          },
          "networkProfile": {
            "networkInterfaces": [
              {
                "id": "[resourceId('Microsoft.Network/networkInterfaces', variables('nicName'))]"
              }
            ]
          }
        }
      },
      {
        "type": "Microsoft.Network/networkSecurityGroups",
        "apiVersion": "2020-11-01",
        "name": "[concat(parameters('vmName'), '-nsg')]",
        "location": "[parameters('location')]",
        "properties": {
          "securityRules": [
            {
              "name": "AllowSSH",
              "properties": {
                "priority": 1000,
                "protocol": "Tcp",
                "access": "Allow",
                "direction": "Inbound",
                "sourceAddressPrefix": "*",
                "sourcePortRange": "*",
                "destinationAddressPrefix": "*",
                "destinationPortRange": "22"
              }
            }
          ]
        }
      },
      {
        "type": "Microsoft.Network/virtualNetworks",
        "apiVersion": "2020-11-01",
        "name": "myVnet",
        "location": "[parameters('location')]",
        "properties": {
          "addressSpace": {
            "addressPrefixes": [
              "10.0.0.0/16"
            ]
          },
          "subnets": [
            {
              "name": "default",
              "properties": {
                "addressPrefix": "10.0.0.0/24"
              }
            }
          ]
        }
      }
    ]
  }
```
## Create a resource group
```bash
$ az group create --name trg --location eastus
```
## Create a VM using above template: azure-template.json
```bash
$ az deployment group create \
    --resource-group trg \
    --template-file azure-template.json \
    --parameters vmName=tvm adminUsername=victoronto adminPassword=Victoront012
```
## access the VM
```bash
$ ssh victoronto@40.71.121.8
The authenticity of host '40.71.121.8 (40.71.121.8)' can't be established.
ED25519 key fingerprint is SHA256:HShN6wFfrrRhqQDjqR41P/KfcgRUu1cb92jdxm7eXlU.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '40.71.121.8' (ED25519) to the list of known hosts.
victoronto@40.71.121.8's password:
Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 6.8.0-1020-azure x86_64)
 ...
```
## Delete the resource group to clean up everything you have created
```bash
$ az group delete --name trg --yes --no-wait
```
# Problems and ToDoList to improve
1. To access it, we need to get it's public IP address from Azure Web Console. It would be better to assign a DNS name to it.
1. Using a prameter file to store the password and other parameters instead of using command line.
1. The password is in plain text in the command line. It would be better to use a key pair.


