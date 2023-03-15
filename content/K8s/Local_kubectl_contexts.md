---
title: "Local_kubectl_contexts"
date: 2023-03-13T13:02:36-04:00
draft: false
tags: ["Azure","K8s","Tips"]
---

# Control my newly create K8s Cluster from my Laptop

Finally my bare-metal K8s Cluster is built.

```bash
vma@MBP ~ % mkdir .kube

vma@MBP ~ % scp -i ~/.ssh/vma_rsa 51:/home/vma/.kube/config .kube/config

Enter passphrase for key '/Users/vma/.ssh/vma_rsa': 

config                                                                                                                                              100% 5640   350.9KB/s   00:00    

vma@MBP ~ % kubectl cluster-info

Kubernetes control plane is running at https://192.168.0.51:6443

CoreDNS is running at https://192.168.0.51:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy



To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.

vma@MBP ~ % kubectl get no

NAME     STATUS   ROLES           AGE     VERSION

cp1      Ready    control-plane   7d11h   v1.26.0

k8s-52   Ready    <none>          7d10h   v1.26.0

k8s-53   Ready    <none>          7d10h   v1.26.0

k8s-54   Ready    <none>          7d10h   v1.26.0

vma@MBP ~ % ls -l .kube 

total 16

drwxr-x---@ 4 vma  staff   128 15 Mar 12:29 cache

-rw-------  1 vma  staff  5640 15 Mar 12:28 config

vma@MBP ~ % wc -l .kube/config 

      19 .kube/config
```

# Connect to my AKS Cluster CSCluster

Because I don't have my AKS configured before connecting to my local K8s Cluster, this az aks get-credentials command added itself to .kube/config file for me.

```bash
vma@MBP ~ % az aks get-credentials --resource-group "Kubernetes-Cloud" --name CSCluster

Merged "CSCluster" as current context in /Users/vma/.kube/config

vma@MBP ~ % wc -l .kube/config                                                         

      32 .kube/config


vma@MBP ~ % kubectl cluster-info

Kubernetes control plane is running at https://cscluster-kubernetes-cloud-ab6151-jpcx0neb.hcp.eastus.azmk8s.io:443

CoreDNS is running at https://cscluster-kubernetes-cloud-ab6151-jpcx0neb.hcp.eastus.azmk8s.io:443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

Metrics-server is running at https://cscluster-kubernetes-cloud-ab6151-jpcx0neb.hcp.eastus.azmk8s.io:443/api/v1/namespaces/kube-system/services/https:metrics-server:/proxy



To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.

vma@MBP ~ % kubectl get no

NAME                                STATUS   ROLES   AGE   VERSION

aks-nodepool1-23893820-vmss000000   Ready    agent   11m   v1.25.5

aks-nodepool1-23893820-vmss000001   Ready    agent   12m   v1.25.5

aks-nodepool1-23893820-vmss000002   Ready    agent   12m   v1.25.5
```

# Switch between them

```bash
vma@MBP ~ % kubectl config get-contexts

CURRENT   NAME                          CLUSTER      AUTHINFO                                 NAMESPACE

*         CSCluster                     CSCluster    clusterUser_Kubernetes-Cloud_CSCluster   

          kubernetes-admin@kubernetes   kubernetes   kubernetes-admin                         

vma@MBP ~ % kubectl config use-context kubernetes-admin@kubernetes

Switched to context "kubernetes-admin@kubernetes".

vma@MBP ~ % kubectl config get-contexts                           

CURRENT   NAME                          CLUSTER      AUTHINFO                                 NAMESPACE

          CSCluster                     CSCluster    clusterUser_Kubernetes-Cloud_CSCluster   

*         kubernetes-admin@kubernetes   kubernetes   kubernetes-admin                         

vma@MBP ~ % kubectl get no             

NAME     STATUS   ROLES           AGE     VERSION

cp1      Ready    control-plane   7d11h   v1.26.0

k8s-52   Ready    <none>          7d10h   v1.26.0

k8s-53   Ready    <none>          7d10h   v1.26.0

k8s-54   Ready    <none>          7d10h   v1.26.0
```

# Delete the AKS cluster won't...

This command won't modify .kube/config file and remove itself. The context still existing after and you can still use it, just it won't be able to connect because the actually cluster is gone.

```bash
$ az aks delete --resource-group "Kubernetes-Cloud" --name CSCluster
Are you sure you want to perform this operation? (y/n): y
```