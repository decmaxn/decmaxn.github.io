---
title: "Basic Docker Review Ecr"
date: 2023-06-12T00:25:50-04:00
draft: false
tags: ["Aws","Docker","tips"]
---


## Docker Basic
Follow [youtube](https://youtu.be/29WbHPDyRIs) "Containers Office Hours | S1 E3 – Build Your First Image and Store It in ECR" by Brent Langston and Nathan Peck.
Most of the following come from it's [github repo](https://github.com/brentley/docker-hello-world).

### Create a Hello World file and run locally
```bash
$ cat <<EOF >brentley_docker-hello-world_app.js
const express = require('express')
const app = express()
const port = 3000

app.get('/', (req, res) => res.send('Hello World!'))

app.listen(port, () => console.log(\`Example app listening on port \${port}!\`))
EOF
$ node brentley_docker-hello-world_app.js # will fail because no express npm
```
Let's install the express npm.
```bash
npm init -y
npm install express --save
```
This npm install command will create node_modules folder with a lot of packages, so I created a .gitignore file to avoid including them in this repo.

Now when we run the demo hello world app again, it should work
```
node brentley_docker-hello-world_app.js 
```
While it's running, I'll open a new terminal and curl to see the output
```
curl localhost:3000
```

### Dockerize our app
Let's take a look at what tags might be available:
https://hub.docker.com/_/centos
Now the whole repo is deprecated, but the tag is still [there](https://hub.docker.com/_/centos/tags?page=1&name=centos7.6.1810)

```bash
ContainerOfficeHoursS1E3$ docker build -t docker-hello-world:latest .
ContainerOfficeHoursS1E3$ docker images | grep docker-hello-world
docker-hello-world                                                                       latest     d61083ac153c   4 years ago     202MB
ContainerOfficeHoursS1E3$ docker run -it docker-hello-world:latest 
[root@9e4aef28af71 /]# head -1 /etc/os-release 
NAME="CentOS Linux"
```
Copy every files and run node, but notice we get an error.

It looks like we need to install NodeJS. After that, build successfully.
```bash
docker run --init -i -p 3000:3000 docker-hello-world:latest
```
Now let's try to curl our hello world app!
```
curl localhost:3000
```
You can also add the EXPOSE command to the Dockerfile, and then use the `-P` option
when running docker. This will expose our port to a dynamic/available high port on the host:
```
docker run --init -i -P docker-hello-world:latest
```

### Uh Oh... we kinda messed up...
In our Dockerfile, we have `COPY . .` and that copies everything from the directory
into the container. Normally that okay, but in this case, we had built/installed
Express locally, which installed into `node_modules`. While this worked, it's not
great design, because I can't always count on those modules being built, or even
being current.

A better design is to actually build the modules inside the container, so we can
ensure they are built every time. Also, we should add a .dockerignore file so if
we have built modules locally, they don't accidentally get copied into the container.
```
cat <<EOF>.dockerignore
.git
.gitignore
node_modules
EOF
```
After build again and run, there is an error of Error: Cannot find module 'express'. 

Now it works.


### Optimizing the container

Okay, it looks like we have a good container... but is it production worthy?
Let's talk about that... first, let's look at the size of the container:
```
$ docker images | grep docker-hello-world
docker-hello-world  latest     c22b804cc59f   2 minutes ago    500MB
```

How can we make this smaller? More efficient? you see our starting point is 202MB, but we've
grown this thing to 500MB, and our app code is only 3MB, so how did we add so much extra stuff?

- we combine all of our commands into one layer, so we can add and delete and
recover the space. (Layers are additive and immutable--if you add stuff in one layer
and delete it in a different layer, that stuff is still in the earlier layer. This is
analogous to adding a file in one git commit and deleting it in the next--it is still
in your git history.)
- since each container is immutable, we don't need to plan to install future
RPMs, so we can delete the RPMdb, and the yum cache (or all caches, for that matter).
- Not a space saver, but when it comes time to copy in our application, and run it,
we should drop priviledges to a regular user, rather than root. It's just good security practice.

```bash
$ docker images | grep docker-hello-world
docker-hello-world           latest     8f0a00bd56ad   33 seconds ago   269MB
```

### Optimizing the build order to take advantage of caching

There is another optimization we can do to optimize how much work needs to be done
if we change something in the app. Watch what happens if I change a line in app.js
and then rebuilt the container.

Did you see that it had to rerun the `npm install`? This is because Docker has to
rerun every command below the first command that has a changed file. That `COPY . .`
is copying both the `package.json` file and the `app.js` file so even if all I changed
was the `app.js` file it has to rerun the NPM install.

Now if I run this build I get an extra layer, but this layer lets Docker cache the
package.json and the installed dendencies separately from the app code. And
if I change a line in the `app.js` file and rerun the build you'll see that it is
able to skip the NPM install because nothing has changed in `package.json`

This is a huge boost to speed and productivity when working with Docker containers

### Use a container specific distribution

There is another distro that is super popular, called Alpine Linux. It's deisgned for containers.
the starting base image is 3MB. Let's see what it takes to use that image, instead.

```bash
$ docker build -t docker-hello-world:latest -f Dockerfile.alpine .

$ docker images | grep docker-hello-world
docker-hello-world            latest     4c51ab589a3a   10 seconds ago   53.7MB
```

### Pushing to Amazon ECR
I have an ECR repo already exist, which is ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/cdk-hnb659fds-container-assets-ACCOUNT_ID-us-east-1
```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
docker tag docker-hello-world:latest $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/cdk-hnb659fds-container-assets-$ACCOUNT_ID-us-east-1:latest
docker push $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/cdk-hnb659fds-container-assets-$ACCOUNT_ID-us-east-1:latest
```
Test it from another box after login with above commands.
```
docker pull $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/cdk-hnb659fds-container-assets-$ACCOUNT_ID-us-east-1:latest
docker run --init -i -p 3000:3000 $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/cdk-hnb659fds-container-assets-$ACCOUNT_ID-us-east-1:latest
```