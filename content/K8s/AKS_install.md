---
title: "AKS_install"
date: 2023-03-01T23:06:34-05:00
draft: false
tags: ["Azure","K8s","course"]
---

# Install Azure Cli

Install on Windows with ```choco install azure-cli```, or in linux as below:

```bash
$ AZ_REPO=$(lsb_release -cs)
$ echo "deb [arch=amd64] https://packages.microsoft.com/repos/$ azure-cli/ $AZ_REPO main" | sudo tee /etc/apt/sources.list.d/$ azure-cli.list
$ curl -sL https://packages.microsoft.com/keys/microsoft.asc | gpg $ --dearmor | sudo tee /etc/apt/trusted.gpg.d/microsoft.gpg > /dev/$ null
$ sudo apt-get update
$ sudo apt-get install azure-cli
```

# Create a AKS cluster
```bash
$ az login
$ az account set --subscription "Visual Studio Professional Subscription"
$ az group create --name "Kubernetes-Cloud" --location eastus
$ az aks get-versions --location eastus -o table # let use 1.25.5  
$ az aks create \
    --resource-group "Kubernetes-Cloud" \
    --generate-ssh-keys \
    --name CSCluster \
    --kubernetes-version 1.25.5 \
    --node-count 1 #default Node count is 3
```
or
```powershell
az login
az account set -s "Visual Studio Professional Subscription"

# default Node count is 3
az group create -l eastus -n Kubernetes-Cloud
az aks create -g Kubernetes-Cloud -n CSCluster --generate-ssh-keys
```

# Install and config Kubectl
```bash
# az aks install-cli # not necessary in my case
$ az aks get-credentials --resource-group "Kubernetes-Cloud" --name CSCluster
Merged "CSCluster" as current context in /home/vma/.kube/config
$ kubectl config get-contexts
CURRENT   NAME        CLUSTER     AUTHINFO                                 NAMESPACE
*         CSCluster   CSCluster   clusterUser_Kubernetes-Cloud_CSCluster   
```
or
```powershell
# Get the credentials and check the connectivity
# az aks install-cli # not necessary in my case
az aks get-credentials -g Kubernetes-Cloud -n CSCluster --overwrite-existing
kubectl get nodes
az aks scale -g Kubernetes-Cloud -n CSCluster --node-count 1
PS C:\> kubectl config get-contexts
CURRENT   NAME                          CLUSTER      AUTHINFO                                 NAMESPACE
*         CSCluster                     CSCluster    clusterUser_Kubernetes-Cloud_CSCluster   
          kubernetes-admin@kubernetes   kubernetes   kubernetes-admin                         
```
# Check created Cluster and clean up

```bash
# kubectl config use-context CSCluster # No need since there is only one context in my case
$ kubectl get nodes
NAME                                STATUS   ROLES   AGE     VERSION
aks-nodepool1-30040660-vmss000000   Ready    agent   6m59s   v1.25.5
aks-nodepool1-30040660-vmss000001   Ready    agent   7m9s    v1.25.5
aks-nodepool1-30040660-vmss000002   Ready    agent   7m4s    v1.25.5
$ kubectl get pods --all-namespaces
```

#  Create ACR and repo, images, tags
```powershell
# 创建 ACR registry
az acr create -n myacr -g $RG --sku Basic  # SKU：Basic、Standard、Premium
az acr list -o table

# 现在，我们将从 Docker 存储库导入 hello-world 映像
az acr import -n myacr --source docker.io/library/hello-world:latest -t hello-world-backup:1.0.0

# 我们现在有一个存储库, 一个映像, 一个标签
az acr repository list -n myacr -o table
az acr repository show -n myacr --repository hello-world-backup -o table
az acr repository show-tags -n myacr --repository hello-world-backup -o table

# 重新导入一个新标签的镜像，再导入另一个镜像
az acr import -n myacr --source docker.io/library/hello-world:latest -t hello-world-backup:1.1.0
az acr import -n myacr --source docker.io/library/nginx:latest --image nginx:v1


# 克隆一个来自GitHub的示例项目, 而且直接build这个docker image
git clone https://github.com/Azure-Samples/acr-build-helloworld-node
az acr build --registry myacr --image helloacrtasks:v1 acr-build-helloworld-node
```

# Deploy a Image to the new Cluster
```powershell
# 获取我们的ACR登录服务器
az acr show -n myacr -o table
$loginServer=(az acr show -n myacr --query loginServer)

# 新建一个命名空间, 便于留用Cluster 的 Clean up.
# kubectl create namespace acr
# kubectl config set-context --current --namespace acr

# 创建一个deployment
kubectl create deployment nginx --image=$loginServer/nginx:v1

# 检查部署是否成功, 得到 Access Denied Error
kubectl get deployment
kubectl get pods
kubectl describe pod (kubectl get pods -o=jsonpath='{.items[0].metadata.name}')

# 解决以上问题，需要将ACR附加到AKS群集（也可以在创建时完成）
kubectl delete deployment nginx
az aks update -n CSCluster -g Kubernetes-Cloud --attach-acr myacr

# 再次部署deployment，成功
kubectl create deployment nginx --image=$loginServer/nginx:v1
kubectl get deployment,pods
```
# Storage Class

