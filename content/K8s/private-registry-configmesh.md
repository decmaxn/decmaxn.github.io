---
title: "Private Registry Configmesh"
date: 2023-03-19T21:37:31-04:00
draft: false
tags: ["K8s","course"]
---

# Pulling a Container from a Private Container Registry
## Create a private image and prove it's private
```bash
$ sudo ctr images pull psk8s.azurecr.io/hello-app:1.0  
$ sudo ctr images tag psk8s.azurecr.io/hello-app:1.0 docker.io/decmaxn/test:1.0
docker.io/decmaxn/test:1.0
$ sudo ctr images push docker.io/decmaxn/test:1.0 --user decmaxn
Password: 
manifest-sha256:a3af38fd5a7dbfe9328f71b00d04516e8e9c778b4886e8aaac8d9e8862a09bc7: done           |++++++++++++++++++++++++++++++++++++++| 
config-sha256:7f20d355455edaaad01555f1a9520782675cf7b228ffd0527fb1349626b0ddb1:   done           |++++++++++++++++++++++++++++++++++++++| 
elapsed: 12.7s                                                                    total:  2.2 Ki (179.0 B/s)     
$ sudo ctr images pull docker.io/decmaxn/test:1.0 
docker.io/decmaxn/test:1.0: resolving      |--------------------------------------| 
elapsed: 0.2 s              total:   0.0 B (0.0 B/s)                                         
INFO[0000] trying next host                              error="pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed" host=registry-1.docker.io
ctr: failed to resolve reference "docker.io/decmaxn/test:1.0": pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed
```
A special type of secret for kubelet to pull image from private docker registry
```bash
$ kubectl create secret docker-registry private-reg-cred \
>     --docker-server=https://index.docker.io/v2/ \
>     --docker-username=$USERNAME \
>     --docker-password=$PASSWORD \
>     --docker-email=$EMAIL
secret/private-reg-cred created
$ cat <<EOF > deploy-secret-private-registry.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-private-registry
spec:
  replicas: 1
  selector:
    matchLabels:
      app: test-private-registry
  template:
    metadata:
      labels:
        app: test-private-registry
    spec:
      containers:
      - name: test
        image: decmaxn/test:1.0
        ports:
          - containerPort: 8080
      imagePullSecrets:
      - name: private-reg-cred
EOF
$ kubectl apply -f deploy-secret-private-registry.yaml 
deployment.apps/test-private-registry created
$ kubectl describe po  test-private-registry-9fcbdd7ff-bn6jc | tail -8
Events:
  Type    Reason     Age    From               Message
  ----    ------     ----   ----               -------
  Normal  Scheduled  2m24s  default-scheduler  Successfully assigned default/test-private-registry-9fcbdd7ff-bn6jc to k8s-53
  Normal  Pulling    2m23s  kubelet            Pulling image "decmaxn/test:1.0"
  Normal  Pulled     2m22s  kubelet            Successfully pulled image "decmaxn/test:1.0" in 946.173162ms (946.186468ms including waiting)
  Normal  Created    2m22s  kubelet            Created container test
  Normal  Started    2m22s  kubelet            Started container test
```

# ConfigMaps
It has to exist before pod can be started

## Create them from literal or from file
```bash
$ kubectl create configmap appconfigprod \
>     --from-literal=DATABASE_SERVERNAME=sql.example.local \
>     --from-literal=BACKEND_SERVERNAME=be.example.local
configmap/appconfigprod created
$ cat <<EOF > appconfigqa
> DATABASE_SERVERNAME="sqlqa.example.local"
> BACKEND_SERVERNAME="beqa.example.local"
> EOF
$ kubectl create configmap appconfigqa --from-file appconfigqa 
configmap/appconfigqa created

$ kubectl get configmaps appconfigprod -o yaml
apiVersion: v1
data:
  BACKEND_SERVERNAME: be.example.local
  DATABASE_SERVERNAME: sql.example.local
kind: ConfigMap
metadata:
  creationTimestamp: "2023-03-20T02:25:31Z"
  name: appconfigprod
  namespace: default
  resourceVersion: "1390103"
  uid: ea8c9c8c-53b2-4d82-a7cd-f6e3674ad09c

$ kubectl get configmaps appconfigqa -o yaml
apiVersion: v1
data:
  appconfigqa: |   # different with one above created imperitively
    DATABASE_SERVERNAME="sqlqa.example.local"
    BACKEND_SERVERNAME="beqa.example.local"
kind: ConfigMap
metadata:
  creationTimestamp: "2023-03-20T02:27:56Z"
  name: appconfigqa
  namespace: default
  resourceVersion: "1390338"
  uid: cb433294-0310-44ca-b16f-55416cc7f577
```
## Utilize them by env var or Volume
env var: valueFrom or envFrom  
volume: this way the configMaps can be updated without terminate the pod

