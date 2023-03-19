---
title: "Persistent Volumes Test"
date: 2023-03-18T13:34:10-04:00
draft: false
tags: ["K8s","course"]
---

# Static Provisioning and storage lifecycle
Create a PV with the read/write many and retain as the reclaim policy
```bash
$ cat <<EOF > nfs.pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-nfs-data
spec:
  accessModes:
    - ReadWriteMany
  capacity:
    storage: 10Gi
  persistentVolumeReclaimPolicy: Retain
  nfs:
    server: 192.168.0.54
    path: "/exports/volumes/pod"
EOF
$ kubectl apply -f nfs.pv.yaml 
persistentvolume/pv-nfs-data created
$ kubectl get pv # note the status is Avaialble, and there is no CLAIM
NAME          CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   STORAGECLASS   REASON   AGE
pv-nfs-data   10Gi       RWX            Retain           Available                                   12s
$ kubectl describe PersistentVolume pv-nfs-data 
Name:            pv-nfs-data
Labels:          <none>
Annotations:     <none>
Finalizers:      [kubernetes.io/pv-protection]
StorageClass:    
Status:          Available
Claim:           
Reclaim Policy:  Retain
Access Modes:    RWX
VolumeMode:      Filesystem
Capacity:        10Gi
Node Affinity:   <none>
Message:         
Source:
    Type:      NFS (an NFS mount that lasts the lifetime of a pod)
    Server:    192.168.0.54
    Path:      /exports/volumes/pod
    ReadOnly:  false
Events:        <none>
```
A PVC is used to claim storage resources from a PV. In order for the PVC to bind to a PV, the PV must meet the PVC's requirements. If multiple PVs are available and meet the requirements of the PVC, the Kubernetes control plane will choose one of them to bind to the PVC.
```bash
$ cat <<EOF > nfs.pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-nfs-data
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 10Gi
EOF
$ kubectl apply -f nfs.pvc.yaml
persistentvolumeclaim/pvc-nfs-data created

$ kubectl get pv # note the status is Bound now
NAME          CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                  STORAGECLASS   REASON   AGE
pv-nfs-data   10Gi       RWX            Retain           Bound    default/pvc-nfs-data                           3m45s

$ kubectl get pvc
NAME           STATUS   VOLUME        CAPACITY   ACCESS MODES   STORAGECLASS   AGE
pvc-nfs-data   Bound    pv-nfs-data   10Gi       RWX                           7s
$ kubectl describe pvc pvc-nfs-data 
Name:          pvc-nfs-data
Namespace:     default
StorageClass:  
Status:        Bound
Volume:        pv-nfs-data
Labels:        <none>
Annotations:   pv.kubernetes.io/bind-completed: yes
               pv.kubernetes.io/bound-by-controller: yes
Finalizers:    [kubernetes.io/pvc-protection]
Capacity:      10Gi
Access Modes:  RWX
VolumeMode:    Filesystem
Used By:       <none>
Events:        <none>
```
Creat some data in the NFS share.
```bash
ssh 192.168.0.54
sudo bash -c 'echo "Hello from our NFS mount!!!" > /exports/volumes/pod/demo.html'
cat /exports/volumes/pod/demo.html
exit
```
Read the exiting data from a pod
```bash
$ cat <<EOF >nfs.nginx.yaml
> apiVersion: apps/v1
> kind: Deployment
> metadata:
>   name: nginx-nfs-deployment
> spec:  
>   replicas: 1
>   selector:
>     matchLabels:
>       app: nginx
>   template:
>     metadata:
>       labels:
>         app: nginx
>     spec:
>       volumes:
>       - name: webcontent
>         persistentVolumeClaim:
>           claimName: pvc-nfs-data
>       containers:
>       - name: nginx
>         image: nginx
>         ports:
>         - containerPort: 80
>         volumeMounts:
>         - name: webcontent
>           mountPath: "/usr/share/nginx/html/web-app"
> EOF
$ kubectl apply -f nfs.nginx.yaml 
deployment.apps/nginx-nfs-deployment created
$ kubectl get pod
NAME                                   READY   STATUS    RESTARTS   AGE
nginx-nfs-deployment-b69b64f9b-7zqvp   1/1     Running   0          2m33s
$ kubectl exec -it nginx-nfs-deployment-b69b64f9b-7zqvp -- /bin/cat /usr/share/nginx/html/web-app/demo.html
Hello from our NFS mount!!!
```
how it works under the hood? The Node has the POD has this volume as well, but the other nodes don't.
```bash
$ kubectl get po -o wide
NAME                                   READY   STATUS    RESTARTS   AGE   IP               NODE     NOMINATED NODE   READINESS GATES
nginx-nfs-deployment-b69b64f9b-7zqvp   1/1     Running   0          32m   172.172.81.225   k8s-53   <none>           <none>

$ ssh 53
vma@k8s-53:~$ mount | grep exports
192.168.0.54:/exports/volumes/pod on /var/lib/kubelet/pods/57388361-b049-4eb3-83fe-b4737342de6c/volumes/kubernetes.io~nfs/pv-nfs-data type nfs4 (rw,relatime,vers=4.2,rsize=1048576,wsize=1048576,namlen=255,hard,proto=tcp,timeo=600,retrans=2,sec=sys,clientaddr=192.168.0.53,local_lock=none,addr=192.168.0.54)
vma@k8s-53:~$ sudo cat /var/lib/kubelet/pods/57388361-b049-4eb3-83fe-b4737342de6c/volumes/kubernetes.io~nfs/pv-nfs-data/demo.html
Hello from our NFS mount!!!
vma@k8s-53:~$ exit
```
Delete the existing pod and the new pod will have it, scale does the same
```bash
$ kubectl delete pod nginx-nfs-deployment-b69b64f9b-7zqvp 
pod "nginx-nfs-deployment-b69b64f9b-7zqvp" deleted
$ kubectl get pod
NAME                                   READY   STATUS    RESTARTS   AGE
nginx-nfs-deployment-b69b64f9b-pdlqt   1/1     Running   0          11s
$ kubectl exec -it nginx-nfs-deployment-b69b64f9b-pdlqt  -- /bin/cat /usr/share/nginx/html/web-app/demo.html
Hello from our NFS mount!!!

$ kubectl scale deployment nginx-nfs-deployment --replicas 3
deployment.apps/nginx-nfs-deployment scaled
$ kubectl get pod
NAME                                   READY   STATUS              RESTARTS   AGE
nginx-nfs-deployment-b69b64f9b-bf64x   1/1     Running             0          11s
nginx-nfs-deployment-b69b64f9b-pdlqt   1/1     Running             0          3m
nginx-nfs-deployment-b69b64f9b-sdfjm   0/1     ContainerCreating   0          11s
$ kubectl exec -it nginx-nfs-deployment-b69b64f9b-bf64x  -- /bin/cat /usr/share/nginx/html/web-app/demo.html
Hello from our NFS mount!!!
$ kubectl exec -it nginx-nfs-deployment-b69b64f9b-sdfjm  -- /bin/cat /usr/share/nginx/html/web-app/demo.html
Hello from our NFS mount!!!
```
## Reclaim policy as Retain
If we don't delete the pvc, new pods can attach to it.
```bash
$ kubectl delete deployments.apps nginx-nfs-deployment 
deployment.apps "nginx-nfs-deployment" deleted
$ kubectl get pv  # Still Bound because the pvc is still there.
NAME          CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                  STORAGECLASS   REASON   AGE
pv-nfs-data   10Gi       RWX            Retain           Bound    default/pvc-nfs-data                           60m
$ kubectl get pvc
NAME           STATUS   VOLUME        CAPACITY   ACCESS MODES   STORAGECLASS   AGE
pvc-nfs-data   Bound    pv-nfs-data   10Gi       RWX                           57m
$ kubectl apply -f nfs.nginx.yaml 
deployment.apps/nginx-nfs-deployment created
$ kubectl get po
NAME                                   READY   STATUS    RESTARTS   AGE
nginx-nfs-deployment-b69b64f9b-87ktk   1/1     Running   0          25s
$ kubectl exec -it nginx-nfs-deployment-b69b64f9b-87ktk  -- /bin/cat /usr/share/nginx/html/web-app/demo.html
Hello from our NFS mount!!!
```
If we deleted the pvc, the PV can't be just reclaimed again
```bash
$ kubectl delete deployments.apps nginx-nfs-deployment 
deployment.apps "nginx-nfs-deployment" deleted
$ kubectl delete pvc pvc-nfs-data 
persistentvolumeclaim "pvc-nfs-data" deleted
$ kubectl get pv # IF we delete the pvc, pv is Released
NAME          CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS     CLAIM                  STORAGECLASS   REASON   AGE
pv-nfs-data   10Gi       RWX            Retain           Released   default/pvc-nfs-data                           62m
$ kubectl apply -f nfs.pvc.yaml
persistentvolumeclaim/pvc-nfs-data created
$ kubectl get pvc # For this released pv, you can't just claim it again,(pending) it has to be clean up first.
NAME           STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
pvc-nfs-data   Pending                                                     12s
$ kubectl apply -f nfs.nginx.yaml 
deployment.apps/nginx-nfs-deployment created
$ kubectl get po # if pvc is pending, so is the pod which is depend on the pvc
NAME                                   READY   STATUS    RESTARTS   AGE
nginx-nfs-deployment-b69b64f9b-bn9gv   0/1     Pending   0          15s
```
The pv needs to be manually clean up (deleted) before it can be claimed again. 
```bash
$ kubectl delete deployment nginx-nfs-deployment
ectl delete pvc pvc-nfs-data
kubectl delete pv pv-nfs-datadeployment.apps "nginx-nfs-deployment" deleted
$ kubectl delete pvc pvc-nfs-data
persistentvolumeclaim "pvc-nfs-data" deleted
$ kubectl delete pv pv-nfs-data
persistentvolume "pv-nfs-data" deleted

$ kubectl apply -f nfs.pv.yaml
kubectl get pods persistentvolume/pv-nfs-data created
$ kubectl apply -f nfs.pvc.yaml
persistentvolumeclaim/pvc-nfs-data created
$ kubectl apply -f nfs.nginx.yaml
deployment.apps/nginx-nfs-deployment created
$ kubectl get pods 
NAME                                   READY   STATUS    RESTARTS   AGE
nginx-nfs-deployment-b69b64f9b-4vnhg   1/1     Running   0          33ss

$  kubectl exec -it nginx-nfs-deployment-b69b64f9b-cfbpd  -- /bin/cat /usr/share/nginx/html/web-app/demo.html
Hello from our NFS mount!!!
```
Retain means the data is important, and K8s won't automatically clean it up.

# Dynamic Provisioning with Storage Class

