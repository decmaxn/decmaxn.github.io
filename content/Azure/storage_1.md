---
title: "Storage_1"
date: 2024-12-29T19:11:08-05:00
draft: false
tags: ["Azure","tips"]
---


# Storage

Manually create storage account from Azure Web Console, then confirm it using the following commands
```bash
$ SubID=$(az account show --query id --output tsv)
$ az group list --subscription $SubID --query [].name
$ az storage account list --subscription $SubID --query [].name
```
Give myself permission to create container and upload blob
```bash
$ az ad signed-in-user show --query id -o tsv | az role assignment create \
    --role "Storage Blob Data Contributor" \
    --assignee @- \
    --scope "/subscriptions/$SubID/resourceGroups/trg"
```
Let's assume the storage account name is tsc123tsc, create container as tsc. pre-check and post-check.
```bash
$ az storage container list --account-name tsa123tsa --auth-mode login
$ az storage container create --account-name tsa123tsa --name tsc --auth-mode login
```
Now let's pre-check the container, upload a file, post-check and download it back.
```bash
$ az storage blob list --container-name tsc --account-name tsa123tsa --auth-mode login
$ az storage blob upload --account-name tsa123tsa --auth-mode login --container-name tsc --file README.md
$ az storage blob download --account-name tsa123tsa --container-name tsc --auth-mode login --name README.md --file DownloadedREADME.md
```
