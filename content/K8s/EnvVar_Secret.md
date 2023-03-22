---
title: "EnvVar_Secret"
date: 2023-03-19T20:21:11-04:00
draft: false
tags: ["K8s","course"]
---

# Environment Variable

They are injected to the pod when it is started, and stay there even if they disapear. They only get updated when new pod is started.

# Secrets

It's saved in etcd, and NOT encrypted by default.

It's namespaced, and only available for this namespace.

Unavailable secrets will prevent a pod from starting up.

## Create and verify

```bash
$ kubectl create secret generic app1 \
>     --from-literal=USERNAME=app1login \
>     --from-literal=PASSWORD='S0methingS@Str0ng!'
secret/app1 created
$ kubectl get secrets 
NAME         TYPE     DATA   AGE
app1         Opaque   2      9s 
# 2 DATA? Yes, they are PASSWORD and USERNAME
$ kubectl describe secrets app1 
Name:         app1
Namespace:    default
Labels:       <none>
Annotations:  <none>

Type:  Opaque

Data
====
PASSWORD:  18 bytes
USERNAME:  9 bytes
$ kubectl get secrets app1 --output json
{
    "apiVersion": "v1",
    "data": {
        "PASSWORD": "UzBtZXRoaW5nU0BTdHIwbmch",
        "USERNAME": "YXBwMWxvZ2lu"
    },
    "kind": "Secret",
    "metadata": {
        "creationTimestamp": "2023-03-20T00:37:27Z",
        "name": "app1",
        "namespace": "default",
        "resourceVersion": "1379106",
        "uid": "a34af034-007f-43ed-9634-b29f2446c86a"
    },
    "type": "Opaque"
}
$ \
> echo $(kubectl get secrets app1 --output json | jq -r .data.PASSWORD  | base64 --decode)
S0methingS@Str0ng!
$ \
> echo $(kubectl get secrets app1 --output json | jq -r .data.USERNAME  | base64 --decode)
app1login
```

## Utilize
From env var
```bash
$ cat <<EOF > deploy-secret.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-world-secrets-env
spec:
  replicas: 1
  selector:
    matchLabels:
      app: hello-world-secrets-env
  template:
    metadata:
      labels:
        app: hello-world-secrets-env
    spec:
      containers:
      - name: hello-world
        image: psk8s.azurecr.io/hello-app:1.0
        env:
        - name: app1username
          valueFrom:
            secretKeyRef:
              name: app1
              key: USERNAME 
        - name: app1password
          valueFrom:
            secretKeyRef:
              name: app1
              key: PASSWORD 
        ports:
        - containerPort: 8080
EOF
$ kubectl apply -f deploy-secret.yaml 
deployment.apps/hello-world-secrets-env created
$ PODNAME=$(kubectl get pods | grep hello-world-secrets-env | awk '{print $1}' | head -n 1)
$ kubectl exec -it $PODNAME -- printenv | grep ^app1
app1username=app1login
app1password=S0methingS@Str0ng!
```
From volume
```bash
$ cat <<EOF > deploy-secret-vol.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-world-secrets-files
spec:
  replicas: 1
  selector:
    matchLabels:
      app: hello-world-secrets-files
  template:
    metadata:
      labels:
        app: hello-world-secrets-files
    spec:
      volumes:
        - name: appconfig
          secret:
            secretName: app1
      containers:
      - name: hello-world
        image: psk8s.azurecr.io/hello-app:1.0
        ports:
        - containerPort: 8080
        volumeMounts:
          - name: appconfig
            mountPath: "/etc/appconfig"
EOF
$ kubectl apply -f deploy-secret-vol.yaml 
deployment.apps/hello-world-secrets-files created
$ PODNAME=$(kubectl get pods | grep hello-world-secrets-files | awk '{print $1}' | head -n 1)

$ kubectl exec -it $PODNAME -- /bin/sh
/etc/appconfig # cd /etc/appconfig ; ls 
PASSWORD  USERNAME
/etc/appconfig # cat USERNAME 
app1login/etc/appconfig # cat PASSWORD
S0methingS@Str0ng!/etc/appconfig # exit
```
envFrom:
```bash
$ cat <<EOF > deploy-secret-envfrom.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-world-secrets-env-from
spec:
  replicas: 1
  selector:
    matchLabels:
      app: hello-world-secrets-env-from
  template:
    metadata:
      labels:
        app: hello-world-secrets-env-from
    spec:
      containers:
      - name: hello-world
        image: psk8s.azurecr.io/hello-app:1.0
        envFrom:
        - secretRef:
            name: app1
        ports:
        - containerPort: 8080
EOF
$ kubectl apply -f deploy-secret-envfrom.yaml 
deployment.apps/hello-world-secrets-env-from created
$ PODNAME=$(kubectl get pods | grep hello-world-secrets-env-from | awk '{print $1}' | head -n 1)
$ kubectl exec -it $PODNAME -- printenv | grep -E 'USERNAME|PASSWORD'
PASSWORD=S0methingS@Str0ng!
USERNAME=app1login
```