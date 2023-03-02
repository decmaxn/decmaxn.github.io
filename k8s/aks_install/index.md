# AKS_install


# Install Azure Cli

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
    --kubernetes-version 1.25.5 \ # no need to 
    --node-count 3 #default Node count is 3
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

# Check created Cluster and clean up

```bash
# kubectl config use-context CSCluster # No need since there is only one context in my case
$ kubectl get nodes
NAME                                STATUS   ROLES   AGE     VERSION
aks-nodepool1-30040660-vmss000000   Ready    agent   6m59s   v1.25.5
aks-nodepool1-30040660-vmss000001   Ready    agent   7m9s    v1.25.5
aks-nodepool1-30040660-vmss000002   Ready    agent   7m4s    v1.25.5
$ kubectl get pods --all-namespaces
NAMESPACE     NAME                                  READY   STATUS    RESTARTS   AGE
kube-system   azure-ip-masq-agent-4rtqg             1/1     Running   0          7m15s
kube-system   azure-ip-masq-agent-7cksn             1/1     Running   0          7m20s
kube-system   azure-ip-masq-agent-pfrlc             1/1     Running   0          7m10s
kube-system   cloud-node-manager-bkx6r              1/1     Running   0          7m10s
kube-system   cloud-node-manager-jc7nc              1/1     Running   0          7m15s
kube-system   cloud-node-manager-pmtjw              1/1     Running   0          7m20s
kube-system   coredns-77f75ff65d-4tkjq              1/1     Running   0          8m3s
kube-system   coredns-77f75ff65d-5jwpn              1/1     Running   0          5m49s
kube-system   coredns-autoscaler-58bfcf6b5-tqxfc    1/1     Running   0          8m3s
kube-system   csi-azuredisk-node-4dm99              3/3     Running   0          7m20s
kube-system   csi-azuredisk-node-p2vwd              3/3     Running   0          7m10s
kube-system   csi-azuredisk-node-tln65              3/3     Running   0          7m15s
kube-system   csi-azurefile-node-hqb26              3/3     Running   0          7m15s
kube-system   csi-azurefile-node-rvtrg              3/3     Running   0          7m20s
kube-system   csi-azurefile-node-xfn99              3/3     Running   0          7m10s
kube-system   konnectivity-agent-75bbc5fb66-9k28c   1/1     Running   0          5m48s
kube-system   konnectivity-agent-75bbc5fb66-wpwv7   1/1     Running   0          8m1s
kube-system   kube-proxy-2jqsn                      1/1     Running   0          7m15s
kube-system   kube-proxy-9v9vl                      1/1     Running   0          7m10s
kube-system   kube-proxy-w9pj4                      1/1     Running   0          7m20s
kube-system   metrics-server-686f5fc4bc-f6thg       2/2     Running   0          5m43s
kube-system   metrics-server-686f5fc4bc-g86rh       2/2     Running   0          5m43s
$ az aks delete --resource-group "Kubernetes-Cloud" --name CSCluster #--yes --no-wait
Are you sure you want to perform this operation? (y/n): y
# if used -no-wait option, it will delete in the back ground. Verify like this:
# az aks show --resource-group "Kubernetes-Cloud" --name CSCluster
```