envFrom:
```bash
vma@hpeb:~/decmaxn.github.io$ cat <<EOF > deployment-configmaps-env-prod.yaml
> apiVersion: apps/v1
> kind: Deployment
> metadata:
>   name: hello-world-configmaps-env-prod
> spec:
>   replicas: 1
>   selector:
>     matchLabels:
>       app: hello-world-configmaps-env-prod
>   template:
>     metadata:
>       labels:
>         app: hello-world-configmaps-env-prod
>     spec:
>       containers:
>       - name: hello-world
>         image: psk8s.azurecr.io/hello-app:1.0
>         envFrom:
>           - configMapRef:
>               name: appconfigprod
>         ports:
>         - containerPort: 8080
> EOF
vma@hpeb:~/decmaxn.github.io$ kubectl apply -f deployment-configmaps-env-prod.yaml 
deployment.apps/hello-world-configmaps-env-prod created
vma@hpeb:~/decmaxn.github.io$ kubectl get pod
NAME                                              READY   STATUS    RESTARTS   AGE
hello-world-configmaps-env-prod-8b7d6c9f4-z86cn   1/1     Running   0          11s
vma@hpeb:~/decmaxn.github.io$ kubectl exec -it hello-world-configmaps-env-prod-8b7d6c9f4-z86cn -- printenv | grep SERVERNAME
DATABASE_SERVERNAME=sql.example.local
BACKEND_SERVERNAME=be.example.local
```
volume:
```bash
vma@hpeb:~/decmaxn.github.io$ cat <<EOF > deployment-configmaps-directory-qa.yaml
> apiVersion: apps/v1
> kind: Deployment
> metadata:
>   name: hello-world-configmaps-files-qa
> spec:
>   replicas: 1
>   selector:
>     matchLabels:
>       app: hello-world-configmaps-files-qa
>   template:
>     metadata:
>       labels:
>         app: hello-world-configmaps-files-qa
>     spec:
>       volumes:
>         - name: appconfig
>           configMap:
>             name: appconfigqa
>       containers:
>       - name: hello-world
>         image: psk8s.azurecr.io/hello-app:1.0
>         ports:
>         - containerPort: 8080
>         volumeMounts:
>           - name: appconfig
>             mountPath: "/etc/appconfig"
> EOF
vma@hpeb:~/decmaxn.github.io$ kubectl exec -it hello-world-configmaps-files-qa-7f977cccd4-t7pfd -- /bin/sh
/app # ls /etc/appconfig/
appconfigqa
/app # cat /etc/appconfig/appconfigqa 
DATABASE_SERVERNAME="sqlqa.example.local"
BACKEND_SERVERNAME="beqa.example.local"
/app # exit
```
If you ```kubectl edit configmaps appconfigqa``` and modify the key pairs, the above file will change in a mintue or so.


If you create a configmap over a folder and use volume map, the whole folder is mounted.
```bash
$ ls configs/
httpd.conf  ssl.conf
$ cat configs/httpd.conf 
A complex HTTPD configuration
$ kubectl create configmap httpdconfigprod1 --from-file=./configs/

$ kubectl get configmaps httpdconfigprod1 -o yaml
apiVersion: v1
data:
  httpd.conf: |
    A complex HTTPD configuration
  ssl.conf: |
    All of our SSL configurations settings
kind: ConfigMap
metadata:
  creationTimestamp: "2023-03-20T02:54:26Z"
  name: httpdconfigprod1
  namespace: default
  resourceVersion: "1393009"
  uid: 21b01e56-a57f-42ec-a4a2-55e71f156c39

$ kubectl exec -it hello-world-configmaps-directory-qa-65646dc745-xlvnn -- /bin/sh
/app # ls /etc/httpd
httpd.conf  ssl.conf
/app # cat /etc/httpd/httpd.conf 
A complex HTTPD configuration
```

You can also reate a configmap over a file and use volume map, the file with the name as THE configmap name is inside the mounted folder.
```bash
$ cat appconfigprod 
DATABASE_SERVERNAME="sql.example.local"
BACKEND_SERVERNAME="be.example.local"$ kubectl create configmap appconfigprod1 --from-file=app1=appconfigprod
$ kubectl get configmap appconfigprod1 -o yaml
apiVersion: v1
data:
  app1: |-
    DATABASE_SERVERNAME="sql.example.local"
    BACKEND_SERVERNAME="be.example.local"
kind: ConfigMap
metadata:
  creationTimestamp: "2023-03-20T03:04:22Z"
  name: appconfigprod1
  namespace: default
  resourceVersion: "1394018"
  uid: 4edb931c-cdb3-4a69-87cd-0442f758543f

/app # ls /etc/appconfig
app1
/app # ls /etc/appconfig/app1
/etc/appconfig/app1
/app # cat /etc/appconfig/app1
DATABASE_SERVERNAME="sql.example.local"
BACKEND_SERVERNAME="be.example.local"/app # exit
```