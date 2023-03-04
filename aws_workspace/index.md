# AWS_Workspace


Don't expect to see AWS created public Images based on Windows 10 Desktop, they are all Windows Server based. 

However, I have installed Docker Desktop successfully on a "Windows 10(Server 2019 based)" workspace.

```bash
Profile=<profile>
Region=<region.

# existing Directory Service dreictory
$ aws ds --profile $Profile --region $Region \
    describe-directories --query 'DirectoryDescriptions[].DirectoryId'

# exsiting bundles
$ aws workspaces --profile $Profile --region $Region \
    describe-workspace-bundles --query 'Bundles[].BundleId'

export DirectoryId = <>
export BundleId = <>

# Creat a workspace with existing user and bundle.
$ aws workspaces --profile $Profile --region $Region \
    create-workspaces --workspace \
    DirectoryId=$DirectoryId,\
    UserName=<UserName>,\
    BundleId=$BundleID
# Describe the workspace 
$ aws workspaces --profile $Profile --region $Region describe-workspaces \
    --query 'Workspaces[?UserName==`<UserName>`]'
# Migrate to another existing bundle
$ aws workspaces --profile $Profile --region $Region migrate-workspace \
    --source-workspace-id <workspaceID just been created> \
    --bundle-id <another bundle id>

# Change size of the workspace
$ aws workspaces --profile $Profile --region $Region \
    modify-workspace-properties \
    --workspace-id <workspaceID just been created> \
    --workspace-properties ComputeTypeName=PERFORMANCE

An error occurred (InvalidResourceStateException) when calling the ModifyWorkspaceProperties operation: Action not supported.  Property update not allowed within 21,600 seconds of creation. #6 hours
```

Install workspace client on Windows with Choco.

```cmd
choco install amazon-workspaces
```
Follow [Amazon WorkDocs Drive](https://docs.aws.amazon.com/workdocs/latest/userguide/drive_install.html) to share files between local computer and workspace.