```bash
$ kubectl get storageclasses.storage.k8s.io default 
NAME                PROVISIONER          RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
default (default)   disk.csi.azure.com   Delete          WaitForFirstConsumer   true                   11m
$ kubectl describe storageclasses.storage.k8s.io default 
Name:                  default
IsDefaultClass:        Yes   # 
Annotations:           storageclass.kubernetes.io/is-default-class=true
Provisioner:           disk.csi.azure.com
Parameters:            skuname=StandardSSD_LRS  # Different with other classes, refer to below managed-premium
AllowVolumeExpansion:  True
MountOptions:          <none>
ReclaimPolicy:         Delete  #
VolumeBindingMode:     WaitForFirstConsumer
Events:                <none>
$ kubectl describe storageclasses.storage.k8s.io managed-premium | grep Parameter
Parameters:            cachingmode=ReadOnly,kind=Managed,storageaccounttype=Premium_LRS
$ cat <<EOF > azure_disk.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-azure-managed  #
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: managed-premium
  resources:
    requests:
      storage: 10Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-azdisk-deployment
spec:  
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      volumes:
      - name: webcontent
        persistentVolumeClaim:
          claimName: pvc-azure-managed  # 
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
        volumeMounts:
        - name: webcontent
          mountPath: "/usr/share/nginx/html/web-app"
EOF
$ kubectl apply -f azure_disk.yaml 

$ kubectl get PersistentVolume 
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                       STORAGECLASS      REASON   AGE
pvc-01042b9c-aa58-4d4e-ac9a-9497135c7f58   10Gi       RWO            Delete           Bound    default/pvc-azure-managed   managed-premium            4m53s
$ kubectl get pvc
NAME                STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS      AGE
pvc-azure-managed   Bound    pvc-01042b9c-aa58-4d4e-ac9a-9497135c7f58   10Gi       RWO            managed-premium   5m7s
$ kubectl get pod
NAME                                       READY   STATUS    RESTARTS   AGE
nginx-azdisk-deployment-65cd8f669c-2bss2   1/1     Running   0          5m15s
$ kubectl exec -it deployments/nginx-azdisk-deployment -- /bin/bash
root@nginx-azdisk-deployment-65cd8f669c-2bss2:/# lsblk | grep nginx
sdc       8:32   0    10G  0 disk /usr/share/nginx/html/web-app
```
## Customized Storage Class
Need to refer to Provider ( Azure in this case) document to get all those parameters right.
```bash
$ kubectl delete deployment nginx-azdisk-deployment
$ kubectl delete PersistentVolumeClaim pvc-azure-managed
$ cat <<EOF > custom-storage-class-azure.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: managed-standard-ssd
parameters:
  cachingmode: ReadOnly
  kind: Managed
  storageaccounttype: StandardSSD_LRS
provisioner: kubernetes.io/azure-disk
EOF
$ kubectl apply -f custom-storage-class-azure.yaml 
storageclass.storage.k8s.io/managed-standard-ssd created
$ kubectl get storageclasses.storage.k8s.io   | grep managed-standard-ssd
managed-standard-ssd    kubernetes.io/azure-disk   Delete          Immediate              false                  32s
$ diff azure_disk.yaml custom_azure_disk.yaml   # Just change the storage class in my previous pvc and deployment.
8c8
<   storageClassName: managed-premium
---
>   storageClassName: managed-standard-ssd
$ kubectl apply -f custom_azure_disk.yaml 
persistentvolumeclaim/pvc-azure-managed created
deployment.apps/nginx-azdisk-deployment created

# Only the storage class changed, nothing else.
$ kubectl get PersistentVolume 
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                       STORAGECLASS           REASON   AGE
pvc-54e34adf-441e-465d-865b-6a1d8f38ddce   10Gi       RWO            Delete           Bound    default/pvc-azure-managed   managed-standard-ssd            15s
$  kubectl get pvc
NAME                STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS           AGE
pvc-azure-managed   Bound    pvc-54e34adf-441e-465d-865b-6a1d8f38ddce   10Gi       RWO            managed-standard-ssd   61s
$  kubectl exec -it deployments/nginx-azdisk-deployment -- /bin/bash
root@nginx-azdisk-deployment-65cd8f669c-mgttz:/# lsblk | grep nginx
sdc       8:32   0    10G  0 disk /usr/share/nginx/html/web-app
```
# Clean up
```bash
$ kubectl delete deployment nginx-azdisk-deployment
$ kubectl delete PersistentVolumeClaim pvc-azure-managed
$ az acr delete -n myacr -g Kubernetes-Cloud
$ az aks delete --resource-group "Kubernetes-Cloud" --name CSCluster #--yes --no-wait
Are you sure you want to perform this operation? (y/n): y
# if used -no-wait option, it will delete in the back ground. Verify like this:
# az aks show --resource-group "Kubernetes-Cloud" --name CSCluster

```