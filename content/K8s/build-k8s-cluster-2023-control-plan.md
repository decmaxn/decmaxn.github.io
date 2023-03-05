---
title: "Build K8s Cluster 2023 Control Plan"
date: 2023-03-05T16:54:54-05:00
draft: false
tags: ["K8s","course"]
---

This is with the same requirment, an updated version of [Build K8s Cluster 1 Control Plan](../build-k8s-cluster-1-control-plan), which is tested on Ubuntu 20.04 LTS.

# Common install and config for all cluster nodes
```bash
# Load two modules and configure them to load on boot
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

# Disable swap - actuqally disabled by vagrant already
sed -i '/swap/d' /etc/fstab
swapoff -a

# Install containerd...we need to install from the docker repo to get containerd 1.6, the ubuntu repo stops at 1.5.9
# 用GPG 工具将下载的密钥进行解析（解码），并将其保存GPG 工具将下载的密钥进行解析（解码），并将其保存
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/trusted.gpg.d/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update -q >/dev/null
sudo apt-get install -q -y containerd.io >/dev/null
containerd --version

# Enable containerd service
sudo mkdir -p /etc/containerd
sudo containerd config default | sudo tee /etc/containerd/config.toml >/dev/null

# 使用 cgroup driver，容器可以在系统中独立地运行和使用资源，而不会对其他容器或宿主机造成干扰
#Set the cgroup driver for containerd to systemd which is required for the kubelet.
#For more information on this config file see:
# https://github.com/containerd/cri/blob/master/docs/config.md and also
# https://github.com/containerd/containerd/blob/master/docs/ops.md

# Set the cgroup driver for containerd to systemd, because ubuntu is systemd system
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml
grep SystemdCgroup /etc/containerd/config.toml
sudo systemctl restart containerd

# Add Google's apt repository gpg key
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo bash -c 'cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF'

# Install Kubernetes
sudo apt-get -q update  >/dev/null
#Install the required packages, if needed we can request a specific version. 
# apt-cache policy kubelet | head -n 20 
#Use this version because in a later course we will upgrade the cluster to a newer version.
VERSION=1.26.0-00
sudo apt-get -q install -y kubelet=$VERSION kubeadm=$VERSION kubectl=$VERSION  >/dev/null
sudo apt-mark hold kubelet kubeadm kubectl containerd  >/dev/null

# Start and Enable kubelet and containerd services
#The kubelet will enter a crashloop until a cluster is created or the node is joined to an existing cluster.
# sudo systemctl status kubelet.service 
# sudo systemctl status containerd.service 
sudo systemctl enable kubelet.service >/dev/null 2>&1
sudo systemctl enable containerd.service >/dev/null 2>&1
```
# Control Plane nodes
以上步骤需要在所有 kubernetes 节点里做， 下面只属于 control plane 节点
```bash
#Generate a default kubeadm init configuration file...this defines the settings of the cluster being built.
#If you get a warning about how docker is not installed...this is OK to ingore and is a bug in kubeadm
#For more info on kubeconfig configuration files see: 
#    https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init/#config-file
kubeadm config print init-defaults | tee ClusterConfiguration.yaml >/dev/null

#Change the address of the localAPIEndpoint.advertiseAddress to the Control Plane Node's IP address
sed -i 's/  advertiseAddress: 1.2.3.4/  advertiseAddress: 172.16.94.10/' ClusterConfiguration.yaml
#Set the CRI Socket to point to containerd, I found in 1.26 it's already containerd, but it'sn't hurt
sed -i 's/  criSocket: \/var\/run\/dockershim\.sock/  criSocket: \/run\/containerd\/containerd\.sock/' ClusterConfiguration.yaml
# Added configuration to set the node name for the control plane node to the actual hostname
sed -i 's/  name: node/  name: c1-cp1/' ClusterConfiguration.yaml
# Change the pod Subnet from the default 192.168.0.0 to not overlap with your host network in case it's
sed -i '/serviceSubnet: /a \  podSubnet: 172.172.0.0/16\' ClusterConfiguration.yaml

cat <<EOF | cat >> ClusterConfiguration.yaml
---
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
cgroupDriver: systemd
EOF

sudo kubeadm init --config=ClusterConfiguration.yaml
#Need to add CRI socket since there's a check for docker in the kubeadm init process, 
#if you don't you'll get this error...
#   error execution phase preflight: docker is required for container runtime: exec: "docker": executable file not found in $PATH
# However, this is no longer the case for 1.26 version.
    # --cri-socket /run/containerd/containerd.sock
# The pod-network-cidr should not be overlapped with any of the host networks
# 如果在 kubeadm init 初始化集群时指定了 --pod-network-cidr，则 Calico 将使用此 CIDR 作为 IP 地址池
# This will solve the calico pods fails to start with error not able to reach out to 10.96.0.x(which is the service/kubernetes's Cluster-IP)
# but you "can not mix '--config' with arguments [pod-network-cidr]".
# So I have put the equivlent line into ClusterConfiguration.yaml which --config calls.
    # --pod-network-cidr=172.172.0.0/16 

# Copy Kube admin config
mkdir /home/vagrant/.kube
cp /etc/kubernetes/admin.conf /home/vagrant/.kube/config
chown -R vagrant:vagrant /home/vagrant/.kube

# Deploy calico network
wget  https://raw.githubusercontent.com/projectcalico/calico/master/manifests/calico.yaml >/dev/null 2>&1
su - vagrant -c "kubectl apply -f calico.yaml"

# Generate Cluster join command
kubeadm token create --print-join-command > /joincluster.sh

# Kubectl command completion. No need to do this on worker nodes since we use this control plane node as work bench.
sudo apt-get install -y bash-completion
echo "source <(kubectl completion bash)" >> ~/.bashrc
```