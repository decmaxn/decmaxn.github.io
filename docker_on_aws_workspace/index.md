# AWS_Workspace


# Develop Docker appliation in Windows workspace?

Don't expect to see AWS created public Images based on Windows 10 Desktop, they are all Windows Server based. 

However, I get myself into installing Docker Desktop on a "Windows 10(Server 2019 based)" workspace. Just wan to know if it works.

## Create workspace
```bash
Profile=<profile>
Region=<region>

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

## install Docker Desktop

Install workspace client on Windows with Choco.

```cmd
choco install amazon-workspaces
```
Follow [Amazon WorkDocs Drive](https://docs.aws.amazon.com/workdocs/latest/userguide/drive_install.html) to share files between local computer and workspace.

After remote into the workspace, I used choco to install docker desktop. It  completes successfully.

However, it can't be started and complains about hyperV. I found by systeminfo command that hyperV is installed. 
```
Hyper-V Requirements:      A hypervisor has been detected. Features required for Hyper-V will not be displayed.
```

# Solution

According to official AWS document ["Containers and Windows subsystem for Linux on Amazon WorkSpaces"](https://docs.aws.amazon.com/whitepapers/latest/best-practices-deploying-amazon-workspaces/containers-and-windows-subsystem-for-linux-on-amazon-workspaces.html)

> In cases where customer requirements mandate enabling containers using Amazon WorkSpaces, a [technical how-to](http://aws.amazon.com/blogs/desktop-and-application-streaming/how-to-configure-amazon-workspaces-with-windows-and-docker/) has been published that enables the use of Docker. Customers should be informed that this requires other trailing services, and that there are increased costs and complexity when compared with decoupled, native container services.

That end my advanture.
