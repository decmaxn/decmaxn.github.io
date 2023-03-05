---
title: "Build K8s Cluster 1 Control Plan"
date: 2023-03-03T13:40:24-05:00
draft: false
tags: ["K8s","course"]
---

Here are steps from a training course long time ago to install configure K8s control plane:

1. control plan hostname is c1-cp1, other nodes will be c1-node# and c1-storage
1. control plan IP is 172.16.94.10, other nodes will be 11, 12....
1. the pod network is 172.172.0.0/16 to not overlay with my lap network.
1. All nodes have user vagrant for install, configure and maintain k8s cluster

# Common install and config for all cluster nodes
```bash
# Linux 文件系统层叠内核模块,将多个文件系统合并成一个只读文件系统，并在其上添加一个可写层
sudo modprobe overlay
# Linux 网络地址转换（NAT）和 IP 数据包过滤器内核模块，允许容器与宿主机和其他容器之间进行网络通信
sudo modprobe br_netfilter
cat <<EOF | sudo tee /etc/modules-load.d/containerd.conf >/dev/null
overlay
br_netfilter
EOF

# Add sysctl settings 内核参数（Kernel Parameters）
cat <<EOF | sudo tee /etc/sysctl.d/99-kubernetes-cri.conf >/dev/null
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF
# 在不需要重启系统的情况下重新加载 /etc/sysctl.conf 和 /etc/sysctl.d 文件中的所有设置
sudo sysctl --system >/dev/null 2>&1

# Disable swap
sed -i '/swap/d' /etc/fstab
swapoff -a

# Install the latest containerd using apt package
sudo apt-get update -q >/dev/null
sudo apt-get install -q -y containerd >/dev/null

# Enable containerd service
sudo mkdir -p /etc/containerd
sudo containerd config default | sudo tee /etc/containerd/config.toml >/dev/null

# Set the cgroup driver for containerd to systemd, because ubuntu is systemd system
# 使用 cgroup driver，容器可以在系统中独立地运行和使用资源，而不会对其他容器或宿主机造成干扰
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml
grep SystemdCgroup /etc/containerd/config.toml
sudo systemctl restart containerd

# Add Google's apt repository gpg key
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo bash -c 'cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF'
# Install Kubernetes 1.21 (kubeadm, kubelet and kubectl)
sudo apt-get -q update  >/dev/null
#Install the required packages, if needed we can request a specific version. 
#Use this version because in a later course we will upgrade the cluster to a newer version.
VERSION=1.21.0-00
sudo apt-get -q install -y kubelet=$VERSION kubeadm=$VERSION kubectl=$VERSION  >/dev/null
sudo apt-mark hold kubelet kubeadm kubectl containerd  >/dev/null

# Start and Enable kubelet and containerd services
sudo systemctl enable kubelet.service >/dev/null 2>&1
sudo systemctl enable containerd.service >/dev/null 2>&1
```
# Control Plane nodes
以上步骤需要在所有 kubernetes 节点里做， 下面只属于 control plane 节点

```bash
# Initialize Kubernetes with kubeadm command
kubeadm config print init-defaults | tee ClusterConfiguration.yaml >/dev/null
sed -i 's/  advertiseAddress: 1.2.3.4/  advertiseAddress: 172.16.94.10/' ClusterConfiguration.yaml
sed -i 's/  criSocket: \/var\/run\/dockershim\.sock/  criSocket: \/run\/containerd\/containerd\.sock/' ClusterConfiguration.yaml
sed -i 's/  name: node/  name: c1-cp1/' ClusterConfiguration.yaml
sed -i '/serviceSubnet: /a \  podSubnet: 172.172.0.0/16\' ClusterConfiguration.yaml

cat <<EOF | cat >> ClusterConfiguration.yaml
---
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
cgroupDriver: systemd
EOF

sudo kubeadm init \
    --config=ClusterConfiguration.yaml \
    --cri-socket /run/containerd/containerd.sock

# Copy Kube admin config prepare to use kubectl command for calico network
mkdir /home/vagrant/.kube
cp /etc/kubernetes/admin.conf /home/vagrant/.kube/config
chown -R vagrant:vagrant /home/vagrant/.kube

# Deploy calico network
echo "[TASK 3] Deploy calico network"
wget https://docs.projectcalico.org/manifests/calico.yaml >/dev/null 2>&1
su - vagrant -c "kubectl apply -f calico.yaml"

# Kubectl command completion. No need to do this on worker nodes since we use this control plane node as work bench.
sudo apt-get install -y bash-completion
echo "source <(kubectl completion bash)" >> ~/.bashrc
```