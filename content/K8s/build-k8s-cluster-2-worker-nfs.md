---
title: "Build K8s Cluster 2 Worker Nfs"
date: 2023-03-04T13:40:24-05:00
draft: false
tags: ["K8s","course"]
---

Note for all nodes below, we have to install and configure kubernetes following "Build K8s Cluster 1 Control Plan"

# NFS service
NFS server hostname is c1-storage, IP is 172.16.94.5.

```bash
# Install NFS server and prepare export path
sudo apt install -y nfs-kernel-server
sudo mkdir -p /export/volumes
sudo mkdir /export/volumes/pod

# Configure our NFS Export in /etc/export for /export/volumes to (*) all IPs, with (rw) write permission
# Using no_root_squash because in the demo we are going to mount it with root access.
# and no_subtree_check to allow applications to mount subdirectories of the export directly.
sudo bash -c 'echo "/export/volumes  *(rw,no_root_squash,no_subtree_check)" > /etc/exports'
cat /etc/exports
sleep 2
sudo systemctl restart nfs-kernel-server.service
```
# worker nodes

From the control plane, run ```kubeadm token create --print-join-command > /joincluster.sh``` to create a script for worker node to join it. 

```bash
# Join worker nodes to the Kubernetes cluster
sudo apt-get install -q -y sshpass >/dev/null 2>&1
sshpass -p "vagrant" scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no vagrant@c1-cp1.example.com:/joincluster.sh /joincluster.sh
bash /joincluster.sh >/dev/null 2>&1

# Join worker nodes to the Kubernetes cluster
echo "[TASK 2] Install NFS client"
sudo apt install -y nfs-common
```

