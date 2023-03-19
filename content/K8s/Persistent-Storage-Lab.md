---
title: "Persistent Storage"
date: 2023-03-17T10:56:17-04:00
draft: false
tags: ["K8s","course"]
---

# Containers are ephemeral, but can be persistent

It is persistent enough to be used for Database.

# API objects 

In Kubernetes, the "volume" is defined as part of the pod specification, which includes implementation details that may vary across different environments. In order to ensure that our Kubernetes declarative configuration file can be used across different environments, it is necessary to separate the implementation details from any specific environment.

## Volumes

part of the pod spec, which need to work in other env.

## Persistent Volumes

K8s Admin defined include implementation details of the specific K8s Cluster with API server. It is then mapped to the node by Kubelet.

It's lifecycle is independent of any pods. This is how data can be persistent after pod is gone.

It can be network as NFS, Block as Fiber Channnel or iSCSI, Cloud as AWS EBS.



## Persistent Volume Claims

## Storage Class

# Prepare NFS Server and Clients
Utilized a spare harddisk for NFS on 192.168.0.54 (it is also a worker node)
```bash
$ sudo lsblk -o NAME,FSTYPE,SIZE,MOUNTPOINT,LABEL,UUID /dev/sdb
NAME FSTYPE   SIZE MOUNTPOINT LABEL UUID
sdb         931.5G                
$ fdisk /dev/sdb
...
$ sudo lsblk -o NAME,FSTYPE,SIZE,MOUNTPOINT,LABEL,UUID /dev/sdb
NAME   FSTYPE   SIZE MOUNTPOINT LABEL UUID
sdb           931.5G                  
└─sdb1        931.5G       
$ mkfs -t ext4 /dev/sdb1
$ mount -t auto /dev/sdb1 /exports/
$ sudo lsblk -o NAME,FSTYPE,SIZE,MOUNTPOINT,LABEL,UUID /dev/sdb
NAME   FSTYPE   SIZE MOUNTPOINT LABEL UUID
sdb           931.5G                  
└─sdb1 ext4   931.5G /exports         fc67a7ee-fa14-4fb2-b4b3-41de54f4d681
$ vi /etc/fstab
$ grep  fc67a7ee-fa14-4fb2-b4b3-41de54f4d681 /etc/fstab
UUID=fc67a7ee-fa14-4fb2-b4b3-41de54f4d681 /exports               ext4   defaults 0       0
$ shutdown -r now
```
After reboot, verify you still have /exports mounted
```bash
$ mount | grep exports
/dev/sdb1 on /exports type ext4 (rw,relatime)
$ apt install nfs-kernel-server
$ mkdir /exports/volumes
$ mkdir /exports/volumes/pod
$ echo "/exports/volumes  *(rw,no_root_squash,no_subtree_check)" > /etc/exports
$ cat /etc/exports
/exports/volumes  *(rw,no_root_squash,no_subtree_check)
$ systemctl restart nfs-kernel-server.service
```
Install NFS client on each nodes and test mount
```bash
$ apt install nfs-common -y 
$ mount -t nfs4 192.168.0.54:/exports/volumes /mnt/
$ mount | grep nfs
$ umount /mnt
```