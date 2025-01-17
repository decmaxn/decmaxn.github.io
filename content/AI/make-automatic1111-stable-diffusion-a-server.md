---
title: "Make Automatic1111 Stable Diffusion a Server"
date: 2025-01-17T17:04:12-05:00
draft: false
tags: ["python", "ai", "linux"]
---
## Install and test Automatic1111 Stable Diffusion 
Install Python3.10 and it's virtual env package.
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
grep -r "deadsnakes" /etc/apt/sources.list /etc/apt/sources.list.d/
sudo apt update
sudo apt install python3.10 # It seems it's already installed in my case
apt-cache policy python3.10 # confirmed the 3.10 python was installed from unbuntu official repo
```
The Deadsnakes PPA is a Personal Package Archive maintained by a group of volunteers that provides newer Python versions (and sometimes older versions that are no longer included in Ubuntu's official repositories). IT's well-maintained and trusted by the community

Find the automatic1111's stable diffusion webui github repo and clone it to ai fodler. Hey this repo seems not for cpu only.
```bash
$ mkdir ai
$ cd ai
/ai$ git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
/ai$ cd stable-diffusion-webui/
/ai/stable-diffusion-webui$ python3.10 -m venv a1111env
/ai/stable-diffusion-webui$ source a1111env/bin/activate
/ai/stable-diffusion-webui$ pip install -r requirements.txt
```
Run it for the first time, downloading the default models 
```bash
/ai/stable-diffusion-webui$ python3 launch.py --use-cpu all --no-half \
    --skip-torch-cuda-test --enable-insecure-extension-access
```
Create a SSH tunnel and access the web console through http://localhost:7860
```bash
ssh -i ~/.ssh/vma_rsa -L 7860:localhost:7860 vma@192.168.0.70
```

## moving the application to mnt volume with bigger space

```mv ai /mnt/mydisk/``` and hope it will work as is. However, the python venv has a lot of hardcoded path in scripts and even binary files.

Eventually I have to remove the a1111env folder and recreate a venv again. However, I have saved some time by manually moved some big models folders etc. nvidia/tensor before pip install again. 

## Using the webui.sh
Is there a better way to start the stable-diffusion by activate the venv and launch.py with all those parameters? Is there a way to access the site without using port forward? Let's using the repo's default webui starting script webui.sh. 

It does the python vevn stuff, I believe it will even create one if there isn't one already created.

However it doesn't work for me by default - of course I need to custmize for all those parameters, right? When I study the script, I realized that they want me to modify webui-user.sh for customization.
```
#!/usr/bin/env bash
#################################################
# Please do not make any changes to this file,  #
# change the variables in webui-user.sh instead #
#################################################
```
I studied the webui-user.sh, found it's meant to set some variables to customize the behavior of webui.sh. After quite a few tests, I found the following changes need to be made:
```
# Commandline arguments for webui.py, for example: export COMMANDLINE_ARGS="--medvram --opt-split-attention"
export COMMANDLINE_ARGS="--listen --use-cpu all --no-half --skip-torch-cuda-test --enable-insecure-extension-access"

# python3 venv without trailing slash (defaults to ${install_dir}/${clone_dir}/venv)
venv_dir="a1111venv"
```
Here are some explainations:

1. the "--listen" is to fix the problem that webui listen to 127.0.0.1 only. 
在服务器上运行以下命令查看 Web UI 是否监听 0.0.0.0：
```sudo netstat -tuln | grep 7860```
如果看到以下输出，说明 Web UI 已开放给所有网络设备：
```tcp        0      0 0.0.0.0:7860          0.0.0.0:*               LISTEN```
如果只看到 127.0.0.1:7860，说明只监听了本地，你需要加上 --listen 参数重新启动。
在 Stable Diffusion Web UI（Automatic1111 版） 的源码中（launch.py），--listen 参数的作用已经明确地将监听地址绑定为 0.0.0.0。这是 --listen 的默认行为。如果你使用 python3 launch.py --listen, 服务将对本地和外部网络都可访问。
1. "--use-cpu all --no-half --skip-torch-cuda-test --enable-insecure-extension-access" is from the command above to start the webui
1. "a1111venv" is from the error prompt when running webui.sh. If I don't change this, it will try to create a venv on the fly.

After the above changes, webui.sh will start webui and listen to access from the world.

## Create the systemd service file
To make it a server, we need to start stable-diffusion-webui automatically.

```bash
cat <<EOF > /etc/systemd/system/stable-diffusion-webui.service
[Unit]
Description=Stable Diffusion Web UI
After=network.target

[Service]
User=vma
Group=vma
WorkingDirectory=/mnt/mydisk/ai/stable-diffusion-webui
ExecStart=/mnt/mydisk/ai/stable-diffusion-webui/webui.sh
Restart=always
Environment="PATH=/usr/bin:/usr/local/bin:/mnt/mydisk/ai/stable-diffusion-webui/a1111venv/bin"

[Install]
WantedBy=multi-user.target
EOF
```