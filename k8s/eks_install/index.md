# Eks_install


# Install eksctl and kubectl
[eksctl.io](https://eksctl.io/introduction/?h=#installation)
```bash
$ curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
$ sudo mv /tmp/eksctl ~/.local/bin/
$ eksctl version
0.133.0
$ . <(eksctl completion bash)
```
[Amazon EKS](https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html)
```bash
$ curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.25.6/2023-01-30/bin/linux/amd64/kubectl
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 42.9M  100 42.9M    0     0  2295k      0  0:00:19  0:00:19 --:--:-- 3581k
$ mv kubectl ~/.local/bin/
$ chmod a+x ~/.local/bin/kubectl 
```
# Create an EKS cluster

```bash
$ eksctl get --profile dec --region us-east-1 cluster 
No clusters found

$ eksctl create --profile dec --region us-east-1 cluster --name wp-cluster
:10:58 [ℹ]  eksctl version 0.133.0
:10:58 [ℹ]  using region us-east-1
:10:59 [ℹ]  setting availability zones to [us-east-1d us-east-1a]
:10:59 [ℹ]  subnets for us-east-1d - public:192.168.0.0/19 private:192.168.64.0/19
:10:59 [ℹ]  subnets for us-east-1a - public:192.168.32.0/19 private:192.168.96.0/19
:10:59 [ℹ]  nodegroup "ng-c3af3c25" will use "" [AmazonLinux2/1.24]
:10:59 [ℹ]  using Kubernetes version 1.24
:10:59 [ℹ]  creating EKS cluster "wp-cluster" in "us-east-1" region with managed nodes
:10:59 [ℹ]  will create 2 separate CloudFormation stacks for cluster itself and the initial managed nodegroup
:10:59 [ℹ]  if you encounter any issues, check CloudFormation console or try 'eksctl utils describe-stacks --region=us-east-1 --cluster=wp-cluster'
:10:59 [ℹ]  Kubernetes API endpoint access will use default of {publicAccess=true, privateAccess=false} for cluster "wp-cluster" in "us-east-1"
:10:59 [ℹ]  CloudWatch logging will not be enabled for cluster "wp-cluster" in "us-east-1"
:10:59 [ℹ]  you can enable it with 'eksctl utils update-cluster-logging --enable-types={SPECIFY-YOUR-LOG-TYPES-HERE (e.g. all)} --region=us-east-1 --cluster=wp-cluster'
:10:59 [ℹ]  
2 sequential tasks: { create cluster control plane "wp-cluster", 
    2 sequential sub-tasks: { 
        wait for control plane to become ready,
        create managed nodegroup "ng-c3af3c25",
    } 
}
:10:59 [ℹ]  building cluster stack "eksctl-wp-cluster-cluster"
:10:59 [ℹ]  deploying stack "eksctl-wp-cluster-cluster"
:11:29 [ℹ]  waiting for CloudFormation stack "eksctl-wp-cluster-cluster"

:27:05 [ℹ]  building managed nodegroup stack "eksctl-wp-cluster-nodegroup-ng-c3af3c25"
:27:05 [ℹ]  deploying stack "eksctl-wp-cluster-nodegroup-ng-c3af3c25"
:27:05 [ℹ]  waiting for CloudFormation stack "eksctl-wp-cluster-nodegroup-ng-c3af3c25"

:31:35 [ℹ]  waiting for the control plane to become ready
:31:36 [✔]  saved kubeconfig as "/home/vma/.kube/config"
:31:36 [ℹ]  no tasks
:31:36 [✔]  all EKS cluster resources for "wp-cluster" have been created
:31:36 [ℹ]  nodegroup "ng-c3af3c25" has 2 node(s)
:31:36 [ℹ]  node "ip-192-168-14-169.ec2.internal" is ready
:31:36 [ℹ]  node "ip-192-168-61-46.ec2.internal" is ready
:31:36 [ℹ]  waiting for at least 2 node(s) to become ready in "ng-c3af3c25"
:31:36 [ℹ]  nodegroup "ng-c3af3c25" has 2 node(s)
:31:36 [ℹ]  node "ip-192-168-14-169.ec2.internal" is ready
:31:36 [ℹ]  node "ip-192-168-61-46.ec2.internal" is ready
:31:39 [ℹ]  kubectl command should work with "/home/vma/.kube/config", try 'kubectl get nodes'
:31:39 [✔]  EKS cluster "wp-cluster" in "us-east-1" region is ready

$ aws cloudformation --profile dec list-stacks --query 'StackSummaries[].StackName' | grep eksctl
    "eksctl-wp-cluster-nodegroup-ng-c3af3c25",
    "eksctl-wp-cluster-cluster",

$ kubectl config get-contexts 
CURRENT   NAME                                 CLUSTER                          AUTHINFO                             NAMESPACE
          local51                              kubernetes                       kubernetes-admin                     
*         vma@wp-cluster.us-east-1.eksctl.io   wp-cluster.us-east-1.eksctl.io   vma@wp-cluster.us-east-1.eksctl.io  

$ kubectl get nodes
NAME                             STATUS   ROLES    AGE     VERSION
ip-192-168-14-169.ec2.internal   Ready    <none>   3m27s   v1.24.10-eks-48e63af
ip-192-168-61-46.ec2.internal    Ready    <none>   3m26s   v1.24.10-eks-48e63af
```
# Deploy an example wordpress app
```bash
$ kubectl create secret generic mysql-pass --from-literal=password=mypassword
secret/mysql-pass created
$ kubectl get secrets 
NAME         TYPE     DATA   AGE
mysql-pass   Opaque   1      8s

$ curl https://kubernetes.io/examples/application/wordpress/mysql-deployment.yaml > mysql-deployment.yaml
$ curl https://kubernetes.io/examples/application/wordpress/wordpress-deployment.yaml > wordpress-deployment.yaml

$ kubectl create -f mysql-deployment.yaml 
service/wordpress-mysql created
persistentvolumeclaim/mysql-pv-claim created
deployment.apps/wordpress-mysql created
$ kubectl create -f wordpress-deployment.yaml 
service/wordpress created
persistentvolumeclaim/wp-pv-claim created
deployment.apps/wordpress created
```
Wait for it to complete, there is an error this time. I will do it again later.
```bash
$ kubectl get pod
NAME                               READY   STATUS    RESTARTS   AGE
wordpress-55c9ff4b54-wk76c         0/1     Pending   0          5s
wordpress-mysql-668d75584d-7jczl   0/1     Pending   0          15s
$ kubectl get pvc -o wide
NAME             STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE   VOLUMEMODE
mysql-pv-claim   Pending                                      gp2            40s   Filesystem
wp-pv-claim      Pending                                      gp2            30s   Filesystem
$ kubectl describe pvc mysql-pv-claim | tail -5
Events:
  Type    Reason                Age                 From                         Message
  ----    ------                ----                ----                         -------
  Normal  WaitForFirstConsumer  5m5s                persistentvolume-controller  waiting for first consumer to be created before binding
  Normal  ExternalProvisioning  5s (x22 over 5m5s)  persistentvolume-controller  waiting for a volume to be created, either by external provisioner "ebs.csi.aws.com" or manually created by system administrator
```
Verify(if it completes) by browse to http://aca09e50ff58e41a99c4254e385500c9-2052174023.us-east-1.elb.amazonaws.com
```bash
$ kubectl get svc
NAME              TYPE           CLUSTER-IP      EXTERNAL-IP                                                               PORT(S)        AGE
kubernetes        ClusterIP      10.100.0.1      <none>                                                                    443/TCP        21m
wordpress         LoadBalancer   10.100.82.183   aca09e50ff58e41a99c4254e385500c9-2052174023.us-east-1.elb.amazonaws.com   80:32039/TCP   6m39s
wordpress-mysql   ClusterIP      None            <none>                                                                    3306/TCP       6m49s
```

# Clean up
```bash
$ kubectl delete deployments.apps -l app=wordpress
deployment.apps "wordpress" deleted
deployment.apps "wordpress-mysql" deleted
$ kubectl delete service -l app=wordpress
service "wordpress" deleted
service "wordpress-mysql" deleted
$ kubectl delete pvc -l app=wordpress
persistentvolumeclaim "mysql-pv-claim" deleted
persistentvolumeclaim "wp-pv-claim" deleted
$ eksctl delete --profile dec --region us-east-1 cluster  --name wp-cluster
:46:35 [ℹ]  deleting EKS cluster "wp-cluster"
:46:36 [ℹ]  will drain 0 unmanaged nodegroup(s) in cluster "wp-cluster"
:46:36 [ℹ]  starting parallel draining, max in-flight of 1
:46:36 [ℹ]  deleted 0 Fargate profile(s)
:46:37 [✔]  kubeconfig has been updated
:46:37 [ℹ]  cleaning up AWS load balancers created by Kubernetes objects of Kind Service or Ingress
:46:38 [ℹ]  
2 sequential tasks: { delete nodegroup "ng-c3af3c25", delete cluster control plane "wp-cluster" [async] 
}
:46:38 [ℹ]  will delete stack "eksctl-wp-cluster-nodegroup-ng-c3af3c25"
:46:38 [ℹ]  waiting for stack "eksctl-wp-cluster-nodegroup-ng-c3af3c25" to get deleted
:46:38 [ℹ]  waiting for CloudFormation stack "eksctl-wp-cluster-nodegroup-ng-c3af3c25"

:55:24 [ℹ]  will delete stack "eksctl-wp-cluster-cluster"
:55:24 [✔]  all cluster resources were deleted

$ kubectl config current-context 
error: current-context is not set
$ kubectl config get-contexts 
CURRENT   NAME      CLUSTER      AUTHINFO           NAMESPACE
          local51   kubernetes   kubernetes-admin   
$ kubectl config use-context local51
Switched to context "local51".
$ kubectl config get-contexts 
CURRENT   NAME      CLUSTER      AUTHINFO           NAMESPACE
*         local51   kubernetes   kubernetes-admin   
$ kubectl get no
NAME     STATUS   ROLES           AGE   VERSION
cp1      Ready    control-plane   8d    v1.26.0
k8s-52   Ready    <none>          8d    v1.26.0
k8s-53   Ready    <none>          8d    v1.26.0
k8s-54   Ready    <none>          8d    v1.26.0
```
